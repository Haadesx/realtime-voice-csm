import requests
from generator import load_csm_1b
import torchaudio
import torch
from huggingface_hub import hf_hub_download
import sounddevice as sd
import soundfile as sf
import os
from functools import lru_cache
import speech_recognition as sr
import numpy as np
import wave
import time
from tqdm import tqdm
from colorama import init, Fore, Back, Style
import threading
import keyboard

# Initialize colorama for cross-platform colored output
init()

# Global flag for stopping
stop_listening = threading.Event()

# Initialize Sesame voice generator with optimizations
if torch.cuda.is_available():
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    print(f"{Fore.GREEN}Using CUDA with optimizations{Style.RESET_ALL}")
else:
    device = "cpu"
    print(f"{Fore.YELLOW}Using CPU{Style.RESET_ALL}")

# Cache directory for audio files
CACHE_DIR = "audio_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Load model once and cache it
print(f"{Fore.CYAN}Loading models...{Style.RESET_ALL}")
with tqdm(total=1, desc="Loading CSM model") as pbar:
    model_path = hf_hub_download(repo_id="sesame/csm-1b", filename="ckpt.pt")
    generator = load_csm_1b(model_path, device)
    generator._model.eval()
    pbar.update(1)

# Initialize speech recognition with optimized settings
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8  # Increased for better sentence completion
recognizer.phrase_threshold = 0.5  # Increased for better phrase detection

def show_listening_animation():
    """Show an animation while listening"""
    frames = ["🎤 ", "🎤  ●", "🎤  ● ●", "🎤  ● ● ●"]
    i = 0
    while not stop_listening.is_set():
        print(f"\r{Fore.CYAN}{frames[i % len(frames)]}{Style.RESET_ALL} (Press 'Esc' to stop listening)", end="", flush=True)
        i += 1
        time.sleep(0.3)
    print("\r", end="", flush=True)

def handle_keyboard():
    """Handle keyboard events"""
    while not stop_listening.is_set():
        if keyboard.is_pressed('esc'):
            stop_listening.set()
            print(f"\n{Fore.YELLOW}Stopping...{Style.RESET_ALL}")
            break
        time.sleep(0.1)

def record_audio():
    """Record audio from microphone"""
    stop_listening.clear()
    
    try:
        with sr.Microphone() as source:
            print(f"\n{Fore.CYAN}Adjusting for ambient noise...{Style.RESET_ALL}")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Start the listening animation and keyboard handler in separate threads
            animation_thread = threading.Thread(target=show_listening_animation)
            keyboard_thread = threading.Thread(target=handle_keyboard)
            animation_thread.start()
            keyboard_thread.start()
            
            print(f"\n{Fore.GREEN}Listening... (Press 'Esc' to stop){Style.RESET_ALL}")
            try:
                audio = recognizer.listen(source, phrase_time_limit=None)
                stop_listening.set()
                animation_thread.join()
                keyboard_thread.join()
                return audio
            except Exception as e:
                print(f"\n{Fore.RED}Error recording: {e}{Style.RESET_ALL}")
                return None
            
    except Exception as e:
        print(f"\n{Fore.RED}Error with microphone: {e}{Style.RESET_ALL}")
        return None
    finally:
        stop_listening.set()

def transcribe_audio(audio):
    """Convert speech to text"""
    if audio is None:
        return None
        
    try:
        text = recognizer.recognize_google(audio)
        print(f"\n{Fore.GREEN}You said: {Style.BRIGHT}{text}{Style.RESET_ALL}")
        return text
    except sr.UnknownValueError:
        print(f"\n{Fore.YELLOW}Could not understand audio{Style.RESET_ALL}")
        return None
    except sr.RequestError as e:
        print(f"\n{Fore.RED}Error with speech recognition: {e}{Style.RESET_ALL}")
        return None

@lru_cache(maxsize=100)
def get_cached_response(text):
    """Get cached response from Ollama"""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "dolphin3",
        "prompt": format_prompt(text),
        "stream": False
    }
    try:
        print(f"\n{Fore.CYAN}Getting AI response...{Style.RESET_ALL}")
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"\n{Fore.RED}Error with Ollama: {e}{Style.RESET_ALL}")
        return None

def format_prompt(user_input):
    return f"""<|im_start|>system
You are Dolphin, a helpful AI assistant. Provide clear and complete responses.<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""

@torch.inference_mode()
def generate_optimized_speech(text, speaker=0):
    """Generate speech with optimized parameters"""
    cache_file = os.path.join(CACHE_DIR, f"{hash(text)}.wav")
    
    if os.path.exists(cache_file):
        return cache_file
    
    print(f"\n{Fore.CYAN}Generating voice response...{Style.RESET_ALL}")
    audio = generator.generate(
        text=text,
        speaker=speaker,
        context=[],
        max_audio_length_ms=20_000,  # Increased to handle longer responses
        temperature=0.7,
        topk=30,
    )
    
    torchaudio.save(cache_file, audio.unsqueeze(0).cpu(), generator.sample_rate, bits_per_sample=16)
    return cache_file

def play_audio(file_path):
    """Play audio file using sounddevice"""
    try:
        print(f"\n{Fore.CYAN}🔊 Playing response...{Style.RESET_ALL}")
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate, blocking=True)  # Changed to blocking for complete playback
    except Exception as e:
        print(f"\n{Fore.RED}Error playing audio: {e}{Style.RESET_ALL}")

def main():
    print(f"\n{Fore.GREEN}{'='*50}")
    print("Voice Interactive Chat")
    print(f"{'='*50}{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Instructions:")
    print("1. Just start speaking when you see the microphone 🎤")
    print("2. Press 'Esc' anytime to stop listening")
    print("3. Say 'quit' to exit the program")
    print(f"\n{Fore.YELLOW}Ready for conversation!{Style.RESET_ALL}\n")
    
    while True:
        audio_input = record_audio()
        if stop_listening.is_set() and audio_input is None:
            continue
            
        text = transcribe_audio(audio_input)
        if not text:
            continue
            
        if text.lower() == 'quit':
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break
        
        response = get_cached_response(text)
        if response:
            print(f"\n{Fore.BLUE}Assistant: {Style.BRIGHT}{response}{Style.RESET_ALL}")
            output_file = generate_optimized_speech(response)
            play_audio(output_file)

if __name__ == "__main__":
    main() 
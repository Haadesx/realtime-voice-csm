import requests
from generator import load_csm_1b
import torchaudio
import torch
from huggingface_hub import hf_hub_download
import json
import sounddevice as sd
import soundfile as sf

# Initialize Sesame voice generator
if torch.cuda.is_available():
    device = "cuda"
    print("Using CUDA")
else:
    device = "cpu"
    print("Using CPU")

model_path = hf_hub_download(repo_id="sesame/csm-1b", filename="ckpt.pt")
generator = load_csm_1b(model_path, device)

def play_audio(file_path):
    """Play audio file using sounddevice"""
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()  # Wait until the audio is finished playing

def generate_speech(text, output_file="response.wav", speaker=0):
    """Generate speech from text using Sesame model"""
    audio = generator.generate(
        text=text,
        speaker=speaker,
        context=[],
        max_audio_length_ms=20_000,  # 30 seconds max
    )
    torchaudio.save(output_file, audio.unsqueeze(0).cpu(), generator.sample_rate)
    return output_file

def format_prompt(user_input):
    """Format the prompt using ChatML format for Dolphin3"""
    return f"""<|im_start|>system
You are Dolphin, a helpful AI assistant. You provide clear, concise, and natural-sounding responses that will be converted to speech.<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""

def chat_with_dolphin(prompt):
    """Send a message to Ollama's Dolphin model and get response"""
    url = "http://localhost:11434/api/generate"
    formatted_prompt = format_prompt(prompt)
    
    data = {
        "model": "dolphin3",
        "prompt": formatted_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "I apologize, but I encountered an error while processing your request."

def main():
    print("Welcome to Interactive Chat with Voice!")
    print("Type your message and press Enter. Type 'quit' to exit.")
    print("Using Dolphin3.0-Llama3.2-1B for text generation and Sesame CSM for voice synthesis")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            break
        
        # Get response from Dolphin
        response = chat_with_dolphin(user_input)
        print(f"\nAssistant: {response}")
        
        # Generate speech for the response
        try:
            output_file = generate_speech(response)
            print(f"Voice response saved to: {output_file}")
            print("Playing audio response...")
            play_audio(output_file)
        except Exception as e:
            print(f"Error generating/playing speech: {e}")

if __name__ == "__main__":
    main() 
from huggingface_hub import hf_hub_download
from generator import load_csm_1b
import torchaudio
import torch

if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
    print("Using CUDA")
else:
    device = "cpu"
    print("Using CPU")
model_path = hf_hub_download(repo_id="sesame/csm-1b", filename="ckpt.pt")
generator = load_csm_1b(model_path, device)
audio = generator.generate(
    text="Hello from Sesame.",
    speaker=1,
    context=[],
    max_audio_length_ms=10_000,
)

torchaudio.save("audio00.wav", audio.unsqueeze(0).cpu(), generator.sample_rate)



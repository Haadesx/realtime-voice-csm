# Real-Time Voice Conversation System with Sesame CSM

An uncensored implementation of the Sesame CSM (Conversational Speech Model) with real-time voice interaction capabilities. This project combines Sesame's speech synthesis with Dolphin3's language model for natural conversations.

## ⚠️ Important Disclaimer

This is an educational project that provides an uncensored implementation of Sesame's CSM model. While this offers more flexibility than standard implementations, it comes with important responsibilities:

### Ethical Usage Guidelines

- **Educational Purpose Only**: This implementation is intended strictly for research and educational purposes.
- **No Harmful Use**: Do not use this system to:
  - Generate deceptive or misleading content
  - Create deepfake voice content without explicit consent
  - Impersonate individuals or entities
  - Spread misinformation or engage in fraud
  - Cause harm to individuals or organizations

### Legal Notice

By using this code, you agree to:
1. Use it responsibly and ethically
2. Comply with all applicable laws and regulations
3. Accept full responsibility for any consequences of your usage
4. Not use the system for any malicious or harmful purposes

## Features

- 🎤 Real-time voice input with instant stop capability
- 🤖 Integration with Dolphin3 language model
- 🗣️ High-quality speech synthesis using Sesame CSM
- ⚡ GPU-accelerated processing (when available)
- 💾 Response caching for improved performance
- 🎯 Optimized for natural conversation flow
- 📊 Real-time audio visualization
- 🌐 Web interface for easy interaction

## System Requirements

### Hardware Requirements
- **CPU**: Intel Core i5/AMD Ryzen 5 or better (recommended)
- **RAM**: Minimum 8GB, 16GB recommended
- **Storage**: At least 2GB free space
- **GPU**: CUDA-compatible GPU recommended (for faster processing)
  - NVIDIA GPU with Compute Capability 3.5 or higher
  - At least 4GB VRAM recommended
- **Microphone**: Any working microphone (built-in or external)
- **Internet Connection**: Required for speech recognition

### Software Requirements

#### Required Software
1. **Python 3.11.9** (Exact version required)
   - [Download Python 3.11.9](https://www.python.org/downloads/release/python-3119/)
   - Windows: Use the provided `python-3.11.9-amd64.exe` installer
   - Linux/Mac: Download from Python's official website

2. **Git**
   - Windows: [Git for Windows](https://gitforwindows.org/)
   - Linux: `sudo apt-get install git`
   - Mac: `brew install git`

3. **Ollama**
   - Download from [ollama.ai](https://ollama.ai)
   - Required for running the Dolphin3 language model

## Detailed Setup Instructions

### 1. Python Installation (Windows)
```bash
# Run the installer with these options:
# - Add Python 3.11.9 to PATH
# - Install for all users
# - Customize installation:
#   - Select all optional features
#   - Advanced Options: Select all
#   - Install to: C:\Python311
python-3.11.9-amd64.exe
```

### 2. Verify Python Installation
```bash
python --version  # Should show Python 3.11.9
pip --version    # Should show pip with Python 3.11.9
```

### 3. Clone the Repository
```bash
git clone https://github.com/Haadesx/realtime-voice-csm.git
cd realtime-voice-csm
```

### 4. Set Up Virtual Environment
```bash
# Windows
python -m venv csm/.venv
csm/.venv/Scripts/activate

# Linux/Mac
python -m venv csm/.venv
source csm/.venv/bin/activate
```

### 5. Install Dependencies
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### 6. Install and Configure Ollama

#### Windows Users
1. Install WSL2 if not already installed:
```bash
wsl --install
```
2. Install Ollama in WSL2:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Linux Users
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Mac Users
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 7. Download and Run Dolphin3 Model
```bash
# Start Ollama service first
ollama serve

# In a new terminal, pull and run Dolphin3
ollama pull dolphin3
ollama run dolphin3
```

## Running the Application

### 1. Start the Web Interface
```bash
# Make sure you're in the project directory with venv activated
cd csm
python web_interface.py
```

### 2. Access the Interface
- Open your web browser
- Navigate to `http://localhost:5000`
- Allow microphone access when prompted

### 3. Using the Interface
1. Click the central button to start recording
2. Speak naturally into your microphone
3. Watch the input visualizer (left) respond to your voice
4. Click the button again to stop recording
5. Wait for the AI response and watch the output visualizer (right)

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Installation Issues
```bash
# If Python isn't recognized, add to PATH manually:
# Windows: Edit system environment variables > Path > Add:
C:\Python311
C:\Python311\Scripts

# Verify with:
python --version
```

#### 2. Virtual Environment Issues
```bash
# If venv activation fails, try:
# Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/Mac
chmod +x csm/.venv/bin/activate
```

#### 3. CUDA Issues
```bash
# Verify CUDA installation:
python -c "import torch; print(torch.cuda.is_available())"

# Should return True if CUDA is properly installed
```

#### 4. Audio Issues
- Check microphone settings in system preferences
- Verify microphone permissions for browser
- Try different USB ports for external microphones

#### 5. Ollama Connection Issues
```bash
# Check if Ollama is running:
curl http://localhost:11434/api/tags

# Restart Ollama if needed:
ollama serve
```

## Performance Optimization

### GPU Acceleration
- Enable CUDA optimization in `fast_chat.py`:
```python
device = "cuda" if torch.cuda.is_available() else "cpu"
```

### Memory Usage
- Adjust batch size in `models.py`:
```python
batch_size = 16  # Decrease if running out of memory
```

### Audio Processing
- Modify audio parameters in `web_interface.py`:
```python
sample_rate = 44100  # Adjust based on your needs
buffer_size = 1024   # Increase for better quality
```

## Contributing

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```bash
git commit -m "Add your feature description"
```
4. Push to your fork:
```bash
git push origin feature/your-feature-name
```
5. Create a Pull Request

## Support and Community

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Join our GitHub Discussions for general questions
- **Updates**: Watch the repository for new releases and updates

## Author

**Varesh Patel**
- GitHub: [@Haadesx](https://github.com/Haadesx)
- AI Enthusiast and Developer

## License

This project is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Sesame AI Labs](https://www.sesame.com) for the CSM model
- The Ollama team for the Dolphin3 model
- Contributors to the various open-source libraries used

## Version History

- v1.0.0 - Initial release
  - Basic voice interaction
  - Web interface
  - Real-time visualization

## Future Plans

- [ ] Multi-language support
- [ ] Custom voice cloning
- [ ] Mobile interface
- [ ] Docker containerization
- [ ] Cloud deployment options

---

*Remember: With great power comes great responsibility. Use this tool ethically and responsibly.* 
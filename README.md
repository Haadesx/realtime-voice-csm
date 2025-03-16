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

## Requirements

- Python 3.10 or newer
- CUDA-compatible GPU (recommended)
- Internet connection for speech recognition
- [Ollama](https://ollama.ai/) running locally with Dolphin3 model

### Required Packages
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Setup

1. Clone the repository:
\`\`\`bash
git clone https://github.com/Haadesx/realtime-voice-csm.git
cd realtime-voice-csm
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Install and start Ollama with Dolphin3:
\`\`\`bash
ollama run dolphin3
\`\`\`

4. Run the application:
\`\`\`bash
python csm/fast_chat.py
\`\`\`

## Usage

1. Start the program and wait for the microphone icon (🎤)
2. Begin speaking naturally when you see the icon
3. Press 'Esc' at any time to stop recording
4. Wait for the AI response and voice synthesis
5. Say 'quit' to exit the program

## Technical Details

- Uses Sesame's CSM-1B model for speech synthesis
- Integrates with Dolphin3 (based on Llama3.2-1B) for text generation
- Implements real-time voice processing with optimized parameters
- Features response caching for improved performance
- Supports both CPU and GPU acceleration

## Customization

You can modify various parameters in the code:
- Speech recognition sensitivity
- Response length and quality
- Voice characteristics
- Model parameters
- Cache settings

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request

## Author

**Varesh Patel**
- GitHub: [@Haadesx](https://github.com/Haadesx)
- AI Enthusiast and Developer

## Acknowledgments

- [Sesame AI Labs](https://www.sesame.com) for the CSM model
- The Ollama team for the Dolphin3 model
- Contributors to the various open-source libraries used

## License

This project is released under the MIT License. However, please note that this does not override any restrictions or licenses of the underlying models and libraries used.

## Disclaimer of Warranty

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. THE AUTHOR IS NOT RESPONSIBLE FOR ANY CONSEQUENCES OF USING THIS SOFTWARE.

---

*Remember: With great power comes great responsibility. Use this tool ethically and responsibly.* 
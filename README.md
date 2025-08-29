# AIDesk - Intelligent Desktop Assistant

![Desktop Assistant - AIDesk](AIDesk.png)

**AIDesk** is a modern Python-based desktop assistant powered by Google's Gemini AI. It combines voice commands, GUI interactions, and advanced AI capabilities to create a seamless desktop automation experience.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

AIDesk is a sophisticated desktop assistant that integrates Google's cutting-edge Gemini AI with practical desktop automation features. It provides:

- Intelligent AI-powered conversations using Google's Gemini
- Voice-controlled interface with natural language processing
- Modern PyQt5-based graphical interface
- System automation capabilities
- Real-time weather information
- Web service integrations

The assistant uses streaming responses for longer queries and provides context-aware interactions through its advanced AI model. Built with Python, it offers both voice and text-based interactions through an intuitive GUI.

## Features

### AI Capabilities
- Advanced conversational AI powered by Google's Gemini
- Contextual response generation with streaming support
- Natural language understanding and processing
- Intelligent task interpretation and execution

### Voice Interface
- Speech recognition for hands-free control
- Text-to-speech response system
- Clear voice feedback for commands
- Multi-language voice support

### System Functions
- Screenshot capture with automatic file naming
- Date and time information
- System status monitoring
- Clipboard management

### Web Integration
- Intelligent web searches (Google, YouTube)
- Smart website navigation
- YouTube Music integration
- Weather information for any city

### User Interface
- Modern PyQt5-based GUI
- Responsive design
- Easy-to-use controls
- Visual feedback for actions

## Prerequisites

Before installing AIDesk, ensure your system meets these requirements:

### System Requirements
- Python 3.8 or higher
- Windows 10/11 (primary support)
- Minimum 4GB RAM
- Microphone for voice commands
- Internet connection

### API Requirements
- Google Gemini API key (for AI features)
- WeatherAPI key (for weather information)

### Python Packages
- PyQt5 for GUI
- google-generativeai for Gemini integration
- pyttsx3 for text-to-speech
- SpeechRecognition for voice commands
- Additional dependencies in `requirements.txt`

## Installation

### Quick Start

1. Clone the repository:
    ```bash
    git clone https://github.com/Desai-Vedant/AIDesk.git
    ```

2. Set up your Python environment:
    ```bash
    cd AIDesk
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Environment Setup

AIDesk uses environment variables for secure configuration. Follow these steps:

1. Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

2. Configure your `.env` file with your API keys and preferences:
    ```env
    # API Keys
    GEMINI_API_KEY=your_gemini_api_key_here
    WEATHER_API_KEY=your_weather_api_key_here

    # User Configuration
    OWNER_NAME=Your_Name
    ASSISTANT_NAME=AIDesk
    SCREENSHOT_PATH=C:/Users/YourUser/Pictures/Screenshots/
    ```

### API Keys Setup

1. **Google Gemini API**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

2. **WeatherAPI**
   - Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
   - Generate an API key
   - Add it to your `.env` file

### Optional Configuration

- **Screenshot Directory**: Customize the screenshot save location in `.env`
- **Assistant Name**: Change the assistant's name for personalization
- **Voice Settings**: Adjust voice parameters in `functions.py` if needed

## Usage

### Starting the Assistant

1. Activate your virtual environment:
    ```bash
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Launch AIDesk:
    ```bash
    python main.py
    ```

### Voice Commands

AIDesk responds to various voice commands:

- **Web Searches**: 
  - "Search [query] on Google"
  - "Search [query] on YouTube"
  - "Play [song] on YouTube Music"

- **System Commands**:
  - "Take a screenshot"
  - "What's the time?"
  - "What's today's date?"

- **Weather Information**:
  - "What's the temperature in [city]?"
  - "How's the weather in [city]?"

- **Website Navigation**:
  - "Open [website]" (Supports major websites like Google, YouTube, GitHub, etc.)

- **AI Conversations**:
  - Ask any question for Gemini AI-powered responses
  - Get detailed explanations and assistance

### GUI Interface

The modern interface provides:
- Voice command button
- Text input option
- Response display area
- Status indicators
- Clipboard integration

## Contributing

We welcome contributions to AIDesk! Here's how you can help:

### Ways to Contribute
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit pull requests
- Share usage examples

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please follow our coding standards and include appropriate tests.

---

## Support and Community

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Join project discussions on GitHub
- **Updates**: Star the repository to stay informed about updates

Thank you for using AIDesk! For questions or support, please open an issue on GitHub.

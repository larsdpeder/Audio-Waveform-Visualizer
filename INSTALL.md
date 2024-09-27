# Installation Guide

Follow these steps to set up the Audio Waveform Visualizer on your system:

1. Ensure you have Python 3.6 or higher installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

2. Clone this repository or download the source code:
   ```
   git clone https://github.com/yourusername/audio-waveform-visualizer.git
   cd audio-waveform-visualizer
   ```

3. It's recommended to create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. You're all set! You can now run the script:
   ```
   python waveform_visualizer.py
   ```

## Troubleshooting

- If you encounter issues with PyAudio installation on macOS, you may need to install portaudio first:
  ```
  brew install portaudio
  ```

- On Linux, you might need to install additional system packages. For Ubuntu or Debian-based systems:
  ```
  sudo apt-get install python3-dev libasound2-dev
  ```

If you encounter any other issues, please check the project's issue tracker on GitHub or create a new issue.

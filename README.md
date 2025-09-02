# Audio-Trimmer
This python code allows you to trim audio files. Here's what it does:

## Features:
- **Flexible input**: Takes an audio file as a command-line argument or prompts for it
- **Multiple timestamp formats**: Supports MM:SS, HH:MM:SS, seconds, or milliseconds
- **Smart defaults**: Press Enter to use the beginning/end of the file
- **File validation**: Checks if the input file exists and validates timestamps
- **Progress feedback**: Shows the audio duration and extraction progress
- **Auto-naming**: Suggests a default output filename with "_trimmed" suffix

## Installation Requirements:
Before using the script, you'll need to install the required library:

```bash
pip install pydub
```

**Important**: You'll also need FFmpeg installed on your system:
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or equivalent

The script supports various audio formats including MP3, WAV, FLAC, OGG, and more (anything that FFmpeg can handle). It will automatically detect the format from the file extension and maintain the same format for the output file.

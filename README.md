# YouTube Transcript Downloader

A Python tool that downloads YouTube videos, converts them to audio, and generates transcripts using OpenAI's Whisper API. This tool is designed to be simple to use and produces high-quality transcriptions while minimizing bandwidth usage by downloading the lowest quality audio necessary.

## Features

- Download audio from YouTube videos in lowest quality to save bandwidth
- Automatic audio conversion to MP3 format
- Transcription using OpenAI's Whisper API
- Automatic cleanup of temporary files
- Simple command-line interface
- Customizable output directory for transcripts

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio conversion)
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone [your-repo-url]
cd youtube-transcript-downloader
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg:
   - **Windows**: 
     1. Download FFmpeg from [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)
     2. Extract the zip file
     3. Copy `ffmpeg.exe`, `ffprobe.exe`, and `ffplay.exe` from the `bin` folder
     4. Paste them into your project directory
   
   - **Linux**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   
   - **macOS**:
     ```bash
     brew install ffmpeg
     ```

4. Set up your OpenAI API key:
   - Replace `"your-api-key-here"` in `youtube_transcriber_v5.py` with your actual OpenAI API key
   - Alternatively, set it as an environment variable:
     ```bash
     export OPENAI_API_KEY='your-api-key-here'
     ```

## Usage

1. Run the script:
```bash
python youtube_transcriber_v5.py
```

2. When prompted:
   - Enter the output folder path (or press Enter for default)
   - Enter the YouTube URL you want to transcribe

3. The script will:
   - Download the audio
   - Convert it to MP3
   - Transcribe it using Whisper
   - Save the transcript to your specified folder
   - Clean up temporary files

The transcript will be saved as `[video_id]_transcript.txt` in your specified output folder.

## Example

```bash
$ python youtube_transcriber_v5.py
Enter output folder path (press Enter for default: C:\path\to\transcripts): 

Transcripts will be saved to: C:\path\to\transcripts

Enter YouTube URL: https://www.youtube.com/watch?v=example

[Output showing download and transcription progress]

Success! Transcript saved to: C:\path\to\transcripts\example_transcript.txt
```

## Error Handling

The script includes comprehensive error handling for:
- Invalid YouTube URLs
- Download failures
- Audio conversion issues
- Transcription errors
- File system operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [OpenAI Whisper](https://openai.com/research/whisper) for transcription
- [FFmpeg](https://ffmpeg.org/) for audio processing

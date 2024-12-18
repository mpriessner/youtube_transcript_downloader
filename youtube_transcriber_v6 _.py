import os
import yt_dlp
from openai import OpenAI
from pathlib import Path
import sys
from pydub import AudioSegment
import math

class YouTubeTranscriber:
    def __init__(self, api_key, output_folder="transcripts"):
        self.client = OpenAI(api_key=api_key)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        # Maximum file size for Whisper API (25MB)
        self.max_file_size = 25 * 1024 * 1024  # 25MB in bytes

    def download_audio(self, youtube_url, output_path):
        """Download the audio from a YouTube video in lowest quality"""
        try:
            print(f"Attempting to download audio from: {youtube_url}")
            
            ydl_opts = {
                'format': 'worstaudio/worst',
                'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '96',
                }],
                'quiet': False,
                'no_warnings': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                video_id = info['id']
                audio_file = os.path.join(output_path, f"{video_id}.mp3")
                print(f"Successfully downloaded to: {audio_file}")
                return audio_file
                
        except Exception as e:
            print(f"Detailed error in download_audio: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            if hasattr(e, 'args'):
                print(f"Error args: {e.args}")
            raise

    def split_audio(self, audio_file, chunk_duration_ms=600000):  # 10 minutes chunks
        """Split audio file into smaller chunks"""
        try:
            print(f"Loading audio file: {audio_file}")
            audio = AudioSegment.from_mp3(audio_file)
            total_duration = len(audio)
            chunks = []
            
            # Calculate number of chunks needed
            num_chunks = math.ceil(total_duration / chunk_duration_ms)
            print(f"Splitting audio into {num_chunks} chunks...")

            for i in range(num_chunks):
                start_time = i * chunk_duration_ms
                end_time = min((i + 1) * chunk_duration_ms, total_duration)
                
                chunk = audio[start_time:end_time]
                chunk_path = f"{audio_file[:-4]}_chunk_{i}.mp3"
                chunk.export(chunk_path, format="mp3")
                chunks.append(chunk_path)
                print(f"Created chunk {i+1}/{num_chunks}")

            return chunks
        except Exception as e:
            print(f"Error splitting audio: {str(e)}")
            raise

    def transcribe_audio_chunk(self, audio_file):
        """Transcribe a single audio chunk using Whisper API"""
        try:
            print(f"Transcribing chunk: {os.path.basename(audio_file)}")
            with open(audio_file, "rb") as audio:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            print(f"Error transcribing chunk: {str(e)}")
            raise

    def process_video(self, youtube_url):
        """Process a YouTube video: download audio and transcribe"""
        try:
            # Create a temporary directory for audio
            temp_dir = Path("temp_audio")
            temp_dir.mkdir(exist_ok=True)
            print(f"Created temporary directory: {temp_dir}")

            # Download audio
            audio_file = self.download_audio(youtube_url, str(temp_dir))
            print(f"Using audio file: {audio_file}")
            
            # Split audio into chunks
            print("Splitting audio into chunks...")
            chunks = self.split_audio(audio_file)
            
            # Transcribe each chunk
            print("Transcribing chunks...")
            full_transcript = []
            for chunk in chunks:
                transcript = self.transcribe_audio_chunk(chunk)
                full_transcript.append(transcript)
            
            # Combine transcripts
            complete_transcript = "\n".join(full_transcript)
            
            # Get video ID and save transcript
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                video_id = info['id']
            
            transcript_file = self.output_folder / f"{video_id}_transcript.txt"
            with open(transcript_file, "w", encoding="utf-8") as f:
                f.write(complete_transcript)
            
            print(f"Transcript saved to: {transcript_file}")
            
            # Cleanup
            print("Cleaning up temporary files...")
            for chunk in chunks:
                if os.path.exists(chunk):
                    os.remove(chunk)
                    print(f"Cleaned up chunk: {chunk}")
            
            if os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"Cleaned up audio file: {audio_file}")
            
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
                print(f"Cleaned up temp directory: {temp_dir}")
            
            return transcript_file
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            raise

def main():
    # Replace with your OpenAI API key
    api_key = "API_KEY"
    
    # Get output folder from user
    default_output = os.path.join(os.getcwd(), "transcripts")
    output_folder = input(f"Enter output folder path (press Enter for default: {default_output}): ").strip()
    if not output_folder:
        output_folder = default_output
    
    # Create transcriber instance
    transcriber = YouTubeTranscriber(api_key, output_folder=output_folder)
    print(f"\nTranscripts will be saved to: {output_folder}")
    
    # Example usage
    youtube_url = input("\nEnter YouTube URL: ")
    try:
        transcript_file = transcriber.process_video(youtube_url)
        print(f"\nSuccess! Transcript saved to: {transcript_file}")
        print(f"You can find your transcript at: {os.path.abspath(transcript_file)}")
    except Exception as e:
        print(f"\nFailed to process video: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

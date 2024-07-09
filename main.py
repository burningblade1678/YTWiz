# YouTube Video Converter Project

## Project Structure
'''
youtube-video-converter/
│
├── main.py
├── downloader.py
├── converter.py
├── file_manager.py
├── requirements.txt
├── .gitignore
└── README.md
'''
## File Contents

### main.py


import argparse
from downloader import download_video
from converter import convert_video
from file_manager import save_file, clean_up

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Downloader and Converter")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("format", choices=["mp4", "mp3", "wav", "avi", "mov"], help="Output format")
    parser.add_argument("output", help="Output file name")
    parser.add_argument("--location", default=".", help="Download location (default: current directory)")
    args = parser.parse_args()

    try:
        print("Downloading video...")
        video_path = download_video(args.url, args.location)
        
        print("Converting video...")
        converted_path = convert_video(video_path, args.format)
        
        print("Saving file...")
        final_path = save_file(converted_path, args.output, args.location)
        
        print(f"Video successfully downloaded and converted: {final_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        clean_up()

if __name__ == "__main__":
    main()
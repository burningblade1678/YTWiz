import argparse
from gui import main as gui_main
from downloader import download_video
from converter import convert_video
from file_manager import save_file, clean_up

def cli_main(args):
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
    parser = argparse.ArgumentParser(description="YTWiz - YouTube Video Downloader and Converter")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--url", help="YouTube video URL")
    parser.add_argument("--format", choices=["mp3", "wav", "ogg", "aac"], help="Output format")
    parser.add_argument("--output", help="Output file name")
    parser.add_argument("--location", default=".", help="Download location (default: current directory)")
    
    args = parser.parse_args()
    
    if args.cli:
        if not all([args.url, args.format, args.output]):
            parser.error("--cli mode requires --url, --format, and --output arguments")
        cli_main(args)
    else:
        gui_main()
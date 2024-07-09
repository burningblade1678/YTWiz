# YouTube Video Converter

This Python application allows you to download YouTube videos and convert them to various formats.

## Features

- Download YouTube videos
- Convert videos to mp4, mp3, wav, avi, and mov formats
- Simple command-line interface
- Customizable output file name and location

## Project Structure

YTwiz/
│
├── `main.py`
├── `downloader.py`
├── `converter.py`
├── `file_manager.py`
├── `requirements.txt`
├── `.gitignore`
└── `README.md`

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/your-username/youtube-video-converter.git
   cd youtube-video-converter
   ```
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application using the following command:

```
python main.py <youtube_url> <output_format> <output_name> [--location <download_location>]
```

Example:

```
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ mp3 my_song --location ~/Downloads 
```

## Supported Formats

- mp4: Standard video format, good quality and compatibility
- mp3: Audio-only format, suitable for music
- wav: Uncompressed audio format, larger file size but higher quality
- avi: Older video format, good compatibility with older systems
- mov: QuickTime video format, commonly used on Apple devices

## Limitations

- Some video formats may not be available for certain YouTube videos
- High-resolution videos may take longer to download and convert
- Audio extraction quality depends on the original video's audio quality

## Future Improvements

- Add support for downloading entire playlists
- Implement a graphical user interface (GUI)
- Add options for video quality selection
- Implement multi-threading for faster conversions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pytube](https://github.com/pytube/pytube) for YouTube video downloading
- [MoviePy](https://zulko.github.io/moviepy/) for video conversion

## Contact

If you have any questions or suggestions, please open an issue or contact burningblade1678.

---

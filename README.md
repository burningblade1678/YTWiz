# YTWiz

YTWiz is a user-friendly application for downloading YouTube videos and converting them to various audio formats. With a simple and intuitive interface, YTWiz makes it easy to save your favorite YouTube content for offline listening.

![YTWiz Screenshot](screenshot.png)

## Features

- Download videos from YouTube
- Convert videos to popular audio formats (MP3, WAV, OGG)
- Batch processing for multiple videos
- Simple and intuitive graphical user interface
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

### For End Users

#### Windows
1. Download the latest YTWiz.zip from the [Releases](https://github.com/yourusername/YTWiz/releases) page.
2. Extract the zip file to a location of your choice (e.g., `C:\Program Files\YTWiz`).
3. Double-click on `YTWiz.exe` to run the application.
4. (Optional) Right-click on `YTWiz.exe`, select "Send to" > "Desktop (create shortcut)" to create a desktop shortcut.

#### macOS
1. Download the latest YTWiz.dmg from the [Releases](https://github.com/yourusername/YTWiz/releases) page.
2. Open the .dmg file.
3. Drag the YTWiz app to your Applications folder.
4. Run YTWiz from your Applications folder or Launchpad.

### For Developers

To set up YTWiz for development:

1. Clone the repository:
```
git clone https://github.com/yourusername/YTWiz.git
cd YTWiz
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```
3. Install the required dependencies:

```
pip install -r requirements.txt
```
4. run the application:

```
python main.py
```

## Usage

1. Launch YTWiz.
2. Enter a YouTube URL in the input field and click "Add".
3. Select your desired output format(s) (MP3, WAV, OGG).
4. Choose the output location for your converted files.
5. Click "Download and Convert".
6. Wait for the process to complete. Your files will be saved in the chosen output location.

## Building from Source

To build YTWiz into a standalone executable:

1. Ensure you have PyInstaller installed:
```
pip install pyinstaller
```
2. Run the build script:
- On Windows: `build.bat`
- On macOS/Linux: `./build.sh`

3. The packaged application will be available in the `dist/YTWiz` directory.

## Project Structure

- `main.py`: Entry point of the application
- `gui.py`: GUI implementation
- `downloader.py`: YouTube video downloading logic
- `converter.py`: Audio conversion logic
- `file_manager.py`: File management utilities
- `build.spec`: PyInstaller specification file
- `build.bat`/`build.sh`: Build scripts for Windows and macOS/Linux
- `requirements.txt`: List of Python dependencies
- `youtube_wizard_logo.png`: Application logo

## Dependencies

- Python 3.7+
- yt-dlp
- PyQt5
- moviepy

For a complete list of dependencies, see `requirements.txt`.

## Contributing

Contributions to YTWiz are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the graphical user interface
- [moviepy](https://zulko.github.io/moviepy/) for video/audio conversion

## Contact
Feel free to open an issue and I'll get back to you asap!

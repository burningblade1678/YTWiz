import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from downloader import download_video
from converter import convert_video
from file_manager import save_file, clean_up

class DownloadThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, format, output_path):
        QThread.__init__(self)
        self.url = url
        self.format = format
        self.output_path = output_path

    def run(self):
        try:
            self.progress.emit("Downloading video...")
            video_path = download_video(self.url, self.output_path)
            
            self.progress.emit("Converting video...")
            converted_path = convert_video(video_path, self.format)
            
            self.progress.emit("Saving file...")
            final_path = save_file(converted_path, os.path.basename(converted_path), self.output_path)
            
            self.finished.emit(final_path)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            clean_up()

class YouTubeConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "mp3", "wav", "avi", "mov"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # Output location
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Location:"))
        self.output_path = QLineEdit()
        self.output_path.setText(os.path.expanduser("~/Downloads"))
        output_layout.addWidget(self.output_path)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_output)
        output_layout.addWidget(self.browse_button)
        layout.addLayout(output_layout)

        # Download button
        self.download_button = QPushButton("Download and Convert")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle("YouTube Video Converter")
        self.setGeometry(300, 300, 500, 200)

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path.setText(folder)

    def start_download(self):
        url = self.url_input.text()
        format = self.format_combo.currentText()
        output_path = self.output_path.text()

        if not url or not output_path:
            QMessageBox.warning(self, "Input Error", "Please enter a URL and select an output location.")
            return

        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)

        self.thread = DownloadThread(url, format, output_path)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.download_finished)
        self.thread.error.connect(self.download_error)
        self.thread.start()

    def update_progress(self, message):
        self.progress_bar.setValue(self.progress_bar.value() + 33)
        self.progress_bar.setFormat(message)

    def download_finished(self, final_path):
        self.progress_bar.setValue(100)
        self.download_button.setEnabled(True)
        QMessageBox.information(self, "Download Complete", f"Video successfully downloaded and converted:\n{final_path}")

    def download_error(self, error_message):
        self.progress_bar.setValue(0)
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")

def main():
    app = QApplication(sys.argv)
    ex = YouTubeConverterGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
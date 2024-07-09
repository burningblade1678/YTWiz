import sys
import os
import zipfile
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QProgressBar, QMessageBox, QListWidget, QCheckBox, QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

from src.downloader import download_video
from src.converter import convert_video
from src.file_manager import save_file, clean_up

class DownloadThread(QThread):
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, urls, formats, output_path):
        QThread.__init__(self)
        self.urls = urls
        self.formats = formats
        self.output_path = output_path

    def run(self):
        try:
            converted_files = []
            total_steps = len(self.urls) * (len(self.formats) + 1)
            current_step = 0

            for url in self.urls:
                try:
                    self.progress.emit(f"Downloading video: {url}...", current_step * 100 // total_steps)
                    video_path = download_video(url, self.output_path)
                    current_step += 1
                    
                    for format in self.formats:
                        try:
                            self.progress.emit(f"Converting to {format}...", current_step * 100 // total_steps)
                            converted_path = convert_video(video_path, format)
                            final_path = save_file(converted_path, os.path.basename(converted_path), self.output_path)
                            converted_files.append(final_path)
                        except Exception as e:
                            self.error.emit(f"Error converting to {format}: {str(e)}")
                        finally:
                            current_step += 1
                except Exception as e:
                    self.error.emit(f"Error processing {url}: {str(e)}")
            
            if len(converted_files) > 1:
                self.progress.emit("Creating ZIP file...", 95)
                zip_path = os.path.join(self.output_path, "converted_videos.zip")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for file in converted_files:
                        zipf.write(file, os.path.basename(file))
                        os.remove(file)
                self.finished.emit(zip_path)
            elif len(converted_files) == 1:
                self.finished.emit(converted_files[0])
            else:
                self.error.emit("No files were successfully converted.")
            
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")
        finally:
            clean_up()

class YTWizGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                font-size: 14px;
            }
            QPushButton {
                background-color: #FF0000;
                color: #FFFFFF;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
            QLineEdit, QListWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
                border: 1px solid #FF0000;
                padding: 5px;
                border-radius: 4px;
            }
            QProgressBar {
                border: 2px solid #FF0000;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #FF0000;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QGroupBox {
                border: 1px solid #FF0000;
                border-radius: 4px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)

        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel(self)
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wizard_tube_logo.jpg")
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaledToWidth(200, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        else:
            print(f"Failed to load logo from: {logo_path}")

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        self.add_url_button = QPushButton("Add")
        self.add_url_button.clicked.connect(self.add_url)
        url_layout.addWidget(self.add_url_button)
        layout.addLayout(url_layout)

        # URL list
        self.url_list = QListWidget()
        layout.addWidget(self.url_list)

        # Format selection
        format_group = QGroupBox("Output Formats")
        format_layout = QVBoxLayout()
        self.format_checkboxes = []
        for format in ["mp3", "wav", "ogg"]:  # Removed 'aac'
            checkbox = QCheckBox(format)
            self.format_checkboxes.append(checkbox)
            format_layout.addWidget(checkbox)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

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

        # Scroll area for responsiveness
        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.setWindowTitle("YTWiz")
        self.setGeometry(100, 100, 1024, 768)
        
        # Set window icon
        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

    def add_url(self):
        url = self.url_input.text()
        if url:
            self.url_list.addItem(url)
            self.url_input.clear()

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path.setText(folder)

    def start_download(self):
        urls = [self.url_list.item(i).text() for i in range(self.url_list.count())]
        formats = [cb.text() for cb in self.format_checkboxes if cb.isChecked()]
        output_path = self.output_path.text()

        if not urls or not formats or not output_path:
            QMessageBox.warning(self, "Input Error", "Please enter at least one URL, select at least one format, and choose an output location.")
            return

        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)

        self.thread = DownloadThread(urls, formats, output_path)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.download_finished)
        self.thread.error.connect(self.download_error)
        self.thread.start()

    def update_progress(self, message, value):
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"{message} {value}%")

    def download_finished(self, final_path):
        self.progress_bar.setValue(100)
        self.download_button.setEnabled(True)
        self.url_list.clear()
        for checkbox in self.format_checkboxes:
            checkbox.setChecked(False)
        QMessageBox.information(self, "Download Complete", f"Videos successfully downloaded and converted:\n{final_path}")
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("")

    def download_error(self, error_message):
        self.progress_bar.setValue(0)
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_message}")
        print(f"Detailed error: {error_message}")  # This will print the full error to the console
        
        # Log the error to a file
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {error_message}\n")

def main():
    app = QApplication(sys.argv)
    
    # Set the application icon
    app_icon = QIcon("wizard_tube_logo.jpg")
    app.setWindowIcon(app_icon)
    
    # Enable custom window frame
    app.setStyle("Fusion")
    
    # Set the taskbar icon (Windows specific)
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    ex = YTWizGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
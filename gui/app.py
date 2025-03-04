# gui/app.py

__all__ = ["run_app"]

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QRadioButton, QFileDialog, QProgressBar, QTextEdit, QComboBox
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer

# Language mapping: language name -> language code
LANGUAGE_MAPPING = {
    'afrikaans': 'af',
    'albanian': 'sq',
    'amharic': 'am',
    'arabic': 'ar',
    'armenian': 'hy',
    'azerbaijani': 'az',
    'basque': 'eu',
    'belarusian': 'be',
    'bengali': 'bn',
    'bosnian': 'bs',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cebuano': 'ceb',
    'chichewa': 'ny',
    'chinese (simplified)': 'zh-cn',
    'chinese (traditional)': 'zh-tw',
    'corsican': 'co',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'filipino': 'tl',
    'finnish': 'fi',
    'french': 'fr',
    'frisian': 'fy',
    'galician': 'gl',
    'georgian': 'ka',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'haitian creole': 'ht',
    'hausa': 'ha',
    'hawaiian': 'haw',
    'hebrew': 'he',
    'hindi': 'hi',
    'hmong': 'hmn',
    'hungarian': 'hu',
    'icelandic': 'is',
    'igbo': 'ig',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jw',
    'kannada': 'kn',
    'kazakh': 'kk',
    'khmer': 'km',
    'korean': 'ko',
    'kurdish (kurmanji)': 'ku',
    'kyrgyz': 'ky',
    'lao': 'lo',
    'latin': 'la',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'luxembourgish': 'lb',
    'macedonian': 'mk',
    'malagasy': 'mg',
    'malay': 'ms',
    'malayalam': 'ml',
    'maltese': 'mt',
    'maori': 'mi',
    'marathi': 'mr',
    'mongolian': 'mn',
    'myanmar (burmese)': 'my',
    'nepali': 'ne',
    'norwegian': 'no',
    'odia': 'or',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'punjabi': 'pa',
    'romanian': 'ro',
    'russian': 'ru',
    'samoan': 'sm',
    'scots gaelic': 'gd',
    'serbian': 'sr',
    'sesotho': 'st',
    'shona': 'sn',
    'sindhi': 'sd',
    'sinhala': 'si',
    'slovak': 'sk',
    'slovenian': 'sl',
    'somali': 'so',
    'spanish': 'es',
    'sundanese': 'su',
    'swahili': 'sw',
    'swedish': 'sv',
    'tajik': 'tg',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'uyghur': 'ug',
    'uzbek': 'uz',
    'vietnamese': 'vi',
    'welsh': 'cy',
    'xhosa': 'xh',
    'yiddish': 'yi',
    'yoruba': 'yo',
    'zulu': 'zu'
}

# Worker thread for processing files without blocking the UI.
class WorkerThread(QThread):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal()

    def __init__(self, files, mode, target_language, parent=None):
        super().__init__(parent)
        self.files = files
        self.mode = mode
        self.target_language = target_language

    def run(self):
        total = len(self.files)
        for idx, file in enumerate(self.files, start=1):
            self.status_signal.emit(f"Processing file {idx}/{total}: {os.path.basename(file)}")
            try:
                if self.mode == "Videos":
                    from processors.video_processor import process_single_video
                    process_single_video(file, target_language=self.target_language)
                else:
                    from processors.document_processor import process_single_document
                    process_single_document(file, target_language=self.target_language)
                self.status_signal.emit(f"Finished processing: {os.path.basename(file)}")
            except Exception as e:
                self.status_signal.emit(f"Error processing {os.path.basename(file)}: {str(e)}")
        self.status_signal.emit("All files processed successfully.")
        self.finished_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Global Classroom")
        self.resize(700, 600)
        self.setStyleSheet("background-color: #FFFFFF;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header with the app name
        header_label = QLabel("Global Classroom")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #0A3D62; font: bold 36px 'Segoe UI';")
        layout.addWidget(header_label)

        # Description label
        description_label = QLabel("Translate your educational videos and documents into multiple languages quickly and easily for a global audience.")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("color: #0A3D62; font: 18px 'Segoe UI';")
        layout.addWidget(description_label)

        # Translation type selection layout
        type_layout = QHBoxLayout()
        type_label = QLabel("Select Translation Type:")
        type_label.setStyleSheet("color: #0A3D62; font: 18px 'Segoe UI';")
        type_layout.addWidget(type_label)

        self.video_radio = QRadioButton("Video")
        self.video_radio.setStyleSheet("""
            QRadioButton {
                background-color: #CCCCCC;
                color: #0A3D62;
                font: 16px 'Segoe UI';
                padding: 6px;
                border-radius: 4px;
            }
            QRadioButton::hover {
                background-color: #BBBBBB;
            }
        """)
        self.video_radio.setChecked(True)
        self.document_radio = QRadioButton("Document")
        self.document_radio.setStyleSheet("""
            QRadioButton {
                background-color: #CCCCCC;
                color: #0A3D62;
                font: 16px 'Segoe UI';
                padding: 6px;
                border-radius: 4px;
            }
            QRadioButton::hover {
                background-color: #BBBBBB;
            }
        """)
        type_layout.addWidget(self.video_radio)
        type_layout.addWidget(self.document_radio)
        layout.addLayout(type_layout)

        # Language selection layout
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Select Target Language:")
        lang_label.setStyleSheet("color: #0A3D62; font: 18px 'Segoe UI';")
        lang_layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.setStyleSheet(
            "background-color: #FFFFFF; color: #0A3D62; font: 16px 'Segoe UI';"
            "border: 1px solid #38ADA9; padding: 4px;"
        )
        languages = list(LANGUAGE_MAPPING.keys())
        self.lang_combo.addItems(languages)
        default_index = languages.index("nepali") if "nepali" in languages else 0
        self.lang_combo.setCurrentIndex(default_index)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # File selection layout
        file_layout = QHBoxLayout()
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #38ADA9;
                color: #FFFFFF;
                font: 16px 'Segoe UI';
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2F8B80;
            }
        """)
        self.browse_button.clicked.connect(self.browse_files)
        file_layout.addWidget(self.browse_button)

        self.files_label = QLabel("No files selected")
        self.files_label.setStyleSheet("color: #0A3D62; font: 16px 'Segoe UI';")
        file_layout.addWidget(self.files_label)
        layout.addLayout(file_layout)

        # Translate button
        self.translate_button = QPushButton("Translate")
        self.translate_button.setStyleSheet("""
            QPushButton {
                background-color: #38ADA9;
                color: #FFFFFF;
                font: bold 18px 'Segoe UI';
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2F8B80;
            }
        """)
        self.translate_button.clicked.connect(self.start_translation)
        layout.addWidget(self.translate_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #38ADA9;
                border-radius: 5px;
                text-align: center;
                color: #0A3D62;
                background-color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #F6B93B;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Status messages text area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet(
            "background-color: #FFFFFF; color: #0A3D62; font: 16px 'Segoe UI';"
            "border: 1px solid #38ADA9;"
        )
        layout.addWidget(self.status_text)

        self.selected_files = []
        
        # QTimer for simulated progress updates.
        self.fake_progress = 0
        self.timer = QTimer(self)
        self.timer.setInterval(200)  # update every 200 ms
        self.timer.timeout.connect(self.update_fake_progress)
        # We'll calculate a tick increment based on expected processing time.
        self.tick_increment = 0

    def update_fake_progress(self):
        if self.fake_progress < 95:
            self.fake_progress += self.tick_increment
            self.progress_bar.setValue(int(self.fake_progress))

    def browse_files(self):
        mode = "Videos" if self.video_radio.isChecked() else "Documents"
        file_filter = "Video Files (*.mp4 *.mkv *.avi *.mov *.flv *.wmv)" if mode == "Videos" else "Word Documents (*.docx)"
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", file_filter)
        if files:
            self.selected_files = files
            self.files_label.setText(f"{len(files)} file(s) selected")
        else:
            self.selected_files = []
            self.files_label.setText("No files selected")

    def start_translation(self):
        if not self.selected_files:
            self.append_status("Please select one or more files.")
            return
        self.translate_button.setEnabled(False)
        self.fake_progress = 0
        self.progress_bar.setValue(0)
        
        # Calculate expected processing time:
        # Assuming 10 minutes (600,000 ms) per file.
        expected_time_ms = 600000 * len(self.selected_files)
        # Total ticks = expected_time_ms divided by timer interval.
        total_ticks = expected_time_ms / self.timer.interval()
        # We want to reach 95% over total_ticks.
        self.tick_increment = 95 / total_ticks
        
        self.timer.start()  # Start simulated progress updates

        mode = "Videos" if self.video_radio.isChecked() else "Documents"
        lang_name = self.lang_combo.currentText()
        target_language = LANGUAGE_MAPPING.get(lang_name, "ne")
        self.worker = WorkerThread(self.selected_files, mode, target_language)
        self.worker.progress_signal.connect(lambda x: None)  # Ignored in favor of fake progress.
        self.worker.status_signal.connect(self.append_status)
        self.worker.finished_signal.connect(self.translation_finished)
        self.worker.start()

    def translation_finished(self):
        self.timer.stop()  # Stop the timer once processing is complete.
        self.progress_bar.setValue(100)
        self.translate_button.setEnabled(True)
        self.append_status("Translation complete!")

    def append_status(self, message):
        self.status_text.append(message)

def run_app():
    """Function to run the PySide6 application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()

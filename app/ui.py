import os

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QFileDialog,
    QMessageBox, QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from .wipe import wipe_files
from .verifier import generate_certificate
from .utils import is_safe_path

CERTIFICATE_PATH = os.path.expanduser("~/wipe_certificate.json")


class SecureWipeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Wipe Tool")
        self.setGeometry(300, 150, 500, 300)

        # ✅ Minimalist background + font
        self.setStyleSheet("""
    background-color: #2F3E46;
    font-size: 12px;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #FFFFFF;
    padding: 12px;
    border-radius: 6px;
    letter-spacing : 1px;
""")


        self.selected_paths = []

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Label
        self.label = QLabel("SELECT FILES/FOLDERS TO SECURELY WIPE")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Buttons
        button_layout = QHBoxLayout()

        self.select_btn = QPushButton("SELECT FILE/FOLDERS")
        self.select_btn.setStyleSheet("""
    background-color: #52796F;
    font-size: 11px;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #FFFFFF;
    padding: 16px;
    border-radius: 6px;
""")

        self.select_btn.clicked.connect(self.select_files)
        button_layout.addWidget(self.select_btn)

        self.wipe_btn = QPushButton("START WIPE")
        self.wipe_btn.setStyleSheet("""
    background-color: #52796F;
    font-size: 11px;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #FFFFFF;
    padding: 16px;
    border-radius: 6px;
""")

        self.wipe_btn.setEnabled(False)
        self.wipe_btn.clicked.connect(self.start_wipe)
        button_layout.addWidget(self.wipe_btn)

        layout.addLayout(button_layout)

        # Certificate + clear buttons
        action_layout = QHBoxLayout()

        self.cert_btn = QPushButton("OPEN CERTIFICATE")
        self.cert_btn.setStyleSheet("""
    background-color: #52796F;
    font-size: 11px;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #FFFFFF;
    padding: 16px;
    border-radius: 6px;
    hover::{}
""")

        self.cert_btn.clicked.connect(self.open_certificate)
        action_layout.addWidget(self.cert_btn)

        self.clear_btn = QPushButton("CLEAR SELECTION")
        self.clear_btn.setStyleSheet("""
    background-color: #52796F;
    font-size: 11px;
    font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #FFFFFF;
    padding: 16px;
    border-radius: 6px;
""")

        self.clear_btn.clicked.connect(self.clear_selection)
        action_layout.addWidget(self.clear_btn)

        layout.addLayout(action_layout)
        central.setLayout(layout)

    def select_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Files or Folders")
        if not paths:
            path = QFileDialog.getExistingDirectory(self, "Select Folder")
            if path:
                paths = [path]
        if paths:
            safe_paths = [p for p in paths if is_safe_path(p)]
            if not safe_paths:
                QMessageBox.critical(self, "Error", "No valid files/folders selected.")
                return
            self.selected_paths = safe_paths
            self.wipe_btn.setEnabled(True)
            QMessageBox.information(self, "Selected", f"{len(self.selected_paths)} files/folders selected.")

    def start_wipe(self):
        if not self.selected_paths:
            QMessageBox.warning(self, "Warning", "No files selected.")
            return
        for path in self.selected_paths:
            wipe_files(path)
        cert_path = generate_certificate(self.selected_paths, parent=self)
        global CERTIFICATE_PATH
        CERTIFICATE_PATH = cert_path
        QMessageBox.information(self, "Success", f"Wipe completed!\nCertificate: {cert_path}")
        self.selected_paths = []
        self.wipe_btn.setEnabled(False)

    def open_certificate(self):
        if os.path.exists(CERTIFICATE_PATH):
            try:
                if os.name == "nt":
                    os.startfile(CERTIFICATE_PATH)
                elif os.name == "posix":
                    os.system(f"xdg-open '{CERTIFICATE_PATH}'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot open certificate: {e}")
        else:
            QMessageBox.information(self, "Not Found", "No certificate found yet!")

    def clear_selection(self):
        self.selected_paths = []
        self.wipe_btn.setEnabled(False)
        QMessageBox.information(self, "Cleared", "Selection cleared.")

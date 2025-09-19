from .ui import SecureWipeUI
from PyQt5.QtWidgets import QApplication

def main():
    import sys
    app = QApplication(sys.argv)
    window = SecureWipeUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

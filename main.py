import sys
from PyQt5.QtWidgets import QApplication

from abilities.interface import LogWindow


def main():
    app = QApplication(sys.argv)
    log_window = LogWindow()
    log_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

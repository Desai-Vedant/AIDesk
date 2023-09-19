#Import Required Libraries
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QIcon, QColor, QPainter, QPainterPath, QBrush
from PyQt5.QtCore import Qt, QPoint, QRectF, QSize, QThread, pyqtSignal, QObject
from functions import Assistant

#Assistant Widget Class
class AssistantWidget(QWidget):

    mic_activated = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.drag_position = QPoint()
        self.is_listening = False

        self.microphone_button = QPushButton(self)
        self.microphone_button.setIcon(QIcon("microphone_icon.png"))
        self.microphone_button.setIconSize(QSize(30,30))
        self.microphone_button.clicked.connect(self.start_listen_thread)
        self.set_button_stylesheet()

        layout.addWidget(self.microphone_button, alignment=Qt.AlignCenter)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.listening_thread = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def set_button_stylesheet(self):
        style = '''
            QPushButton {{
                background-color: {bg_color};
                border: none;
                padding: {padding}px;
                color: #ffffff;
                border-radius: {radius}px;
            }}

            QPushButton:checked {{
                background-color: {bg_color};
                border: none;
            }}

            QPushButton:hover {{
                border: 2px solid {hover_color};
            }}
        '''
        if self.is_listening:
            bg_color = "#007bff"
            padding = 2
            hover_color = "#007bff"
        else:
            bg_color = "transparent"
            padding = 3
            hover_color = "#007bff"
        self.microphone_button.setStyleSheet(style.format(bg_color=bg_color, padding=padding, radius=17, hover_color=hover_color))

    def start_listening(self):
        self.is_listening = True
        self.set_button_stylesheet()

    def stop_listening(self):
        self.is_listening = False
        self.set_button_stylesheet()

    def start_listen_thread(self):
        if self.listening_thread is None or not self.listening_thread.isRunning():
            self.listening_thread = ListeningThread()
            self.listening_thread.finished.connect(self.stop_listening)
            self.listening_thread.start()
            self.start_listening()
            self.mic_activated.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect().adjusted(2, 2, -2, -2))
        path = QPainterPath()
        path.addRoundedRect(rect, 36, 36)

        painter.fillPath(path, QBrush(Qt.white))

        painter.setPen(QColor("#000000"))
        painter.drawPath(path)

#Listening Thread Class
class ListeningThread(QThread):
    def run(self):
        assistant = Assistant()
        assistant.run()

#Searching Thread Class
class SearchingThread(QThread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.assistant = Assistant()

    def run(self):
        self.assistant.print_query(self.command)
        self.assistant.decide_action(self.command)

#Output Window Class
class OutputWindow(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def appendText(self, text):
        self.append(text)
        self.ensureCursorVisible()

#Main Window Class
class AIDesk(QMainWindow):

    searching_thread = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIDesk - Desktop Assistant")
        self.setGeometry(100, 100, 800, 450)
        self.setup_ui()
        self.setStyleSheet("background-color: #d0b3ff;")

    def setup_ui(self):
        main_widget = QWidget(self)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        sidebar_widget = QWidget(self)
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sidebar_widget.setMinimumWidth(int(self.width() / 6))
        sidebar_widget.setStyleSheet(
            "QWidget { background-color: #ffffff; border: 2px solid #9e96b0 ;border-radius: 20px ; padding: 10px; margin: 5px; }"
        )
        main_layout.addWidget(sidebar_widget)

        self.launch_button = QPushButton()
        self.launch_button.setIcon(QIcon("launch_icon.png"))
        self.launch_button.setIconSize(QSize(30, 30))
        self.launch_button.setStyleSheet(
            "QPushButton { background-color: #ffffff; border-radius: 15px; border: 2px solid #9e96b0; padding: 10px; }"
            "QPushButton:hover { background-color: #e6e6e6; }"
        )

        self.microphone_button = QPushButton()
        self.microphone_button.setIcon(QIcon("microphone_icon.png"))
        self.microphone_button.setIconSize(QSize(30, 30))
        self.microphone_button.setStyleSheet(
            "QPushButton { background-color: #ffffff; border-radius: 15px; border: 2px solid #9e96b0; padding: 10px; }"
            "QPushButton:hover { background-color: #e6e6e6; }"
        )

        sidebar_layout.addWidget(self.launch_button, alignment=Qt.AlignCenter)
        sidebar_layout.addWidget(self.microphone_button, alignment=Qt.AlignCenter)

        main_window_layout = QVBoxLayout()
        main_layout.addLayout(main_window_layout)

        self.text_box = OutputWindow()
        self.text_box.setReadOnly(True)
        self.text_box.setStyleSheet(
            "QTextEdit { background-color: #ffffff; color: #333333; border-radius: 20px; border: 2px solid #9e96b0; margin: 5px; padding: 10px }"
        )
        main_window_layout.addWidget(self.text_box)

        input_layout = QHBoxLayout()
        main_window_layout.addLayout(input_layout)

        self.text_input = QLineEdit()
        self.text_input.setStyleSheet(
            "QLineEdit { background-color: #ffffff; color: #333333; border-radius: 20px; padding: 20px; border: 2px solid #9e96b0; margin : 5px}"
        )
        self.text_input.returnPressed.connect(self.search_button_clicked)

        search_button = QPushButton("Search")
        search_button.setStyleSheet(
            "QPushButton { background-color: #007bff; border-radius: 20px; border: none; color: #ffffff; padding: 20px; border: 2px solid #9e96b0; margin : 5px }"
            "QPushButton:hover { background-color: #0056b3; }"
        )

        input_layout.addWidget(self.text_input)
        input_layout.addWidget(search_button)

        self.launch_button.clicked.connect(self.launch_button_clicked)
        self.microphone_button.clicked.connect(self.microphone_button_clicked)
        search_button.clicked.connect(self.search_button_clicked)
        self.resizeEvent = self.on_resize

        self.assistant_widget = AssistantWidget()
        self.assistant_widget.setVisible(False)
        self.assistant_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.assistant_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.assistant_widget.mic_activated.connect(self.microphone_button_clicked)

        sys.stdout = OutputWrapper(self.text_box)

        output_wrapper = sys.stdout
        output_wrapper.textWritten.connect(self.text_box.appendText)

        self.destroyed.connect(self.assistant_widget.close)

    def on_resize(self, event):
        self.update_sidebar_width()

    def update_sidebar_width(self):
        sidebar_widget = self.centralWidget().layout().itemAt(0).widget()
        sidebar_width = int(self.width() / 6)
        sidebar_widget.setMinimumWidth(sidebar_width)

        initial_button_width = 30
        initial_sidebar_width = 800 / 6
        button_width = int((sidebar_width / initial_sidebar_width) * initial_button_width)

        icon_size = QSize(button_width, button_width)
        self.launch_button.setIconSize(icon_size)
        self.microphone_button.setIconSize(icon_size)

    def start_search_thread(self, command):
        if self.searching_thread is None or not self.searching_thread.isRunning():
            self.searching_thread = SearchingThread(command)
            self.searching_thread.start()
            self.text_input.clear()

    def launch_button_clicked(self):
        if self.assistant_widget.isVisible():
            self.assistant_widget.setVisible(False)
            self.launch_button.setIcon(QIcon("launch_icon.png"))
            self.launch_button.setIconSize(QSize(30, 30))
            self.launch_button.setStyleSheet(
                "QPushButton { background-color: #ffffff; border-radius: 15px; border: 2px solid #9e96b0; padding: 10px; }"
                "QPushButton:hover { background-color: #e6e6e6; }"
            )
            self.update_sidebar_width()
        else:
            self.assistant_widget.setVisible(True)
            self.launch_button.setIcon(QIcon("close_icon.png"))
            self.launch_button.setIconSize(QSize(30, 30))
            self.launch_button.setStyleSheet(
                "QPushButton { background-color: #726eff; border-radius: 15px; border: 2px solid #9e96b0; padding: 10px; }"
                "QPushButton:hover { background-color: #5c57ff; }"
            )
            self.update_sidebar_width()

    def microphone_button_clicked(self):
        self.assistant_widget.start_listen_thread()
        self.assistant_widget.listening_thread.started.connect(lambda: self.microphone_button.setStyleSheet(
            "QPushButton { background-color: #726eff; border-radius: 15px; border: 2px solid #9e96b0; padding: 10px; }"
            "QPushButton:hover { background-color: #5c57ff; }"
        ))

        self.assistant_widget.listening_thread.finished.connect(lambda: self.microphone_button.setStyleSheet(
            "QPushButton { background-color: #ffffff; border-radius: 15px; border: 2px solid #9e96b0; padding: 10px; }"
            "QPushButton:hover { background-color: #e6e6e6; }"
        ))

    def search_button_clicked(self):
        command = self.text_input.text()
        if command:
            self.start_search_thread(command)

#Output Wrapper Class
class OutputWrapper(QObject):
    textWritten = pyqtSignal(str)

    def __init__(self, output_widget):
        super().__init__()
        self.output_widget = output_widget

    def write(self, text):
        self.textWritten.emit(text)

    def flush(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIDesk()
    window.show()
    sys.exit(app.exec())

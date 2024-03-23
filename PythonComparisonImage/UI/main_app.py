from PyQt5.QtWidgets import QMainWindow, QTabWidget, QStatusBar, QVBoxLayout

import UI.image_comparison_tab as comparison_tab


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Application")
        self.resize(self.screen().size())

        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        settings_menu = menubar.addMenu("Настройки")
        help_menu = menubar.addMenu("Помощь")

        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        image_comparison_tab = comparison_tab.ImageComparisonTab()
        tab_widget.addTab(image_comparison_tab, "Тестирование алгоритмов")
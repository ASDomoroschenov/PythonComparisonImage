import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QToolBar, QComboBox, QAction, QLabel, QVBoxLayout, \
    QWidget, QFrame, QAbstractItemView, QTableWidget, QTableWidgetItem, QScrollArea

import src.open_cv.image_hash as image_hash
import src.open_cv.ncc as ncc
import src.open_cv.sift as sift
import src.open_cv.ssim as ssim


class ImageComparisonTab(QWidget):
    def __init__(self):
        super().__init__()

        toolbar = QToolBar()
        toolbar.setFixedHeight(50)

        action_load_source = QAction("Загрузить исходное изображение", self)
        action_load_comparison = QAction("Загрузить изображение для сравнения", self)
        action_show_result = QAction("Показать результат", self)

        algorithm_menu = QComboBox()
        algorithm_menu.addItems([
            "NCC",
            "SSIM",
            "SIFT",
            "Hash"
        ])
        toolbar.addSeparator()
        toolbar.addAction(action_load_source)
        toolbar.addSeparator()
        toolbar.addAction(action_load_comparison)
        toolbar.addSeparator()
        toolbar.addWidget(algorithm_menu)
        toolbar.addSeparator()
        toolbar.addAction(action_show_result)
        toolbar.addSeparator()

        action_load_source.triggered.connect(self.load_source_image)
        action_load_comparison.triggered.connect(self.load_comparison_image)
        action_show_result.triggered.connect(self.show_result)
        algorithm_menu.currentIndexChanged.connect(self.select_algorithm)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        layout.addWidget(self.result_label)

        self.status_bar = QTableWidget(1, 6)
        self.status_bar.setFixedHeight(37)
        self.status_bar.horizontalHeader().setVisible(False)
        self.status_bar.verticalHeader().setVisible(False)
        self.status_bar.setShowGrid(False)
        self.status_bar.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.status_bar.setStyleSheet(
            """
            QTableWidget {
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            QTableWidget::item {
                border: 1px solid #ccc;
                padding: 5px;
                background-color: #fff;
            }
            """
        )
        self.status_bar.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.status_bar.setSelectionMode(QAbstractItemView.NoSelection)
        self.status_bar.setFixedWidth(1890)
        column_width = int(self.status_bar.width() / 6)
        for i in range(6):
            self.status_bar.setColumnWidth(i, column_width)

        layout.addWidget(self.status_bar)
        self.setLayout(layout)

        self.source_path = ""
        self.comparison_path = ""
        self.selected_algorithm = "NCC"

    def load_source_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.bmp *.jpeg)", options=options)
        if file_name:
            self.source_path = file_name
            print("Selected Source File:", file_name)

    def load_comparison_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.bmp *.jpeg)", options=options)
        if file_name:
            self.comparison_path = file_name
            print("Selected Comparison File:", file_name)

    def select_algorithm(self, index):
        algorithms = [
            "NCC",
            "SSIM",
            "SIFT",
            "Hash"
        ]
        self.selected_algorithm = algorithms[index]
        print("Selected Algorithm:", self.selected_algorithm)

    def show_result(self):
        if self.source_path and self.comparison_path:
            try:
                if self.selected_algorithm == "NCC":
                    result_path = ncc.show_difference(self.source_path, self.comparison_path)
                elif self.selected_algorithm == "SSIM":
                    result_path = ssim.show_difference(self.source_path, self.comparison_path)
                else:
                    result_path = sift.show_difference(self.source_path, self.comparison_path)

                if self.selected_algorithm != "Hash":
                    pixmap = QPixmap(result_path)
                    new_width = int(self.result_label.width() * 0.7)
                    new_height = int(self.result_label.height() * 0.7)
                    pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)

                    self.result_label.setPixmap(pixmap)

                hash1 = self.calculate_hash(self.source_path)
                hash2 = self.calculate_hash(self.comparison_path)
                self.update_status_bar([np.abs(hash1[i] - hash2[i]) for i in range(len(hash1))])
            except Exception as e:
                print("Error loading image:", e)

    def calculate_hash(self, image_path):
        return [image_hash.average_hash(image_path),
                image_hash.perceptual_hash(image_path),
                image_hash.difference_hash(image_path),
                image_hash.wavelet_hash(image_path),
                image_hash.color_hash(image_path),
                image_hash.crop_resistant_hash(image_path)]

    def update_status_bar(self, differences):
        hash_names = [
            "average_hash",
            "perceptual_hash",
            "difference_hash",
            "wavelet_hash",
            "color_hash",
            "crop_resistant_hash"
        ]
        for i in range(len(differences)):
            item = QTableWidgetItem(f"{hash_names[i]}: {differences[i]}")
            item.setTextAlignment(Qt.AlignCenter)
            self.status_bar.setItem(0, i, item)



import os

import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog,
                             QMessageBox, QComboBox)

import src.open_cv.ncc as ncc
import src.open_cv.sift as sift
import src.open_cv.ssim as ssim
import src.open_cv.image_hash as image_hash


class ImageClassificationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.patternsList = None
        self.originalsList = None
        self.patternsLayout = None
        self.originalsLayout = None
        self.layout = None
        self.algorithmSelector = None
        self.originalImages = []
        self.patterns = {}
        self.selectedAlgorithm = 'NCC'
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()

        self.originalsLayout = QVBoxLayout()
        self.patternsLayout = QVBoxLayout()

        self.originalsList = QListWidget()
        self.patternsList = QListWidget()

        self.originalsList.clicked.connect(self.onOriginalClicked)

        addOriginalBtn = QPushButton("+")
        addOriginalBtn.setFixedSize(30, 30)
        addOriginalBtn.clicked.connect(self.addOriginalImage)

        originalsHeaderLayout = QHBoxLayout()
        originalsHeaderLayout.addWidget(QLabel("Оригиналы"))
        originalsHeaderLayout.addWidget(addOriginalBtn)
        originalsHeaderLayout.addStretch()

        addPatternBtn = QPushButton("+")
        addPatternBtn.setFixedSize(30, 30)

        self.algorithmSelector = QComboBox()
        self.algorithmSelector.addItems(['NCC', 'SSIM', 'SIFT', 'Hash'])
        self.algorithmSelector.currentTextChanged.connect(self.algorithmChanged)
        self.algorithmSelector.setFixedWidth(100)

        patternsHeaderLayout = QHBoxLayout()
        patternsHeaderLayout.addWidget(QLabel("Паттерны"))
        patternsHeaderLayout.addWidget(addPatternBtn)
        patternsHeaderLayout.addWidget(self.algorithmSelector)
        patternsHeaderLayout.addStretch()

        addPatternBtn.clicked.connect(self.addPatternImage)

        self.originalsLayout.addLayout(originalsHeaderLayout)
        self.originalsLayout.addWidget(self.originalsList)

        self.patternsLayout.addLayout(patternsHeaderLayout)
        self.patternsLayout.addWidget(self.patternsList)

        self.layout.addLayout(self.originalsLayout)
        self.layout.addLayout(self.patternsLayout)

        self.setLayout(self.layout)

    def addOriginalImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fileName:
            relativePath = os.path.relpath(fileName)
            self.originalImages.append(relativePath)
            self.originalsList.addItem(relativePath)
            self.patterns[relativePath] = []

    def onOriginalClicked(self):
        self.patternsList.clear()
        currentItem = self.originalsList.currentItem()
        if currentItem:
            patterns = self.patterns.get(currentItem.text(), [])
            self.patternsList.addItems(patterns)

    def addPatternImage(self):
        currentItem = self.originalsList.currentItem()
        if not currentItem:
            QMessageBox.warning(self, "Внимание", "Сначала выберите оригинальное изображение.")
            return
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите паттерн", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fileName:
            relativePath = os.path.relpath(fileName)
            patternValue = self.calculatePatternValue(currentItem.text(), relativePath)
            patternLabel = f"{relativePath} - {patternValue:.2f}"
            patterns = self.patterns.get(currentItem.text(), [])
            self.patterns[currentItem.text()].append(patternLabel)
            patterns.sort(key=lambda x: float(x.split(' - ')[1]), reverse=True)
            self.patterns[currentItem.text()] = patterns
            self.updatePatternListDisplay()

    def algorithmChanged(self, value):
        self.selectedAlgorithm = value
        self.recalculatePatterns()

    def calculatePatternValue(self, originalImage, patternPath):
        originalImageItem = cv.imread(originalImage)
        originalHeight, originalWidth = originalImageItem.shape[:2]
        patternItem = cv.imread(patternPath)
        patternHeight, patternWidth = patternItem.shape[:2]

        if self.selectedAlgorithm == 'NCC':
            if originalWidth >= patternWidth and originalHeight >= patternHeight:
                return ncc.match(originalImageItem, patternItem)
            else:
                return 0
        elif self.selectedAlgorithm == 'SIFT':
            return sift.match(originalImageItem, patternItem)
        elif self.selectedAlgorithm == 'SSIM':
            if originalWidth == patternWidth and originalHeight == patternHeight:
                return ssim.match(originalImageItem, patternItem)
            else:
                return 0
        elif self.selectedAlgorithm == 'Hash':
            a_hash = np.abs(image_hash.average_hash(originalImage) - image_hash.average_hash(patternPath))
            p_hash = np.abs(image_hash.perceptual_hash(originalImage) - image_hash.perceptual_hash(patternPath))
            d_hash = np.abs(image_hash.difference_hash(originalImage) - image_hash.difference_hash(patternPath))
            w_hash = np.abs(image_hash.wavelet_hash(originalImage) - image_hash.wavelet_hash(patternPath))
            c_hash = np.abs(image_hash.color_hash(originalImage) - image_hash.color_hash(patternPath))
            cr_hash = np.abs(image_hash.crop_resistant_hash(originalImage) - image_hash.crop_resistant_hash(patternPath))
            return np.mean([a_hash, p_hash, d_hash, w_hash, c_hash, cr_hash])
        else:
            raise ValueError("Неподдерживаемый алгоритм")

    def recalculatePatterns(self):
        for originalImagePath, patterns in self.patterns.items():
            updatedPatterns = []
            for patternPath in patterns:
                pattern = patternPath.split(' - ')[0]
                patternValue = self.calculatePatternValue(originalImagePath, pattern)
                updatedPatterns.append((pattern, patternValue))
            updatedPatterns.sort(key=lambda x: x[1], reverse=True)
            self.patterns[originalImagePath] = [f"{pattern} - {patternValue:.2f}" for pattern, patternValue in
                                                updatedPatterns]

        self.updatePatternListDisplay()

    def updatePatternListDisplay(self):
        self.patternsList.clear()
        currentItem = self.originalsList.currentItem()
        if currentItem:
            patterns = self.patterns.get(currentItem.text(), [])
            self.patternsList.addItems(patterns)

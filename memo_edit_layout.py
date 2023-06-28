from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QTableWidget, QListWidget, QListWidgetItem,
        QLineEdit, QFormLayout,
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QSpinBox)
from memo_app import app


text_Question = QLineEdit("")
text_Answer = QLineEdit("")
text_Wrong1 = QLineEdit("")
text_Wrong2 = QLineEdit("")
text_Wrong3 = QLineEdit("")
layout_form = QFormLayout()

layout_form.addRow("Запитання", text_Question)
layout_form.addRow("Правильна відповідь", text_Answer)
layout_form.addRow("Неправильна відповідь1", text_Wrong1)
layout_form.addRow("Неправильна відповідь2", text_Wrong2)
layout_form.addRow("Неправильна відповідь3", text_Wrong3)

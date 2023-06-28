from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QTableWidget, QListView, QListWidgetItem,
        QLineEdit, QFormLayout,
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QSpinBox)
from memo_app import app 
from memo_edit_layout import layout_form  
from memo_card_layout import layout_card



list_Questions = QListView()
wdgt_edit = QWidget()

wdgt_edit.setLayout(layout_form)

btn_add = QPushButton("Нове запитання: ")
btn_delete = QPushButton("Видалити запитання")
btn_start = QPushButton("Почати тренування")

main_col1 = QVBoxLayout()
main_col1.addWidget(list_Questions)
main_col1.addWidget(btn_add)

main_col2 = QVBoxLayout()
main_col2.addWidget(wdgt_edit)
main_col2.addWidget(btn_delete)

mail_line = QHBoxLayout()
mail_line.addLayout(main_col1)
mail_line.addLayout(main_col2)

mail_line2 = QHBoxLayout()
mail_line2.addWidget(btn_start)

layout_main = QVBoxLayout() 
layout_main.addLayout(mail_line) 
layout_main.addLayout(mail_line2)
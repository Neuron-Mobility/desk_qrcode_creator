from threading import Thread

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QIntValidator
import random

from src.RunThread import RunThread
from src.ebike_creator import create_e_bike_qr_codes
from src.n3_scooter_creator import create_n3_scooter_qr_codes


class RootWindow(object):
    batch_array = []
    qr_code_array = []
    create_type = "N3-Scooter"
    creating = False
    thread = None

    width = 920
    height = 640
    padding = 20

    left_box_right = int((width - 40) / 2) - 100
    left_box_bottom = height - 40

    def setup_ui(self, Dialog):
        Dialog.setObjectName("RootWindow")
        Dialog.resize(self.width, self.height)

        self.set_step1_ui(Dialog)
        self.set_step_2_ui(Dialog)

        Dialog.setWindowTitle("Neuron QRCode Creator")
        Dialog.setWindowIcon(QIcon('../static/logo_small.png'))

        Dialog.setFixedSize(Dialog.width(), Dialog.height())
        Dialog.setMaximumSize(QtCore.QSize(Dialog.width(), Dialog.height()))

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def set_step1_ui(self, Dialog):
        self.qr_codes_edit = QtWidgets.QTextEdit(Dialog)
        self.qr_codes_edit.setGeometry(
            QtCore.QRect(self.padding, self.padding, self.left_box_right, self.left_box_bottom))
        self.qr_codes_edit.setObjectName("qrCodesEdit")
        self.qr_codes_edit.setFont(QFont('Arial', 18))

        step1_box = QtWidgets.QGroupBox(Dialog)
        step1_box.setGeometry(QtCore.QRect(self.left_box_right + self.padding * 2,
                                           self.padding,
                                           self.width - self.left_box_right - self.padding * 3,
                                           int(self.height / 2 - self.padding * 2)
                                           ))
        step1_box.setObjectName("step1_box")
        step1_box.setTitle('步骤一')

        row1_left = 20
        row2_left = 20

        prefix_label = QtWidgets.QLabel(step1_box)
        prefix_label.setGeometry(QtCore.QRect(row1_left, 26, 100, 32))
        prefix_label.setObjectName("prefix_label")
        prefix_label.setFont(QFont('Arial', 16))
        prefix_label.setText("二维码前缀：")
        row1_left += 100

        self.prefix_edit = QtWidgets.QLineEdit(step1_box)
        self.prefix_edit.setPlaceholderText("51150")
        self.prefix_edit.setGeometry(QtCore.QRect(row1_left, 26, 80, 30))
        self.prefix_edit.setObjectName("prefixEdit")
        self.prefix_edit.setAlignment(QtCore.Qt.AlignRight)
        self.prefix_edit.setFont(QFont('Arial', 16))
        self.prefix_edit.setMaxLength(5)
        self.prefix_edit.setValidator(QIntValidator(1, 99999))
        self.prefix_edit.textChanged.connect(self.change_generate_btn_status)
        row1_left += 80

        count_label = QtWidgets.QLabel(step1_box)
        count_label.setGeometry(QtCore.QRect(row1_left + 100, 26, 50, 32))
        count_label.setObjectName("count_label")
        count_label.setFont(QFont('Arial', 16))
        count_label.setText("数量：")
        row1_left += 100 + 50

        self.count_edit = QtWidgets.QLineEdit(step1_box)
        self.count_edit.setPlaceholderText("500")
        self.count_edit.setGeometry(QtCore.QRect(row1_left, 26, 60, 30))
        self.count_edit.setObjectName("prefixEdit")
        self.count_edit.setAlignment(QtCore.Qt.AlignRight)
        self.count_edit.setFont(QFont('Arial', 16))
        self.count_edit.setMaxLength(3)
        self.count_edit.setValidator(QIntValidator(1, 999))
        self.count_edit.textChanged.connect(self.change_generate_btn_status)

        self.generate_btn = QtWidgets.QPushButton(step1_box)
        self.generate_btn.setGeometry(QtCore.QRect(row2_left, 80, 160, 34))
        self.generate_btn.setObjectName("generateBtn")
        self.generate_btn.setText("← 随机生成二维码序列")
        self.generate_btn.setStyleSheet(open("static/button.css").read())
        self.generate_btn.setDisabled(True)
        self.generate_btn.clicked.connect(self.generate_btn_clicked)
        row2_left += 160

        self.clear_btn = QtWidgets.QPushButton(step1_box)
        self.clear_btn.setGeometry(QtCore.QRect(row2_left + 20, 80, 140, 34))
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setStyleSheet(open("static/button.css").read())
        self.clear_btn.setText("清空二维码序列")
        self.clear_btn.setDisabled(True)
        self.clear_btn.clicked.connect(self.clear_btn_clicked)

        scroll_area = QtWidgets.QScrollArea(step1_box)
        scroll_area.setGeometry(QtCore.QRect(20, 130, self.width - self.left_box_right - self.padding * 5, 140))
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scroll_area")

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget.setGeometry(QtCore.QRect(0, 0, self.width - self.left_box_right - self.padding * 5, 140))
        scroll_area_widget.setObjectName("scroll_area_widget")

        self.batch_label = QtWidgets.QLabel(scroll_area_widget)
        self.batch_label.setGeometry(QtCore.QRect(20, 130, self.width - self.left_box_right - self.padding * 5, 140))
        self.batch_label.setObjectName("batch_label")
        self.batch_label.setAlignment(QtCore.Qt.AlignTop)
        self.batch_label.setWordWrap(True)
        self.batch_label.setFont(QFont('Arial', 14))
        self.batch_label.setStyleSheet("background-color: lightGray;")
        scroll_area.setWidget(self.batch_label)

    def change_generate_btn_status(self):
        if self.creating:
            self.generate_btn.setDisabled(True)
            return

        if not self.count_edit.text() or int(self.count_edit.text()) == 0 or int(self.count_edit.text()) > 999:
            self.generate_btn.setDisabled(True)
            return

        if not self.prefix_edit.text() or len(self.prefix_edit.text()) < 5:
            self.generate_btn.setDisabled(True)
            return

        self.generate_btn.setDisabled(False)

    def generate_btn_clicked(self):
        count = 0
        while count < int(self.count_edit.text()):
            rand = random.randint(1, 999)
            qr_code = self.prefix_edit.text() + str(rand).zfill(3)
            if qr_code in self.qr_code_array:
                continue
            self.qr_code_array.append(qr_code)
            count += 1
        self.qr_codes_edit.setText('\n'.join(self.qr_code_array))
        self.change_clear_btn_status()
        self.append_qr_code_array()
        self.update_batch_desc()
        self.change_create_btn_status()

    def change_clear_btn_status(self):
        if (len(self.batch_array) == 0 and len(self.qr_code_array) == 0) or self.creating:
            self.clear_btn.setDisabled(True)
            return

        self.clear_btn.setDisabled(False)

    def clear_btn_clicked(self):
        self.batch_array = []
        self.qr_code_array = []
        self.qr_codes_edit.setText('')
        self.change_clear_btn_status()
        self.update_batch_desc()
        self.change_create_btn_status()

    def append_qr_code_array(self):
        self.batch_array.append({'count': int(self.count_edit.text()), 'prefix': self.prefix_edit.text()})

    def update_batch_desc(self):
        text = ''
        for item in self.batch_array:
            text += "批次：{}, 数组：{} \n".format(item['prefix'], item['count'])

        if len(self.batch_array) > 0:
            text += "\n"

        text += "总数量：{}".format(len(self.qr_code_array))
        self.batch_label.setText(text)

    def set_step_2_ui(self, Dialog):
        step2_box = QtWidgets.QGroupBox(Dialog)
        step2_box.setGeometry(QtCore.QRect(self.left_box_right + self.padding * 2,
                                           int(self.height / 2),
                                           self.width - self.left_box_right - self.padding * 3,
                                           int(self.height / 2 - self.padding)
                                           ))
        step2_box.setObjectName("step2Box")
        step2_box.setTitle('步骤二')

        step_title_label = QtWidgets.QLabel(step2_box)
        step_title_label.setGeometry(QtCore.QRect(20, 30, 160, 30))
        step_title_label.setObjectName("step_title_label")
        step_title_label.setAlignment(QtCore.Qt.AlignTop)
        step_title_label.setWordWrap(True)
        step_title_label.setFont(QFont('Arial', 16))
        step_title_label.setText("选择生成二维码类型：")

        scooterRadioButton = QtWidgets.QRadioButton(step2_box)
        scooterRadioButton.setGeometry(QtCore.QRect(20, 65, 140, 30))
        scooterRadioButton.setObjectName("step_title_label")
        scooterRadioButton.setText("N3-Scooter")
        scooterRadioButton.setChecked(True)
        scooterRadioButton.setFont(QFont('Arial', 16))
        scooterRadioButton.toggled.connect(lambda: self.toggle_type_radio(scooterRadioButton))

        ebikeRadioButton = QtWidgets.QRadioButton(step2_box)
        ebikeRadioButton.setGeometry(QtCore.QRect(160, 65, 140, 30))
        ebikeRadioButton.setObjectName("step_title_label")
        ebikeRadioButton.setText("E-Bike")
        ebikeRadioButton.setFont(QFont('Arial', 16))
        ebikeRadioButton.toggled.connect(lambda: self.toggle_type_radio(ebikeRadioButton))

        self.create_btn = QtWidgets.QPushButton(step2_box)
        self.create_btn.setGeometry(QtCore.QRect(20, 110, 160, 34))
        self.create_btn.setObjectName("create_btn")
        self.create_btn.setText("生成二维码图片")
        self.create_btn.setStyleSheet(open("static/button.css").read())
        self.create_btn.setDisabled(True)
        self.create_btn.clicked.connect(self.create_qr_code_clicked)

        self.progress_label = QtWidgets.QLabel(step2_box)
        self.progress_label.setGeometry(QtCore.QRect(20, 160, 200, 30))
        self.progress_label.setObjectName("step_title_label")
        self.progress_label.setAlignment(QtCore.Qt.AlignTop)
        self.progress_label.setWordWrap(True)
        self.progress_label.setFont(QFont('Arial', 16))
        self.progress_label.setText("")

    def toggle_type_radio(self, btn):
        if btn.text() == "N3-Scooter":
            self.create_type = "N3-Scooter"
        elif btn.text() == "E-Bike":
            self.create_type = "E-Bike"

        print(self.create_type)

    def change_create_btn_status(self):
        if len(self.batch_array) == 0 or len(self.qr_code_array) == 0 or self.creating:
            self.create_btn.setDisabled(True)
            return
        self.create_btn.setDisabled(False)

    def create_qr_code_clicked(self):
        self.creating = True
        self.change_create_btn_status()
        self.change_generate_btn_status()
        self.change_clear_btn_status()

        print(self.create_type)

        self.thread = RunThread(self.create_type, self.qr_code_array, self.batch_array)
        self.thread.idx_signal.connect(self.creator_call_back)
        self.thread.start()

        print("complete")

    def creator_call_back(self, idx):
        step = int(((idx + 1) / len(self.qr_code_array)) * 100)
        if step > 100:
            step = 100
        self.progress_label.setText("已完成：{}%".format(step))
        self.progress_label.repaint()
        if idx == len(self.qr_code_array) - 1:
            self.create_finished()

    def create_finished(self):
        self.creating = False
        self.change_create_btn_status()
        self.change_generate_btn_status()
        self.change_clear_btn_status()

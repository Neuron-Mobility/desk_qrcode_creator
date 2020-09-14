from PyQt5.QtCore import QThread, pyqtSignal

from src.ebike_creator import create_e_bike_qr_codes
from src.n3_scooter_creator import create_n3_scooter_qr_codes


class RunThread(QThread):
    idx_signal = pyqtSignal(int)

    def __init__(self, type, qr_code_array, batch_array):
        super().__init__()
        self.type = type
        self.qr_code_array = qr_code_array
        self.batch_array = batch_array

    def run(self):
        if self.type == "E-Bike":
            create_e_bike_qr_codes(self.qr_code_array, self.batch_array, self.creator_call_back)
        elif self.type == "N3-Scooter":
            create_n3_scooter_qr_codes(self.qr_code_array, self.batch_array, self.creator_call_back)

    def creator_call_back(self, idx):
        self.idx_signal.emit(idx)

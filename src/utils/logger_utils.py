import logging
import os

from src.utils.path_utils import get_download_path

lg = logging.getLogger("Error")


def init_log():
    if len(lg.handlers) == 0:  # 避免重复
        # 2.创建handler(负责输出，输出到屏幕streamhandler,输出到文件filehandler)
        path = get_download_path()
        filename = os.path.join(path, 'qr_code_creator.txt')
        fh = logging.FileHandler(filename, mode="a", encoding="utf-8")
        sh = logging.StreamHandler()
        # 3.创建formatter：
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - Model:%(filename)s - Fun:%(funcName)s - Message:%(message)s - Line:%(lineno)d')
        # 4.绑定关系：①logger绑定handler
        lg.addHandler(fh)
        lg.addHandler(sh)
        # # ②为handler绑定formatter
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        # # # 5.设置日志级别(日志级别两层关卡必须都通过，日志才能正常记录)
        # lg.setLevel(40)
        # fh.setLevel(40)
        # sh.setLevel(40)

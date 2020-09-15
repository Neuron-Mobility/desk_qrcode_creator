import os

from src.utils.path_utils import resource_path

LOGO = resource_path(os.path.join('static', 'logo.png'))

FONT = resource_path(os.path.join('static', 'arial.ttf'))

# n3 scooter qrcode config
N3_SCOOTER_FONT = resource_path(os.path.join('static', 'Muli-Bold.ttf'))
# N3_EBIKE_FONT = resource_path(os.path.join('static', 'Muli-Regular.ttf'))
N3_BACK_GROUND = resource_path(os.path.join('static', 'N3_QR_BGD2.jpg'))
N3_LOGO = resource_path(os.path.join('static', 'N3_QR_Logo2.png'))

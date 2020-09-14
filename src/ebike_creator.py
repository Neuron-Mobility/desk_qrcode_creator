from src.utils.path_utils import get_download_path
from src.utils.utilities import make_n3_ebike_logo_qr, add_n3_ebike_caption
from src.config import N3_LOGO
import os


def create_e_bike_qr_codes(qr_codes, batch_array, callback):
    batch_index = 0
    current_batch, path = get_current_batch_and_path(batch_array, batch_index)
    if current_batch is None and path is None:
        return

    count = 0
    for idx, row in enumerate(qr_codes):
        if not row:
            continue

        code = row
        save_path = os.path.join(path, '{}.png'.format(code))
        str = "https://nss.neuron.sg/scan?qrCode={}&type=ebike"
        make_n3_ebike_logo_qr(str.format(code), N3_LOGO, save_path)
        add_n3_ebike_caption(save_path, 'No. ' + code, 35)
        print("Index:", idx, " , Code: ", code)

        if callback:
            callback(idx)

        if count + 1 == current_batch['count']:
            print(count, code, current_batch['count'])
            batch_index += 1
            current_batch, path = get_current_batch_and_path(batch_array, batch_index)
            if current_batch is None and path is None:
                break
            count = 0
        else:
            count += 1


def get_current_batch_and_path(batch_array, batch_index):
    if batch_index > len(batch_array) - 1:
        return None, None

    current_batch = batch_array[batch_index]

    path = os.path.join(get_download_path(), current_batch['prefix'])
    if not os.path.exists(path):
        os.makedirs(path)
    return current_batch, path

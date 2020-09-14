import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from src.config import N3_BACK_GROUND, N3_SCOOTER_FONT


def make_n3_logo_qr(str, logo, save):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=75,
        border=0
    )

    qr.add_data(str)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")

    # Add logo
    if logo and os.path.exists(logo):
        logo = Image.open(logo)

        logo = logo.crop((213, 360, 780 + 213, 780 + 360))
        logo_w, logo_h = logo.size

        img = img.resize((logo_w, logo_h), Image.ANTIALIAS)

        logo = logo.convert("RGBA")
        img.paste(logo, (0, 0, logo_w, logo_h), logo)

    img.save(save)


def add_n3_caption_and_bg(code_src, caption, font_size=20):
    bg = Image.open(N3_BACK_GROUND, 'r')
    w, h = bg.size

    bg = bg.convert("RGBA")

    new = Image.new('RGBA', (w, h), (255, 255, 255))
    new.paste(bg, (0, 0), bg)

    draw = ImageDraw.Draw(new)
    font = ImageFont.truetype(N3_SCOOTER_FONT, font_size)
    text_w, text_h = draw.textsize(caption, font)
    draw.text(((w - text_w) // 2, h - text_h - 60), caption, (255, 255, 255), font=font)

    code_img = Image.open(code_src, 'r')
    cw, ch = code_img.size
    # new_cw, new_ch = int(cw / 2), int(ch / 2)
    # code_img = code_img.resize((new_cw, new_ch), Image.ANTIALIAS)
    new.paste(code_img, (215, 360), code_img)

    new.save(code_src)


def make_n3_ebike_logo_qr(str, logo, save):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=75,
        border=0
    )

    qr.add_data(str)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")

    # Add logo
    if logo and os.path.exists(logo):
        logo = Image.open(logo)

        logo = logo.crop((213, 360, 780 + 213, 780 + 360))
        logo_w, logo_h = logo.size

        img = img.resize((logo_w, logo_h), Image.ANTIALIAS)

        logo = logo.convert("RGBA")
        img.paste(logo, (0, 0, logo_w, logo_h), logo)

    img.save(save)


def add_n3_ebike_caption(code_src, caption, font_size=20):
    w = 360
    h = 360
    new = Image.new('RGBA', (w, h), (255, 255, 255))

    draw = ImageDraw.Draw(new)
    font = ImageFont.truetype(N3_SCOOTER_FONT, font_size)
    text_w, text_h = draw.textsize(caption, font)
    draw.text(((w - text_w) // 2, h - text_h - 10), caption, (0, 0, 0), font=font)

    code_img = Image.open(code_src, 'r')
    code_img = code_img.resize((290, 290), Image.ANTIALIAS)
    new.paste(code_img, (35, 20), code_img)

    new.save(code_src)


def generate_sticker_numbers(code, font_size, file_path, width=413, height=1949):
    image = Image.new('RGBA', (width, height), (0, 0, 0))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(N3_SCOOTER_FONT, font_size)

    for idx, no in enumerate(str(code)):
        text_w, text_h = draw.textsize(no, font)
        draw.text(((width - text_w) // 2, 30 + (idx * (text_h + 30))), no, (255, 255, 255), font=font)

    image.save(file_path)

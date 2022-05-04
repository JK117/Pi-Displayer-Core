from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
import time
import datetime


def init_screen(screen_device):
    device_h = screen_device.height
    device_w = screen_device.width

    font_title = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 18)
    font_subtitle = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 12)

    init_title = 'Raspberry Pi'
    init_subtitle = "Initialize Completed"

    title_w, title_h = font_title.getsize(init_title)
    subtitle_w, subtitle_h = font_subtitle.getsize(init_subtitle)

    title_x_position = device_w / 2 - title_w / 2
    title_y_position = (device_h - title_h - subtitle_h - 2) // 3 + 1
    subtitle_x_position = device_w / 2 - subtitle_w / 2
    subtitle_y_position = (device_h - title_h - subtitle_h - 2) // 3 * 2 + 1 + title_h

    with canvas(screen_device) as draw:
        draw.rectangle(screen_device.bounding_box, fill="black", outline="white")
        draw.text((title_x_position, title_y_position), init_title, fill="white", font=font_title)
        draw.text((subtitle_x_position, subtitle_y_position), init_subtitle, fill="white", font=font_subtitle)
    time.sleep(5)


if __name__ == '__main__':
    try:
        serial = spi(device=0, port=0)
        spi_screen = sh1106(serial)
        init_screen(spi_screen)
    except KeyboardInterrupt:
        pass

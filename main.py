from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont
import time
import datetime


def init_screen(screen_device):
    device_h = screen_device.height
    device_w = screen_device.width

    font_title = ImageFont.truetype("Quicksand-Bold.ttf", 18)
    font_subtitle = ImageFont.truetype("Quicksand-Bold.ttf", 12)

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


def display_time(screen_device):
    font_large = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 22)
    font_small = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 12)

    screen_h = screen_device.height
    screen_w = screen_device.width

    large_0_w, large_0_h = font_large.getsize('0')
    large_colon_w, large_colon_h = font_large.getsize(':')
    small_0_w, small_0_h = font_small.getsize('0')

    hour_position_x = screen_w / 2 - large_0_w * 3 - large_colon_w
    minute_position_x = screen_w / 2 - large_0_w
    second_position_x = screen_w / 2 + large_0_w + large_colon_w
    colon_1_position_x = screen_w / 2 - large_0_w - large_colon_w
    colon_2_position_x = screen_w / 2 + large_0_w
    position_y = (screen_h - large_0_h - small_0_h - 2) // 3 + 1

    while True:
        current_datetime = datetime.datetime.now()
        current_hour = current_datetime.strftime('%H')
        current_minute = current_datetime.strftime('%M')
        current_second = current_datetime.strftime('%S')
        with canvas(screen_device) as draw:
            draw.rectangle(screen_device.bounding_box, fill="black", outline="white")
            draw.text((hour_position_x, position_y), current_hour, fill="white", font=font_large)
            draw.text((minute_position_x, position_y), current_minute, fill="white", font=font_large)
            draw.text((second_position_x, position_y), current_second, fill="white", font=font_large)
            draw.text((colon_1_position_x, position_y), ':', fill="white", font=font_large)
            draw.text((colon_2_position_x, position_y), ':', fill="white", font=font_large)
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        serial = spi(device=0, port=0)
        spi_screen = sh1106(serial)
        init_screen(spi_screen)
        display_time(spi_screen)
    except KeyboardInterrupt:
        pass

import board
import displayio
import time
import os
import terminalio
import touchio
import neopixel
import random
import adafruit_uc8151d
from adafruit_display_text import label

# Define board pinout
board_spi = board.SPI()
board_epd_cs = board.D41
board_epd_dc = board.D40
board_epd_reset = board.D39
board_epd_busy = board.D42

# Define touch buttons
touch_threshold = 20000
touch_1 = touchio.TouchIn(board.D5)
touch_1.threshold = touch_threshold
touch_2 = touchio.TouchIn(board.D4)
touch_2.threshold = touch_threshold
touch_3 = touchio.TouchIn(board.D3)
touch_3.threshold = touch_threshold
touch_4 = touchio.TouchIn(board.D2)
touch_4.threshold = touch_threshold
touch_5 = touchio.TouchIn(board.D1)
touch_5.threshold = touch_threshold

# Define ePaper display colors value
display_color_black = 0x000000
display_color_white = 0xFFFFFF

# Define LED's
led_pin = board.D18
led_matrix = neopixel.NeoPixel(led_pin, 4, brightness = 0.1, auto_write = False)

# Define ePaper display resolution
display_width = 212
display_height = 104

# Prepare ePaper display
displayio.release_displays()
display_bus = displayio.FourWire(
    board_spi, command=board_epd_dc, chip_select=board_epd_cs, reset=board_epd_reset, baudrate=1000000
)
time.sleep(1)
display = adafruit_uc8151d.UC8151D(
    display_bus, width=display_width, height=display_height, rotation=270, busy_pin=board_epd_busy, seconds_per_frame=10.0
)
display_data = displayio.Group()
display_background = displayio.Bitmap(display_width, display_height, 1)
display_color_palette = displayio.Palette(1)
display_color_palette[0] = display_color_white

# Append tilegrid with the background to the display data
display_data.append(displayio.TileGrid(
    display_background, pixel_shader=display_color_palette)
)

# Fuction for display refresh
def _displayRefresh():
    while True:
        try:
            display.refresh()
            while display.busy:
                pass
            return
        except RuntimeError as ex:
            print(ex)
            time.sleep(5)

# Function for append text to the display data
def _addText(text, scale, color, x_cord, y_cord):
    group = displayio.Group(scale=scale, x=x_cord, y=y_cord)
    text_label = label.Label(terminalio.FONT, text=text, color=color)
    group.append(text_label)
    display_data.append(group)

# Function for clearing display data
def _clearDisplayData():
    for i in range(len(display_data) - 1):
        display_data.pop()
    _displayRefresh()

# Function for rendering namecard to display
def _showNamecard():
    try:
        if os.stat('namecard'):
            namecard_raw_file = open('namecard', 'r')
            namecard_data = namecard_raw_file.readlines()
            for line in namecard_data:
                data = line.split(",")
                _addText(data[0], int(data[1]), display_color_black, int(data[2]), int(data[3]))
            display.show(display_data)
            namecard_raw_file.close()
            _displayRefresh()
    except OSError:
        _addText('Missing namecard file!', 1, display_color_black, 40, 48)
        display.show(display_data)
        _displayRefresh()

# Function for turn off all LED's
def _turnOffLeds():
    led_matrix.fill((0, 0, 0))
    led_matrix.show()

# Function for random LED's color
def _randomLedsColor():
    led_matrix.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    led_matrix.show()

# Function for roll of dice
def _rollOfDice():
    count = 0
    while count < 30:
        _randomLedsColor()
        time.sleep(0.1)
        count += 1
    _turnOffLeds()
    _clearDisplayData()
    _addText('>' + str(random.randint(1, 6)) + '<', 9, display_color_black, 25, 50)
    display.show(display_data)
    _displayRefresh()
    pass


### MAIN PROGRAM ###
# Init render of namecard to display
_showNamecard()

# Main loop
while True:
    if touch_1.value:
        # Turn off all LED's and show namecard
        _turnOffLeds()
        _clearDisplayData()
        _showNamecard()
    if touch_2.value:
        # Turn on LED's with random color
        _randomLedsColor()
    if touch_3.value:
        # Roll of dice
        _rollOfDice()
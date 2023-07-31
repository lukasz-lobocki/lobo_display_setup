# lobo_display_setup
import sys

from machine import Pin, SPI, I2C
from lobo_rig.rig import *


class Device:
    def __init__(
        self,
        device: str,
        rotation: int = 0,
        font=None,
        spi_power: Pin = None,
        spi_cs: Pin = None,
        spi_dc: Pin = None,
        spi_rst: Pin = None,
    ):
        self.device = device
        self.rotation = rotation
        self.font = font
        self.spi_power = spi_power
        self.spi_cs = spi_cs
        self.spi_dc = spi_dc
        self.spi_rst = spi_rst

        self.interface = None
        self.display = None

        # Bigger LCD via SPI
        if self.device == "ILI9341":
            from ..micropython_ili9341.ili934xnew import ILI9341

            self.interface = SPI(
                SPI_PORTS[0]["ID"],
                baudrate=40000000,
                miso=SPI_PORTS[0]["SPI_MISO"],
                mosi=SPI_PORTS[0]["SPI_MOSI"],
                sck=SPI_PORTS[0]["SPI_SCK"],
            )
            self.display = ILI9341(
                self.interface,
                cs=self.spi_cs,
                dc=self.spi_dc,
                rst=self.spi_rst,
                w=320,
                h=240,
                r=self.rotation,
                font=self.font,
            )
            
            self.display.set_pos(
                0, self.display.height - self.display._font.height() - 1
            )

            self.spi_power.init(Pin.OUT)
            self.spi_power.on()
            self.display.erase()

        # Medium OLED via I2C
        elif self.device == "SH1106":
            from ..sh1106 import sh1106_fr_buf as sh1106

            self.interface = I2C(
                I2C_PORTS[0]["ID"],
                sda=I2C_PORTS[0]["I2C_SDA"],
                scl=I2C_PORTS[0]["I2C_SCL"],
                freq=1000000,
            )
            self.display = sh1106.SH1106_I2C(
                128,
                64,
                self.interface,
                rotate=self.rotation,
            )
            self.display.poweron()
            self.display.reset()
            self.display.contrast(128)

        # Small OLED via I2C
        elif self.device == "SSD1306":
            import ssd1306

            self.interface = I2C(
                I2C_PORTS[0]["ID"],
                sda=I2C_PORTS[0]["I2C_SDA"],
                scl=I2C_PORTS[0]["I2C_SCL"],
                freq=1000000,
            )
            self.display = ssd1306.SSD1306_I2C(
                128,
                64,
                self.interface,
                0x3C,
            )
            self.display.poweron()
            self.display.reset()
            self.display.contrast(128)

    def line_print(self, text: str) -> None:
        # non-framebuff
        if self.device == "ILI9341":
            self.display.print(text)
        # framebuff
        elif self.device == "SH1106" or self.device == "SSD1306":
            from ..writer.writer import Writer

            wri = Writer(self.display, self.font, verbose=False)
            wri.set_textpos(
                self.display, self.display.height - self.display.pages - 1, 0
            )
            wri.printstring(text)
            self.display.show()

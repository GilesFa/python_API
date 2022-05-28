import struct
import ctypes

#PATH = 'C:\\temp\\cat_4ci.gif'
SPI_SETDESKWALLPAPER = 20

def is_64bit_windows_():
    """Check if 64 bit Windows OS"""
    return struct.calcsize('P') * 8 == 64

def changeBG_(path):
    """Change background depending on bit size"""
    #if is_64bit_windows():
    if struct.calcsize('P') * 8 == 64:
        print("os is 64bit")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    else:
        print("os is 32bit")
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 3)


if __name__ == "__main__": 
    changeBG_(PATH)
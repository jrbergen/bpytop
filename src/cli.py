import argparse

import psutil

from bpytop import __VERSION__


class CliArgs(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("-b", "--boxes", action="store", dest="boxes",
                          help="which boxes to show at start, example: -b \"cpu mem net proc\"")
        self.add_argument("-lc", "--low-color", action="store_true",
                          help="disable truecolor, converts 24-bit colors to 256-color")
        self.add_argument("-v", "--version", action="store_true", help="show version info and exit")
        self.add_argument("--debug", action="store_true",
                          help="start with loglevel set to DEBUG overriding value set in config")

        stdargs = self.parse_args()
        self.ARG_BOXES: str = stdargs.boxes
        self.LOW_COLOR: str = stdargs.low_color
        self.DEBUG: str = stdargs.debug

        if stdargs.version:
            print(f'bpytop version: {__VERSION__}\n'
                  f'psutil version: {".".join(str(x) for x in psutil.version_info)}')
        raise SystemExit(0)

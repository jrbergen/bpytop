import sys
from time import time
from typing import Dict

from bpytop import errlog


def get_system_string() -> str:
	"""Retrieves internal name for OS/platform using sys.platfrom"""
	if "linux" in sys.platform:
		return "Linux"
	elif "bsd" in sys.platform:
		return "BSD"
	elif "darwin" in sys.platform:
		return "MacOS"
	else:
		return "Other"


class TimeIt:
    timers: Dict[str, float] = {}
    paused: Dict[str, float] = {}

    @classmethod
    def start(cls, name):
        cls.timers[name] = time()

    @classmethod
    def pause(cls, name):
        if name in cls.timers:
            cls.paused[name] = time() - cls.timers[name]
            del cls.timers[name]

    @classmethod
    def stop(cls, name):
        if name in cls.timers:
            total: float = time() - cls.timers[name]
            del cls.timers[name]
            if name in cls.paused:
                total += cls.paused[name]
                del cls.paused[name]
            errlog.debug(f'{name} completed in {total:.6f} seconds')

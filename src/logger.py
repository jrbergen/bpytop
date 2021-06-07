import logging

from src.static.paths import Paths


class ErrorLogger(logging.Logger):

    def __init__(self,
                 name: str = 'ErrorLogger',
                 max_bytes_rotating_logfile: int = 1048576,
                 level=logging.DEBUG,
                 backupcount: int = 4):

        super().__init__(name=name, level=level)

        try:
            # noinspection PyUnresolvedReferences
            eh = logging.handlers.RotatingFileHandler(Paths.LOG_PATH_ERR,
                                                      maxBytes=max_bytes_rotating_logfile,
                                                      backupCount=backupcount)
            eh.setLevel(logging.DEBUG)
            eh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s: %(message)s", datefmt="%d/%m/%y (%X)"))
            self.addHandler(eh)

        except PermissionError:
            print(f'ERROR!\nNo permission to write to "{str(Paths.LOG_PATH_ERR.parent)}" directory!')
            raise SystemExit(1)

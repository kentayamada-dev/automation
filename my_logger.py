from logging import (
    Formatter,
    ERROR,
    CRITICAL,
    StreamHandler,
    getLogger,
)
from datetime import datetime
from pytz import timezone


class MyLogger:
    class MyFormatter(Formatter):
        RED = "\033[0;31m"
        GREEN = "\033[0;32m"
        END = "\033[0m"

        info = "[%(asctime)s JST] %(filename)s > %(funcName)s():"
        message = "\n%(message)s\n"
        fmt = {
            # DEBUG: grey + fmt + reset,
            # INFO: grey + fmt + reset,
            # WARNING: yellow + fmt + reset,
            ERROR: f"{GREEN}{info}{END}{message}",
            CRITICAL: f"{RED}{info}{END}{message}",
        }

        @staticmethod
        def __convert_time(_):
            return datetime.now(timezone("Asia/Tokyo")).timetuple()

        def format(self, record):
            formatter = Formatter(
                self.fmt.get(record.levelno),
                datefmt="%Y/%m/%d %H:%M:%S",
            )
            formatter.converter = self.__convert_time

            return formatter.format(record)

    @classmethod
    def get_logger(cls):
        logger = getLogger()
        logger.setLevel(ERROR)
        stream_handler = StreamHandler()
        stream_handler.setLevel(ERROR)
        stream_handler.setFormatter(cls.MyFormatter())
        if not logger.hasHandlers():
            logger.addHandler(stream_handler)

        return logger

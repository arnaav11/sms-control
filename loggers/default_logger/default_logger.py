import logging

from loggers.logger import Logger

class DefaultLogger(Logger):
    def __init__(self):
        super().__init__()
        self.FORMAT = '| %(asctime)s | [%(module)s:%(lineno)d] %(levelname)s: %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=self.FORMAT
        )

        self.logger = logging.getLogger()
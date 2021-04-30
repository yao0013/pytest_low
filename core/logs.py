import os
import logzero
import logging
from configs import settings


class CustomLogger:

    def __init__(self, devel=settings.log_devel, filename='autotest.log'):
        # if not isinstance(logging.)
        self.logfile = os.path.join(settings.log_path, filename)
        file_path = os.path.split(self.logfile)[0]
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        logzero.logfile(self.logfile, maxBytes=1e7, backupCount=3, encoding='utf-8')

        formatter = logging.Formatter('%(asctime)-15s - [%(filename)s: %(lineno)s] - %(levelname)s: %(message)s')
        logzero.formatter(formatter)
        logzero.loglevel(devel)
        self.logger = logzero.logger


log = CustomLogger().logger


if __name__ == "__main__":
    log.info("testtest")

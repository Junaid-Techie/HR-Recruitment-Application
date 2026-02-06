import falcon
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('test.log'))
logger.setLevel(logging.INFO)
import  os
from datetime import datetime
import sys
import falcon
class ResponseLoggerMiddleware(object):
    def __init__(self):
        self.logging = self.set_up_logging()

    def set_up_logging(self):
        file_path = sys.modules[__name__].__file__
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
        log_location = project_path + '/logs/'
        if not os.path.exists(log_location):
            os.makedirs(log_location)

        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        file_name = current_date + '.log'
        file_location = log_location + file_name
        with open(file_location, 'a+'):
            pass

        logger = logging.getLogger(__name__)
        #format = '[%(asctime)s] [%(levelname)s] [%(message)s] [--> %(pathname)s [%(process)d]:]'
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # To store in file
        logging.basicConfig(format=format, filemode='a+', filename=file_location, level=logging.DEBUG)
        # To print only
        # logging.basicConfig(format=format, level=logging.DEBUG)
        #level = logging.DEBUG
        return logger
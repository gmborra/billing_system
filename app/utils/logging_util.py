import logging

log_file = "bill_system_log"
logger = logging.getLogger('bill_system')
logging.basicConfig(filename=log_file, level=logging.INFO)
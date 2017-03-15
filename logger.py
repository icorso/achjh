import logging
import os
from logging.handlers import RotatingFileHandler
import sys

LOGFILE = str(os.path.dirname(os.path.abspath(__file__))) + "/achjh.log"

log = logging.getLogger('')
log.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(fmt)
log.addHandler(ch)

fh = RotatingFileHandler(LOGFILE, maxBytes=(1048576 * 5), backupCount=7)
fh.setFormatter(fmt)
log.addHandler(fh)

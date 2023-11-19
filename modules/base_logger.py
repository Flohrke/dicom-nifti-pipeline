import logging
import config as c
from datetime import datetime
import shutil
import os

# set up logging pathing
date = datetime.now()
date = date.strftime("%y%m%d")

# get real path of script
pathLogs = os.path.realpath(os.path.dirname(__file__)).replace("modules", f"logs/{c.name}/")

if not os.path.exists(pathLogs):
    os.makedirs(pathLogs)

logFile = pathLogs + f"{c.name}_{date}.log"
configFile = pathLogs + f"{c.name}_config_{date}.py"

# set up logger
logger = logging
logger.basicConfig(
    level=c.logLevel,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(logFile),
        logging.StreamHandler()
    ]
)

# getting config regardless from where script is executed
srcConfig = os.path.realpath(os.path.dirname(__file__)).replace("modules", "config.py")
shutil.copy(srcConfig, configFile)


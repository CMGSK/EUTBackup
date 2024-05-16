import time
import os
import zipfile
import dotenv
from utils import startup_script, add_recursively, log, delete_old_files

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

if os.environ["IS_FIRST_EXECUTION"] == "True":
    log("First execution of the script")
    startup_script(env_file)

targets = open(os.getenv("TARGETS_PATH_FILE")).readlines()
log(f"Targets defined: {'\n\t'.join(target for target in targets)}")
safes = open(os.getenv("SAFE_LOCATION_PATHS")).readlines()
log(f"Safe locations defined: {'\n\t'.join(safe for safe in safes)}")

for location in safes:
    try:
        with zipfile.ZipFile(file=f"{location}/{os.getenv("NAME_BACKUP")}_{int(time.time())}.zip",
                             mode='w',
                             compression=zipfile.ZIP_DEFLATED) as zf:
            log("Created instance of zip")
            for target in targets:
                add_recursively(zf=zf, path=target)
        delete_old_files(safes, int(os.getenv("DELETE_WHEN_REACH")))
    except Exception as e:
        log(f"An exception has occurred while trying to backup the necessary files ===> {str(e)}")

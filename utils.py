import datetime
import os
import zipfile
import dotenv


def startup_script(env_file):
    cf_safes = []
    cf_targets = []
    cf_limit = "7"
    cf_path = ".config"
    print("Indicate the paths to store backups.\n"
          "You can omit this step to configure it manually.\n\n")
    while (line := input("Input a path or type 'ready' to finish this configuration step\n>")) != "ready":
        cf_safes.append(line)

    print("Indicate the paths to include in the backup files.\n"
          "You can omit this step to configure it manually.\n\n")
    while (line := input("Input a path or type 'ready' to finish this configuration step\n>")) != "ready":
        cf_targets.append(line)

    print("Indicate the number of older backups to mantain\n"
          "If you leave this blank it will default to 7.\n\n")
    if line := input("Path to the config directory\n>") != "":
        cf_path = line

    print("Indicate the path to include the config files. Please omit the ending slash ('/')\n"
          "If you leave this blank it will be stored automatically in .config folder within this project.\n\n")
    if line := input("Path to the config directory\n>") != "":
        cf_limit = line

    with open(f"{cf_path}/backups.txt", 'x') as file:
        for p in cf_safes:
            file.write(p)
    with open(f"{cf_path}/targets.txt", 'x') as file:
        for p in cf_targets:
            file.write(p)

    os.environ["IS_FIRST_EXECUTION"] = "False"
    dotenv.set_key(env_file, "IS_FIRST_EXECUTION", os.environ["IS_FIRST_EXECUTION"])
    os.environ["DELETE_WHEN_REACH"] = cf_limit
    dotenv.set_key(env_file, "IS_FIRST_EXECUTION", os.environ["IS_FIRST_EXECUTION"])


def add_recursively(zf: zipfile.ZipFile, path: str):
    log(f"Adding {path} contents to the ZIP instance...")
    try:
        for subpath in os.listdir(path):
            if os.path.isfile(subpath):
                zf.write(subpath)
            else:
                add_recursively(zf, subpath)
        log(f"Succesfully added {path} contents to the ZIP instance")
    except Exception as e:
        log(f"An exception has occurred in the previous process ===> {str(e)}")


def delete_old_files(backups: list, max: int):
    log("Deleting old backups...")
    try:
        for dir in backups:
            log(f"Working on {dir}...")
            if len(content := [(name, os.path.getmtime(name)) for name in os.listdir(dir)]) > max:
                content = content.sort(key=lambda e: e[1])[:max]
                for file in content:
                    os.remove(file)
                    log(f"Success.")
        log("Deleted old backups")
    except Exception as e:
        log(f"An exception has occurred in the previous process ===> {str(e)}")


def log(msg: str):
    with open("./logs/log.txt") as logfile:
        logfile.write(f"{datetime.datetime.now().strftime("%d/%m/%Y at %H:%M:%S")} -> {msg}")


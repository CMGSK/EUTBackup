
# EUTBackups

Python script for generating .zip formmated backups of data


# Use
Execute the script manually the first time to configure it following the prompts.

You can create your own .txt file configurations for where to store backups and what contains in them, and store those files either in the provided .config folder, or in a location of your choice that you will need to configure later on through the first run of the script.

You can manually cconnfigure the .env file if you're an experienced user.

# Automatization
## Windows
After following the prompts of the script, run this command on your Shell replacing the values within <> to create an automated service:

```schtasks /create /tn <NAME_TASK> /tr "\"<PY_FILE>"" /sc <[DAILY/HOURLE/WEEKLY...]> /st <HH:MM> /f /RI 60```

Further info can be found on schtasks official documentation.

## Linux/macOS

Install the cron package in your system (from extra/cronie).

Generate the cron command to run the script based on your necessities in a generator such as http://www.cronmaker.com/.

run the followind command on your shell:

```crontab -e <CRON_COMMAND> <PY_FILE>```
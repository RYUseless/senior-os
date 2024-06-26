import logging
import os
import datetime
import subprocess

logger = logging.getLogger(__file__)

def get_DB():
    file_path = os.path.join(os.getcwd().split("smail")[0], "sconf/phish/SMAIL_PHISH_1.txt")
    command = f"wget -O {file_path} https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-links.txt"
    # Check if database exists
    if os.path.exists(file_path):
        last_modif_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        current_date = datetime.datetime.now()
        file_age = current_date - last_modif_date
        update_time = datetime.timedelta(days=14)

        logger.info(f"Phishing database file is {file_age.days} days, {file_age.seconds // 3600} hours, "
              f"and {(file_age.seconds // 60) % 60} minutes old.")

        # If age of the file is bigger than update time,
        # new updated file will be downloaded
        if file_age >= update_time:
            try:
                # Execute command
                subprocess.run(command, shell=True, check=True,
                               executable='/bin/bash', stdout=subprocess.PIPE)
            except:
                logger.info(f"The command {command} failed. "
                            f"Cannot update phishing database.")
        else:
            logger.info(f"The file {file_path} is not older than 2 weeks. "
                        f"No need to update phishing database.")

    else:
        # If file with phishing database is missing
        # Execute command
        try:
            subprocess.run(command, shell=True, check=True,
                           executable='/bin/bash', stdout=subprocess.PIPE)
            logger.info(f"The file {file_path} does not exist. "
                        f"Downloading current phishing database")

        except:
            logger.info(f"The command {command} failed. "
                        f"Cannot update phishing database.")

import os
import re
import csv
import datetime
import subprocess
import logging


EXP_DAY=30

def configure_logging():
    logging.basicConfig(
        filename='/var/log/wg_manager.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

configure_logging()

def read_wg_config_file(path: str) -> str:
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading wg config file: {e}")
        return ""

def write_wg_config_file(path: str, content: str) -> None:
    try:
        with open(path, 'w') as f:
            f.write(content)
    except Exception as e:
        logging.error(f"Error writing wg config file: {e}")

def remove_old_peers(contents: str, days: int = EXP_DAY) -> str:
    users = contents.split('\n\n')
    new_users = []

    for user in users:
        creation_date_match = re.search(r'# Added on: (\d{4}-\d{2}-\d{2})', user)

        if creation_date_match:
            creation_date = datetime.datetime.strptime(creation_date_match.group(1), '%Y-%m-%d').date()
            if (datetime.date.today() - creation_date).days <= days:
                new_users.append(user)
        else:
            new_users.append(user)

    return '\n\n'.join(new_users)

def reload_wg_interface(interface_name: str) -> None:
    try:
        subprocess.run(['wg-quick', 'down', interface_name], check=True)
        subprocess.run(['wg-quick', 'up', interface_name], check=True)
        logging.info(f"WireGuard interface {interface_name} reloaded.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error reloading WireGuard interface {interface_name}: {e}")

def main():
    wg_config_path = '/etc/wireguard/wg0.conf'

    if not os.path.exists(wg_config_path):
        logging.error(f"File '{wg_config_path}' not found.")
        return

    contents = read_wg_config_file(wg_config_path)
    new_contents = remove_old_peers(contents) 
    write_wg_config_file(wg_config_path, new_contents)
    logging.info(f"Old peers removed from '{wg_config_path}'.")

    reload_wg_interface("wg0")

if __name__ == "__main__":
    main()

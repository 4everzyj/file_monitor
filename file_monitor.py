# coding:utf-8

import os
import time
# import winsound
from tkinter import messagebox
import yaml
import logging


VERSION = '1.1'
LOG_PATH = './file_monitor.log'

if os.path.isfile(LOG_PATH):
    os.remove(LOG_PATH)

logger = logging.getLogger(__name__)
handler = logging.FileHandler(LOG_PATH)
fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(fh_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

with open('./config.json', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# file_path = data['file_path']
file_dir = data['file_dir']
ignore_heads = data['ignore_heads']
ts_sleep = data['ts_sleep']


def monitor_files(file_dir):
    logger.info('start monitoring %s.' % file_dir)
    if not os.path.isdir(file_dir):
        logger.info('file_dir not exists: %s' % file_dir)
        time.sleep(1)
        return
    ts_last_dict = {}
    while True:
        file_list = os.listdir(file_dir)
        for filename in file_list:
            ignore = False
            for ignore_head in ignore_heads:
                if filename.startswith(ignore_head):
                    ignore = True
                    break
            if ignore:
                continue
            file_path = os.path.join(file_dir, filename)
            if os.path.isdir(file_path):
                continue
            ts_modify = os.path.getmtime(file_path)
            if filename not in ts_last_dict:
                ts_last_dict.update({filename: -1})
            if ts_modify != ts_last_dict[filename] and ts_last_dict[filename] != -1:
                logger.info('file: %s modified.' % filename)
                # winsound.Beep(440, 1000)
                messagebox.showinfo('new message', 'file: %s modified.' % filename)
            ts_last_dict.update({filename: ts_modify})
        time.sleep(ts_sleep)


def monitor_file(file_path):
    if not os.path.isfile(file_path):
        logger.info('file not exists: %s' % file_path)
        return
    ts_last = -1
    while True:
        ts_modify = os.path.getmtime(file_path)
        if ts_modify != ts_last and ts_last != -1:
            logger.info('file modified.')
            # winsound.Beep(440, 1000)
            messagebox.showinfo('new message', 'file modified.')
        ts_last = ts_modify
        time.sleep(ts_sleep)


if __name__ == '__main__':
    logger.info('current version: %s' % VERSION)
    # monitor_file(file_path)
    monitor_files(file_dir)

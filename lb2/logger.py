import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir='logs', log_file='app.log'):
        self.log_dir = log_dir
        self.log_file = log_file
        #создаём папку для логов если её нет
        os.makedirs(self.log_dir, exist_ok=True)
        self.file_path = os.path.join(self.log_dir, log_file)

    def _write(self, level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} [{level}] {message}\n")

    def info(self, message):
        self._write('INFO', message)

    def error(self, message):
        self._write('ERROR', message)
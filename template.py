import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

for file in list_of_files:
    file = Path(file)
    folder, file = os.path.split(file)
    print(folder, file)
    
    if folder != '':
        os.makedirs(folder, exist_ok=True)
        
    if (not os.path.exists(file)) or (os.path.getsize(file) == 0):
        with open(file, "w") as f:
            pass
            logging.info(f"File creaeted {file}")
    else:
        logging.info(f"{file} already exists")        
    
        
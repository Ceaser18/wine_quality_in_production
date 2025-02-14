#automated script to create a new project folder with a template file structure
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")

project_name="datascience"

list_of_files=[
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",   #constructor to a package so that it can be imported
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",

    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "DOCKERFILE",
    "setup.py",
    "research/research.ipynb",
    "templates/index.html",
    "app.py"

]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath) #splitting the path into directory and filename

    if filedir!="":
        os.makedirs(filedir,exist_ok=True) #creating the directory if it does not exist
        logging.info(f"created directory {filedir} for the file {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,"w") as f:
            logging.info(f"created file {filename}")
    else:
        logging.info(f"file {filename} already exists")





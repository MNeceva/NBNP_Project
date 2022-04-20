# NBNP_Project 

## Linux System

Version: Ubuntu 20.04

## Python

Version: Python 3.8.10

## Flask Framework

Version: Flask 2.0.3

After downloading or cloning this repository, use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the libraries, modules and packages used while developing this application.

```bash
#NBNP_Project is the name of the wrapper folder of this project, you can rename it if you like.
#Pay attention, to perform any activity, you should always be located inside the wrapper folder!
cd NBNP_Project                  
pip install -r requirements.txt
```

From terminal set few ENVIRONMENTAL VARIABLES

```bash
export FLASK_APP=app
export FLASK_ENV=development
```

## Start application

```bash
python run.py
```

## Database 
Used database for this project: MongoDB Atlas (Cloud Database)

Used ODM: MongoEngine

Connection to the cloud database is established automatically when the application is started, using the config.py file

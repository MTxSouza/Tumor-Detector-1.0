# TumorDetector
[ATTENTION]: *This project has some bugs, i'm working to fix them.*
### Requirements
- Git
- Python3
- pip
---
First, clone the repository into your computer using the comand below on terminal and go inside of it.
```
git clone https://github.com/MTxSouza/TumorDetector
cd TumorDetector
```
Go to the project folder and install all requirements to run the application.

*It is strongly recommended to create a virtual environment to run the application, to do so, follow the rules below or skip them and go to 'Install' topic if you don't want to create an isolated environment for this project.*

---
### Virtual Environment
##### - Conda
*Make sure you have anaconda installed in your machine, if you don't you can install using this [link](https://www.anaconda.com).*
```
conda create --name tumor_detector
conda activate tumor_detector
```
##### - Python Env
*Make sure you have python-env installed in your machine, if you don't you can install using this [link](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).*
```
python3 -m venv tumor_detector

source tumor_detector/bin/activate # Linux
# or
./tumor_detector/Scripts/activate # Windows
```
---
### Install
Inside of the project folder, run the requirenments script using the command below on terminal.
```
pip install -r requirements.txt
```
---
### Run
To run the application, run the command below on terminal.
```
python3 app.py
# or
python app.py
```

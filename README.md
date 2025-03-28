# WAD2_Team_Project
WAD2 Team Project
 
Install Python 3.10 on your machine.
 
To clone the repository:
```
git clone https://github.com/ConorHaughney/WAD2_Team_Project
```
To create the Conda environment:
```
conda create -n recipe python=3.10
```
To setup the environment:
```
cd to WAD2_Team_Project\RecipeSite
conda activate recipe
pip install -r requirements.txt
```
 
Wait until the environment is setup. To create the database:
```
python manage.py makemigrations
python manage.py migrate
python population_script.py
```
 
To run the server:
```
python manage.py runserver
```
 
# Pythonanywhere
This website can be accessed on PythonAnywhere at the URL:  
<https://finerstorm30.pythonanywhere.com/>

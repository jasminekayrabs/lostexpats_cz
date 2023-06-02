# Lostexpats_cz
Secure Application Development Software Project

# Project Title: 
Lostexpats_cz

# Description: 
Secure website designed to make life easier for english speaking foreigners in the Czech Republic. It is a website for news, events happening in prague, nightlife as well as restaurants and cafes.

# Requirements: 
- [Python3.9](https://www.python.org)
- [Django](https://docs.djangoproject.com/en/4.2/)
- flask
- requests
- Virtual Environment

# Project Installation:
First, you need to create a folder and install django, as well as a virtual environment. After that, clone this repository into the folder by going into the directory and running the following command on your terminal;
```bash
git clone https://github.com/jasminekayrabs/lostexpats_cz
```
 Activate your virtual environment and cd into lostexpats_cz
 run the following commands to install other dependencies;
```bash
pip install flask
```
```bash
pip install django-cryptology
```
```bash
pip install django-axes
```
Request the secret key from us and add it to settings.py. Open settings.py, tests.py and views.py to change any file paths to your local paths. for example on settings.py, change this line to the path of the static folder on your local device:
```bash
STATICFILES_DIRS = [
    '/Users/jasminekabir/Documents/sad_ica2/lostexpats_cz/static',
    ]
```
to;
```bash
STATICFILES_DIRS = [
    '/your/path/lostexpats_cz/static',
    ]
```
Run the following command to run the server.
 
```bash
>>> python manage.py runsslserver
```
 
# Running the project:
Open the cloned folder and run the command 
```bash
>>> python manage.py runserver
```

# Testing Security Implementation:
Run the following command
```bash
>>> python manage.py test
```
# To make yourself an admin on the website: 
```
Run the following command on your terminal:
```bash
>>> python manage.py createsuperuser
```
# Link to Website


# License:
Copyright © 2023 Jasmine K., Sara M., Veronika K., Mia P.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# Contributors
- Jasmine Kabir
- Mia Petrusic
- Sara Ali
- Veronika Katsevych

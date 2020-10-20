# Software-Engineering


Project Title - GamePlan

Team Members - Matthew Yin, Soojie Chin, Amber Pradhan, Raghuveer Gummadi

Implementation

Go to the linked Github https://github.com/myin3/Software-Engineering and clone the repository

Make sure the following python packages are installed. We recommend using a virtual environment:

```
pip install django
pip install django-crispy-forms
pip install mysqlclient
```
	
NOTE: You must have MySQL already installed on your system. before you can install the python package mysqlclient. See https://pypi.org/project/mysqlclient/ . 

MySQL can be installed here: https://dev.mysql.com/downloads/installer/
	
For windows systems, you’ll need to compile mysqlclient from source, which is hard. Instead, it is easier to download a third party python wheel file for mysqlclient, and then move it to the project folder. (The same folder where the manage.py file is located). Download the latest mysqlclient wheel file from this site https://www.lfd.uci.edu/~gohlke/pythonlibs/ and move the .whl file into the project folder.
Navigate to the directory containing manage.py and input the following command in the command line: 

```
python manage.py runserver
```

Open your preferred browser and go to http://127.0.0.1:8000/gameplanapp/

This is connected to a mqsql database on Google Cloud Platform. To use a local sqlite3 database instead, go to settings.py and insert the following code to the bottom 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
```

Then navigate to the directory containing manage.py and input the following commands

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```




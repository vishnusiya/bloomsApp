#!/bin/bash

cd /home/vishnupriya/projects/shopApp/

source venv/bin/activate 

python -m webbrowser http://127.0.0.1:8000/

python manage.py runserver 

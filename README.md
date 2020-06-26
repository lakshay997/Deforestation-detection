# Installation
For the betterment of the society, we're using virtualenv in conjuntion with virtualenvwrapper

pip install virtualenv virtualenvwrapper (if you're on windows pip install virtualenv virtualenvwrapper-win)
Create new env using mkvirtualenv <envname>
pip install -r requirements.txt
Add the following environment variables (preferably set in on postactivate of env and unset it on predeactivate)
FLASK_ENV=development
FLASK_APP=app.py
MAPBOX_TOKEN=<get your own token> (you might have to reactivate your env after setting these env vars)
Activate the env using workon <envname> (deactivate to get out of virtualenv)

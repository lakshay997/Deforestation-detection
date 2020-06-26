# Installation
For the betterment of the society, we're using virtualenv in conjuntion with virtualenvwrapper

1. pip install virtualenv virtualenvwrapper (if you're on windows pip install virtualenv virtualenvwrapper-win)
2. Create new env using mkvirtualenv <envname>
3. pip install -r requirements.txt
4. Add the following environment variables (preferably set in on postactivate of env and unset it on predeactivate)
5. FLASK_ENV=development
6. FLASK_APP=app.py
7. MAPBOX_TOKEN=<get your own token> (you might have to reactivate your env after setting these env vars)
8. Activate the env using workon <envname> (deactivate to get out of virtualenv)

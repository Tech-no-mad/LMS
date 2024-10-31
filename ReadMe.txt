MAD2
|
|
------code
|	|
|	---- Back
|	|
|	|
|	----front-end
|
|
-----Report


step 1:
npm install

step 2:
pip install -r requirements.txt

backend:
terminal 1
cd / code/Back
    python app.py

terminal 2
cd /code/font-end/npm run serve

wsl
    redis-server


terminal 3
celery -A app.celery worker --loglevel=info
terminal 4
celery -A app.celery beat --loglevel=info
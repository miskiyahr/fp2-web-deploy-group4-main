# Deploy Model

## Starter for Flask run

### If you use git bash

1. export FLASK_APP=app
2. export FLASK_ENV=development
3. flask run

## Deploy to Heroku

1. Pertama login dulu, ini hanya sekali saja
2. ketik heroku create nama-model
3. Buat file requirements.txt yg berisi bahan untuk diinstall
4. procfile, ini ketik aja web:gunicorn app:app
5. Set remote dengan heroku git:remote -a nama-model
6. git push heroku master atau git push heroku main

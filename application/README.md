flask_vue_oracle11HR

Baixar dependencias:
  --pip3 install -r requiremnets.txt
Buildar projeto (Comando na raiz da aplicacao):
  
  GUNICORN:
    --gunicorn --bind 0.0.0.0:8000 --log-config gunicorn.conf app:app
  FLASK:
    --flask run
  PYTHON:
    --python3 app.py

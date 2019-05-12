FROM python:3.6.8-slim-stretch

LABEL maintainer=jonatanvianna

# Configuration for Jupyter
WORKDIR /root/.jupyter/
COPY jupyter_notebook_config.py .

# Creates directory for source code
WORKDIR /app

# Install python dependencies
COPY Pipfile* ./

RUN set -xe \
  && pip3 install pipenv \
  && pipenv install --system --deploy

COPY ["^jupiter*", ".", "/app/"]

EXPOSE 8888


#c.NotebookApp.allow_root = True
#c.NotebookApp.ip = '0.0.0.0'
#c.NotebookApp.password = u'sha1:f7b987e03c85:8a368989b7b70ab1d52d0b722868b6504809daa1'
#c.NotebookApp.open_browser = False
#c.NotebookApp.port = 8888

#jupyter_notebook_config.json
#{
#  "NotebookApp": {
#    "password": "sha1:f7b987e03c85:8a368989b7b70ab1d52d0b722868b6504809daa1"
#  }
#}

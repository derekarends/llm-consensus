FROM python:3.11.4-slim

ENV APP_HOME=/home/appuser

RUN groupadd --gid 1000 appuser \
  && useradd --uid 1000 --gid 1000 -ms /bin/bash appuser

RUN pip3 install --no-cache-dir --upgrade \
  pip \
  virtualenv

USER appuser
WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt

ENV VIRTUAL_ENV=${APP_HOME}/venv
RUN virtualenv ${VIRTUAL_ENV}
RUN . ${VIRTUAL_ENV}/bin/activate && pip install -r $APP_HOME/requirements.txt

EXPOSE 8501

COPY ./web/app $APP_HOME/app
COPY ./web/run.sh $APP_HOME
ENTRYPOINT ["./run.sh"]
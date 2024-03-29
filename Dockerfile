FROM python:3.10.0

WORKDIR /app

RUN pip install --upgrade pip && pip install tox IPython

COPY . /app/

RUN pip install .

ENTRYPOINT ["right-click-save"]

FROM python:3.10.0

WORKDIR /app

RUN pip install --upgrade pip

COPY pkg/ README.md /app/

RUN pip install .

ENTRYPOINT ["right-click-save"]

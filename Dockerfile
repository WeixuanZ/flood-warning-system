FROM python:3

RUN mkdir flood-warning-system

WORKDIR flood-warning-system

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5100

CMD bokeh serve ../flood-warning-system --port 5100

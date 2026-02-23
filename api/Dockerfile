FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./airport_encodings.json /code/airport_encodings.json

COPY ./finalized_model.pkl /code/finalized_model.pkl

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./delay_prediction_api.py /code/delay_prediction_api.py

CMD ["uvicorn", "delay_prediction_api:app", "--host", "0.0.0.0", "--port", "80"]
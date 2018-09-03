FROM python:3.7-alpine

COPY requirements.txt requirements.txt

RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY pageviews pageviews
COPY migrations migrations
COPY config.py .flaskenv .env ./

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]

#Dockerfile: Defines how to build the FastAPI application image.

FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

#Installs FastAPI SQLAlchemy psycopg2 uvicorn inside container.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn App.main:app --host 0.0.0.0 --port 8000"]


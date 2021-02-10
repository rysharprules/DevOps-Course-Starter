FROM python:3.9-buster AS base
RUN mkdir /app
COPY *.toml /app/
WORKDIR /app
RUN pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

FROM base AS dev
WORKDIR /app
EXPOSE 5000
CMD ["poetry", "run", "flask", "run", "-h", "0.0.0.0"]

FROM base AS prod
ENV FLASK_ENV=production
COPY . /app
WORKDIR /app
EXPOSE 8000
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0", "todo_app.app:create_app()"]

FROM base as test
COPY .env.test /app
WORKDIR /app
CMD ["poetry", "run", "pytest", "tests/app_test.py"]
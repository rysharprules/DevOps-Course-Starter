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

FROM base AS test
COPY . /app
WORKDIR /app
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get update && \
    apt-get -f install ./chrome.deb -y && \
    rm ./chrome.deb
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip && \
    apt-get install unzip -y && \
    unzip ./chromedriver_linux64.zip
ENTRYPOINT ["poetry", "run", "pytest"]
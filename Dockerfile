FROM python:3.9.2-slim-buster AS base
RUN mkdir /app
COPY *.toml /app/
WORKDIR /app
RUN pip3 install poetry \
    && poetry config virtualenvs.create false --local \
    && poetry install --no-dev \
    && apt-get update && apt-get install -y curl

FROM base AS dev
WORKDIR /app
EXPOSE 5000
CMD ["poetry", "run", "flask", "run", "-h", "0.0.0.0"]

FROM base AS prod
COPY . /app
WORKDIR /app
ENV PORT=5000
ENTRYPOINT ["sh", "entrypoint.sh"]

FROM base AS test
COPY . /app
WORKDIR /app
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get -f install ./chrome.deb -y && \
    rm ./chrome.deb
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip && \
    apt-get install unzip -y && \
    unzip ./chromedriver_linux64.zip
ENTRYPOINT ["poetry", "run", "pytest"]
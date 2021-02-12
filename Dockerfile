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
COPY . /app
WORKDIR /app
RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    bzip2 \
    && curl -sL 'https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64' | tar -xj -C /opt \
    && ln -s /opt/firefox/firefox /usr/local/bin/
RUN VERSION=$(curl -sL https://api.github.com/repos/mozilla/geckodriver/releases/latest | \
    grep tag_name | cut -d '"' -f 4) \
    && curl -sL "https://github.com/mozilla/geckodriver/releases/download/$VERSION/geckodriver-$VERSION-linux64.tar.gz" | \
    tar -xz -C /app
CMD ["poetry", "run", "pytest"]
#!/bin/bash

docker login -u rysharp -p $DOCKERHUB_PW
docker build --target prod -t rysharp/todo-app:${TRAVIS_COMMIT} .
docker push rysharp/todo-app:${TRAVIS_COMMIT}
docker tag rysharp/todo-app:${TRAVIS_COMMIT} registry.heroku.com/rysharp-todo-app/web
docker push registry.heroku.com/rysharp-todo-app/web
heroku container:release web -a rysharp-todo-app
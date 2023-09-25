FROM ubuntu:latest
LABEL authors="Duke"

ENTRYPOINT ["top", "-b"]
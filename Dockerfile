FROM okteto/python:3
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY code code
ENV PORT=8080
CMD ["python", "-m", "code.api"]
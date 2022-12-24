FROM nikolaik/python-nodejs:python3.10-nodejs17
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  

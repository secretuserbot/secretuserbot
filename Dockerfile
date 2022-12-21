# Faster & Secure & Special Container #
# Thanks to mkaraniya & zakaryan2004

FROM fusuf/asenauserbot:latest
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  

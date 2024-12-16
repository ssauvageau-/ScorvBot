FROM python:3.12.7-alpine3.20

WORKDIR /scorvbot

# Install matplotlib & numpy build dependencies
RUN apk --no-cache --virtual .build-deps add musl-dev linux-headers g++ jpeg-dev zlib-dev libjpeg make

# Intsall discord.py linux voice dependencies
RUN apk --no-cache add libffi python3-dev

# Necessary manual package install for discord.py
RUN pip install --no-cache-dir libnacl

# Install scorvbot python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies once matplotlib is built & installed
RUN apk del .build-deps

# Copy scorvbot source files into working directory
COPY src/ .

# Run scorvbot
CMD [ "python", "bot.py" ]

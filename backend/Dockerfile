FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY backend_static/fonts/Verdana.ttf ./

RUN mkdir -p /usr/share/fonts/truetype/

RUN install -m644 Verdana.ttf /usr/share/fonts/truetype/

RUN rm ./Verdana.ttf

COPY . .

LABEL author='Larkin Michael'

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]

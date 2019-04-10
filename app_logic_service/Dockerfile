FROM python:2.7
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 4010
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN pip install connexion[ui-swagger]  
ENTRYPOINT ["python","index.py"]
FROM python:3-alpine

# create work directory
WORKDIR /app

# copy requirements file 
COPY requirements.txt ./

RUN pip install -r requirements.txt 

# copy app folder 
COPY . . 

EXPOSE 5002

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002", "--debug"]




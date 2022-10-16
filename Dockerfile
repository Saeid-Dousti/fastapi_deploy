FROM python:3.9.7

# everything is going to be done from this directory
WORKDIR /usr/src/app 


# copy requirments.txt from local to docker image in workdirectory
COPY requirements.txt ./

# install requirements this is the longest step
RUN pip install --no-cache-dir -r requirements.txt

# copy everything into workdirectory
COPY . .

# command to run when starting the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
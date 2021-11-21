FROM python:3.8-slim

# Install git, gnupg, curl, and the google cloud SDK
RUN apt-get -y upgrade \
 && apt-get -y update \
 && apt-get install -y \
      build-essential \
      curl \
      git \
      gcc \
      gnupg \
 && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
 && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \
 && apt-get -y update \
 && apt-get install -y google-cloud-sdk

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN python -m pip install --no-cache-dir -r requirements.txt .

# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "nbaspa_app:create_app()"

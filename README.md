# Overview

The repository houses a Flask web app for [nbaspa](https://github.com/ak-gupta/nbaspa).

# Usage

The usage below assumes that you have used `nbaspa` to download and clean your training data, build your
model, and produce impact ratings.

## Basic

Install the requirements via `pip`,

```console
$ python -m pip install -r requirements.txt .
```

set an environment variable to indicate the path to your `nbaspa` data directory,

```console
$ export DATA_DIR=nba-data
```

and launch the web app.

```console
$ python wsgi.py
```

You can change the `--host`, `--port`, and `--config`. The `--config` is either `production` or
`development`, and it refers to the Flask configuration of `config.py`.

## Docker

First, build the docker container

```console
$ docker build --tag nbaspa_app .
```

### Local filesystem

Run the container with the port of your choice.

```console
$ docker run --rm -p 8080:8080 -e PORT=8080 -e DATA_DIR=nba-data nbaspa_app
```

You may need to mount a filesystem to have access to a local data directory:

```console
$ docker run \
    --rm \
    -p 8080:8080 \
    -e PORT=8080 \
    -e DATA_DIR=/opt/nba-data \
    --mount type=bind,src=/opt/<PATH_TO_PARENT_DIRECTORY>,target=/opt \
    nbaspa_app
```

### GCS filesystem

Pull the `gcloud` image:

```console
$ docker pull gcr.io/google.com/cloudsdktool/cloud-sdk:latest
```

and authenticate ``gcloud`` with service account credentials:

```console
$ docker run \
    --name gcloud-config \
    gcr.io/google.com/cloudsdktool/cloud-sdk gcloud auth activate-service-account SERVICE_ACCOUNT@DOMAIN.COM --key-file=/path/key.json --project=PROJECT_ID
```

To change the configuration to point to Google Cloud Storage, supply the `FLASK_CONFIG` environment variable:

```console
$ docker run \
    --rm \
    --volumes-from gcloud-config \
    -p 8080:8080 \
    -e PORT=8080 \
    -e DATA_DIR=<BUCKET_NAME>/<FOLDER_NAME> \
    -e FLASK_CONFIG=production \
    nbaspa_app
```

# Credits

A huge thank you to [Todd Birchard](https://github.com/toddbirchard) for his excellent Flask tutorial
series. In particular, this repository uses

* [Organizing Flask Apps with Blueprints](https://hackersandslackers.com/flask-blueprints/),
* [Demystifying Flask's Application Factory](https://hackersandslackers.com/flask-application-factory/), and
* [The Art of Routing in Flask](https://hackersandslackers.com/flask-routes/)

The docker image used for deploying the web application is adapted from the [Google Cloud Run documentation](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python).
Additionally, this project leverages [bulma](https://bulma.io/) for the styling.

# Overview

The repository houses a Flask web app for [nbaspa](https://github.com/ak-gupta/nbaspa).

# Set up

Assuming you have used `nbaspa` to download and clean your data as well as train your win probability
model, you can install the requirements via `pip`:

```console
$ python -m pip install -r requirements.txt .
```

before setting a environment variables, one to indicate the path to your NBA data

```console
$ export DATA_DIR=nba-data
```

and a secret value

```console
$ export SECRET_KEY=mysecret
```

# Usage

To launch the web app, run

```console
$ python wsgi.py
```

You can change the `--host`, `--port`, and `--config`. The `--config` is either `production` or
`development`, and it refers to the Flask configuration of `config.py`.

# Credits

A huge thank you to [Todd Birchard](https://github.com/toddbirchard) for his excellent Flask tutorial
series. In particular, this repository uses

* [Organizing Flask Apps with Blueprints](https://hackersandslackers.com/flask-blueprints/),
* [Demystifying Flask's Application Factory](https://hackersandslackers.com/flask-application-factory/), and
* [The Art of Routing in Flask](https://hackersandslackers.com/flask-routes/)

Additionally, this project leverages [bulma](https://bulma.io/) for the styling.

#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_CERT=adhoc
export FLASK_RUN_KEY=adhoc
export PATH="$(dirname $(which python3)):$PATH"
flask run

#!/bin/bash
pipenv run env FLASK_APP=remote-cam.py FLASK_ENV=development flask run --host=0.0.0.0
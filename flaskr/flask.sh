#!/usr/bin/env bash
export FLASK_APP=flaskr
export FLASK_DEBUG=true

flask initdb
flask run
#!/usr/bin/env bash
export FLASK_APP=web
export FLASK_DEBUG=true

flask initdb
#flask run
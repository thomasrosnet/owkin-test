#!/bin/sh
export FLASK_APP=app
echo "ENV is set to: "
export FLASK_ENV=development
printenv FLASK_ENV
flask run --debug
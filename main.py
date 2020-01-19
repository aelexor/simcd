from flask import Flask, render_template, redirect, request, flash, url_for
import logging
from logging.handlers import RotatingFileHandler
import json

import modules.get_refs

app = Flask(__name__)

@app.route("/")
def home():
    app.logger.info(app_config["log_level"])
    branches, gitlab_config = modules.get_refs.get_branches()
    return render_template("index.html", branches=branches, gitlab_config=gitlab_config)

@app.route("/", methods=['POST'])
def run_pipeline():
        if request.method == 'POST':
            app.logger.info(app_config["log_level"])
            data = request.form.to_dict()
            return redirect(modules.get_refs.run_pipeline(data)["web_url"], code=302)

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

with open('config/config.json') as ac:
    app_config = json.load(ac)

if __name__ == "__main__":
    handler = RotatingFileHandler(app_config["log_path"], maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host=app_config["listen_ip"], port=app_config["listen_port"])
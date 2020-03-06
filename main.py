import logging
import json
import requests

from gitlab import Gitlab
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, redirect, request, url_for, make_response

import modules.gitlab

app = Flask(__name__)

with open('config/config.json') as ac:
    app_config = json.load(ac)

@app.route("/", methods=['GET', 'POST'])
def home():
    app.logger.info(app_config["log_level"])

    if request.method == 'GET':
        code = request.args.get('code')

        if code != None:
            gitlab_url = request.args.get('state')
            parameters = '/oauth/token?client_id=' + app_config["app_id"] + '&client_secret=' + app_config["secret"] + \
                         '&code=' + code + '&grant_type=authorization_code&redirect_uri=http://' + request.host
            get_token = requests.post(gitlab_url + parameters)
            resp = make_response(redirect(url_for('.deploy', gitlab_url=gitlab_url)))
            resp.set_cookie(''.join(e for e in gitlab_url if e.isalnum()), get_token.json()["access_token"])
            return resp

        else:
            gitlab_config = modules.gitlab.get_config()
            return render_template("index.html", gitlab_config=gitlab_config)

    elif request.method == 'POST':

        try:
            gitlab_url = request.values.get("gitlab_url")
            parameters = "oauth/authorize?client_id=" + app_config["app_id"] + "&redirect_uri=http://" \
                         + request.host + "&response_type=code&state=" + gitlab_url + "&scope=api"
            resp = requests.post(gitlab_url + parameters)
            return redirect(resp.url)

        except Exception as err:
            error = repr(err)
            return internal_error(error)

@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    app.logger.info(app_config["log_level"])
    gitlab_config = modules.gitlab.get_config()
    gitlab_url = request.args.get('gitlab_url')

    if request.method == 'GET':

        try:
            gl_token = request.cookies.get(''.join(e for e in gitlab_url if e.isalnum()))
            gl = Gitlab(gitlab_url, oauth_token=gl_token, ssl_verify=True)
            branches = modules.gitlab.get_refs(gl, gitlab_url)
            projects = [key for key, value in branches.items()]
            return render_template("deploy.html", gitlab_config=gitlab_config, gitlab_url=gitlab_url, branches=branches,
                                   projects=projects)

        except Exception as err:
            error = repr(err)
            return internal_error(error)

    elif request.method == 'POST':
        data = request.form.to_dict()
        vars_list = list()
        for key in data:
            vars_dict = dict()
            if "_name_of_key" in key:
                vars_dict['key'] = key.replace("_name_of_key", "")
                vars_dict['value'] = data[key].replace("_name_of_key", "")
                vars_list.append(vars_dict)

        gl_token = request.cookies.get(''.join(e for e in gitlab_url if e.isalnum()))
        gl = Gitlab(gitlab_url, oauth_token=gl_token, ssl_verify=True)
        project = gl.projects.get(gitlab_config[gitlab_url][data['list_project']]["ID"])
        pipeline = project.pipelines.create({'ref': data["refs"], 'variables': vars_list})
        return redirect(pipeline.web_url)

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error), 500

if __name__ == "__main__":
    handler = RotatingFileHandler(app_config["log_path"], maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host=app_config["listen_ip"], port=app_config["listen_port"], threaded=True)
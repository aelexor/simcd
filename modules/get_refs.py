import json
import requests

def get_branches():
    with open('config/gitlab.json') as gc:
        gitlab_config = json.load(gc)

    creds = {'ids': [], 'tokens': [], 'urls': [], 'projects': []}
    project = {list for list in gitlab_config}
    for pr in project:
        creds["projects"].append(pr)
        for list in gitlab_config[pr]:
            for i in list:
                if i == "TOKEN":
                    creds['tokens'].append(list[i])
                elif i == "ID":
                    creds['ids'].append(list[i])
                elif i == "URL":
                    creds["urls"].append(list[i])

    i = 0
    projects = dict()
    while len(creds['ids']) > i:
        headers = {'PRIVATE-TOKEN': creds['tokens'][i]}
        refs = requests.get(creds['urls'][i] + '/api/v4/projects/' + creds['ids'][i] + '/repository/branches',
                             headers=headers).json()
        tags = requests.get(creds['urls'][i] + '/api/v4/projects/' + creds['ids'][i] + '/repository/tags',
                             headers=headers).json()
        projects[creds["projects"][i]] = [ref['name'] for ref in refs]
        projects[creds["projects"][i]] += [ref['name'] for ref in tags]

        i += 1

    return projects, gitlab_config

def run_pipeline(dict):
    with open('config/gitlab.json') as gc:
        gitlab_config = json.load(gc)

    for list in gitlab_config[dict["gitlab_project_name"]]:
        for key, value in list.items():
            if key == "TOKEN":
                token = value
            elif key == "ID":
                id = value
            elif key == "URL":
                url = value

    variables = ""
    for key in dict:
        if key != "gitlab_project_name" and key != "gitlab_project_url" and key != "gitlab_refs_project":
            variables += ("variables[][key]={key}&variables[][value]={value}&").format(key=key, value=dict[key])

    headers = {'PRIVATE-TOKEN': token}
    run = requests.post(url + 'api/v4/projects/' + id + '/pipeline?ref=' + dict["gitlab_refs_project"] + '&' + variables[0:-1], headers=headers)

    return run.json()
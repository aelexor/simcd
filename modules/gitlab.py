import json

def get_config():
    with open('config/gitlab.json') as gc:
        gitlab_config = json.load(gc)

    return gitlab_config

def get_refs(gl, gitlab_url):
    refs = dict()
    for key, value in get_config()[gitlab_url].items():
        try:
            project = gl.projects.get(get_config()[gitlab_url][key]["ID"])
            branches = list()
            tags = list()
            br = project.branches.list(all=True)
            tg = project.tags.list(all=True)

            i = 0
            while i < len(br):
                branches.append(br[i].name)
                i += 1

            i = 0
            while i < len(tg):
                tags.append(tg[i].name)
                i += 1

            refs[key] = tags + branches

        except:
            continue

    return refs
## Simply application for deploy via gitlab

SIMCD server's configuration in file config/config.json

Gitlab projects's configuration in file config/gitlab.json, for example:
```json
{
  "https://example1.gitlab.ru/": {
    "Project_name_1": {
      "ID": "123",
      "Variables": {
        "VAR_NAME_1": "",
        "VAR_NAME_2": [
          "value_1",
          "value_2",
          "value_3"
        ]
      }
    }
  }
}
```

**"https://example1.gitlab.ru/"** is the URL of the Gitlab.

**Project_name_1** is the name of the Gitlab project.

**ID** is the ID of the Gitlab project.

**Variables** is the dictionary which may contains of the strings or lists in format {key: value}, where key is name of the variable and value is the value.

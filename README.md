## Simply application for deploy via gitlab

SIMCD server's configuration in file config/config.json

Gitlab projects's configuration in file config/gitlab.json, for example:
```json
{
  "App": [
    {
      "ID": "project_id"
    },
    {
      "URL": "https://gitlab.example.com/"
    },
    {
      "TOKEN": "your_private_token"
    },
    {
      "VARIABLE_NAME_1": "string",
      "VARIABLE_NAME_2": ["value_1", "value_2", "value_3"]
    }
  ]
}
```

**APP** is the name of the Gitlab project.

**ID** is the ID of the Gitlab project.

**URL** is the URL of the your Gitlab.

**TOKEN** is the your private access token.

**VARIABLE_NAME** is the key which have be of the string or list value.

There can be several projects and variables, for example:
```json
{
  "App1": [
...
    {
      "VARIABLE_NAME_1": "string",
      "VARIABLE_NAME_2": ["value"]
    }
  ],
  "App2": [
...
    {
      "VARIABLE_NAME_1": "string"
    }
  ],
  "App3": [
...
    {
      "VARIABLE_NAME_1": "string",
      "VARIABLE_NAME_2": ["value1"],
      "VARIABLE_NAME_3": ["value2", "value3"],
    }
  ],
}
```

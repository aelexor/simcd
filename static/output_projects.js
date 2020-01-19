function output_projects(gitlab_config) {
    var select = document.createElement("select").setAttribute("id", "output_projects");

    var option_default = document.createElement("option");
    option_default.setAttribute("hidden", "hidden");
    option_default.setAttribute("selected", "selected");
    var default_choose = document.createTextNode("Choose project");
    option_default.appendChild(default_choose);

    for(let i in Object.keys(gitlab_config)) {
        var key = Object.keys(gitlab_config)[i];
        var value = document.createTextNode(key);
        var option = document.createElement("option");
        option.appendChild(value);

        var element = document.getElementById("output_projects");
        element.appendChild(option);
        element.appendChild(option_default);
    }
}
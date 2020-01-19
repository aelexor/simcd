function output_variables(gitlab_config, branches) {
    const clear_form = document.getElementById("table");
    while (clear_form.firstChild) {
        clear_form.firstChild.remove();
    }

    var select_value = document.getElementById("output_projects");
    var index = select_value.options[select_value.selectedIndex].index;
    var project = select_value.options[select_value.selectedIndex].value;

    var list = Object.values(gitlab_config)[index];
    var list_refs = branches[project];

    var table = document.createElement("table");

    var select_ref = document.createElement("select");
    select_ref.setAttribute("name", "gitlab_refs_project");

    var option_ref = document.createElement("option");
    var option_ref_default = document.createElement("option");
    var choose = document.createTextNode("Choose value");
    option_ref_default.appendChild(choose);
    option_ref_default.setAttribute("hidden", "hidden");
    option_ref_default.setAttribute("selected", "selected");
    option_ref.appendChild(option_ref_default);

    for(let i in list_refs){
        var option_ref_value = document.createElement("option");
        var ref_value = document.createTextNode(list_refs[i]);
        option_ref_value.appendChild(ref_value);
        select_ref.appendChild(option_ref_default)
        select_ref.appendChild(option_ref_value)
    }

    for(let i in Object.keys(list)) {
        var dict = Object.values(list)[i];
        for(let i in Object.keys(dict)) {
            var select = document.createElement("select");
            var option_default = document.createElement("option");
            var choose = document.createTextNode("Choose value");
            option_default.appendChild(choose);
            option_default.setAttribute("hidden", "hidden");
            option_default.setAttribute("selected", "selected");

            var key = Object.keys(dict)[i];
            var value = Object.values(dict)[i];

            if (typeof value == 'object' && value != 'ID' && value != 'URL' && value != 'TOKEN') {
                for(let i in Object.values(value)){
                    var select_value = Object.values(value)[i];
                    td_value = document.createTextNode(select_value);
                    select.setAttribute("name", key)

                    var option = document.createElement("option");
                    option.appendChild(td_value);
                    select.appendChild(option);
                    select.appendChild(option_default);

                    var td_right = document.createElement("td");
                    td_right.appendChild(select);
                }
            } else if (typeof value == 'string' && value == "") {
                var input_value = document.createElement("input");
                input_value.setAttribute("name", key)
                input_value.setAttribute("type", "password")

                var td_right = document.createElement("td");
                td_right.appendChild(input_value);
            } else {
                continue;
            }
            var tr = document.createElement("tr");
            var td_left = document.createElement("td");
            var td_key = document.createTextNode(key);
            td_left.appendChild(td_key)
            tr.appendChild(td_left);
            tr.appendChild(td_right);

            table.appendChild(tr);

            var element = document.getElementById("table");
            element.appendChild(table);
            element.appendChild(select_ref);
        }
    }
}
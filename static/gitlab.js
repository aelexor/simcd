$(document).ready(function(){
    $.fn.list_gitlabs_url = function(gitlab_config){
        $(".js_list_gitlabs_url").select2({
            placeholder: "Select URL of the Gitlab"
        });
        $.each(gitlab_config, function(key, value) {
            $('.js_list_gitlabs_url').append($('<option/>').text(key)).prop('selectedIndex', -1);
        });
    }

    $.fn.log_in = function(){
        $(".js_list_gitlabs_url").change(function(){
            var gitlab_url = $(this).children("option:selected").val();
            $('.js_sign_up').append($('<button class="btn"/>').text("Log In"));
        });
    }

    $.fn.list_projects = function(projects){
        $(".js_list_projects").select2({
            placeholder: "Select project name"
        });
        $.each(projects, function(index, value) {
            $('.js_list_projects').append($('<option/>').text(value)).prop('selectedIndex', -1);
        });
    }

    $.fn.choose_project = function(gitlab_config, gitlab_url, branches){
        $(".js_list_projects").change(function(){
            $('.js_vars').empty();
            $('.js_refs').empty();
            $('.js_run').empty();
            var selectedProject = $(this).children("option:selected").val();
            var table = $('<table style="width:25%"/>');
            $.each(gitlab_config[gitlab_url][selectedProject]["Variables"], function(key, value) {
                if (typeof value == 'string') {
                    var tr = $('<tr/>');
                    var td_left = $('<td/>');
                    var td_right = $('<td/>');
                    var label = $('<label>' + key + '</label>');
                    td_left.append(label);
                    td_right.append($('<input name="'+ key +'_name_of_key" class="vars" type="password" style="width:100%"/>'));
                    tr.append(td_left);
                    tr.append(td_right);
                    table.append(tr);
                }
                else if (typeof value == 'object') {
                    var list = $('<select name="'+ key +'_name_of_key" class="js_select_vars" style="width:100%"/>');
                    var tr = $('<tr/>');
                    var td_left = $('<td/>');
                    var td_right = $('<td/>');
                    var label = $('<label>' + key + '</label>');
                    $.each(value, function(key, value) {
                        list.append($('<option/>').text(value)).prop('selectedIndex', -1);
                    });
                    td_left.append(label);
                    td_right.append(list);
                    tr.append(td_left);
                    tr.append(td_right);
                    table.append(tr);
                }
            });
            $('.js_vars').append(table);
            $('.js_select_vars').select2();

            var list_refs = $('<select name="refs" class="js_select_refs" style="width:25%"/>');
            $.each(branches[selectedProject], function(key, value) {
                list_refs.append($('<option/>').text(value)).prop('selectedIndex', -1);
            });
            $('.js_refs').append(list_refs);
            $('.js_select_refs').select2({
                placeholder: "Select branch or tag"
            });

            $('.js_run').append($('<button class="btn"/>').text("Run pipeline"))
        });
    }
});
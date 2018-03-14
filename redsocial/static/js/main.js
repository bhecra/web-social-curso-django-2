function delete_message(username, message_id) {
    if (confirm("Confirma que quieres borrar el mensaje")) {
        var url = "/" + username + "/message/delete/" + message_id;
        $.getJSON(url, function (json) {
            if (json.status == "success") {
                $("#m-" + message_id).remove();
            }
        });
    }
}
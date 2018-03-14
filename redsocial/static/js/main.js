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

function delete_response(username, response_id) {
    if (confirm("Confirma que quieres borrar la respuesta")) {
        var url = "/" + username + "/response/delete/" + response_id;
        $.getJSON(url, function (json) {
            if (json.status == "success") {
                $("#r-" + response_id).remove();
            }
        });
    }
}

function delete_conversation(username, message_id) {
    if (confirm("Confirma que quieres borrar la conversación")) {
        var url = "/" + username + "/message/delete/" + message_id;
        $.getJSON(url, function (json) {
            if (json.status == "success") {
                window.location.href = "/";
            }
        });
    }
}

$(document).ready(function () {
    $(".btn-like").click(function () {
        var btn = $(this);
        // Creamos la petición asíncrona y cambiamos los likes con la respuesta
        var username = $(this).data('username')
        var message_id = $(this).data('message-id');
        var url = "/" + username + "/message/like/" + message_id;
        $.getJSON(url, function (json) {
            if (json.status == "success") {
                // Recuperamos el hijo span y actualizamos los likes
                $(btn).find('span').text(json.likes);
                // Si hemos hecho un like ponemos el botón verde, sino gris
                if (json.action == "like") {
                    $(btn).removeClass("btn-secondary").addClass("btn-success");
                } else if (json.action == "dislike") {
                    $(btn).removeClass("btn-success").addClass("btn-secondary");
                }
            }
        });
    });
});
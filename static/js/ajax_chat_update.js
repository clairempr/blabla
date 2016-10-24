var chats_table = $('#chats_table tbody');
// keep track of lowest/highest message IDs already displayed on page
var minId = 0;
var maxId = 0;
var numChats = 0;
var busyWithPageUpdate = false;

// Stuff to put CSRFToken in Ajax POST request
//var csrftoken = getCookie('csrftoken');
// Get token from form instead of from cookie,
// so we can use CSRF_COOKIE_HTTPONLY = True
var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function to_post_or_not_to_post() {
    // Submit button only causes a POST if there's no javascript support
    // otherwise use Ajax to send the chat and update the page
    var chat_string = $('#id_chat_string').val();
    if (chat_string != '') {
        send_chat(chat_string);
        $('#id_chat_string').val('');
    }
    // If there's javascript but no websocket connection (Safari?)
    // then we need to initiate chat update now
    if (!websocket_connected) {
        update_chats();
    }
    // We have javascript, so don't submit the form
    return false;
}

$("form input:checkbox").change(function () {
    // filters have changed, so clear everything,
    // set Ids back to zero, and get all relevant chats
    minId = 0;
    maxId = 0;
    update_chats();
});

$("#number_of_chats").change(function () {
    update_chats();
});

function update_chats() {
    if (busyWithPageUpdate)
        return;

    busyWithPageUpdate = true;

    // either we haven't been through this process yet
    // or filters have changed, so clear everything
    if (minId == 0 && maxId == 0) {
        $("#chats_table").find("tr:not(:first)").remove();
    }

    var latest_chats_first = $('#latest_chats_first').prop('checked');
    var just_today = $('#just_today').prop('checked');
    var pirate = $('#pirate').prop('checked');
    var number_of_chats = parseInt($('#number_of_chats').val());
    $.ajax({
        type: "GET",
        dataType: "json",
        data: {
            latest_chats_first: latest_chats_first,
            just_today: just_today,
            pirate: pirate,
            number_of_chats: number_of_chats,
            min_id: minId,
            max_id: maxId
        },
        url: "/ajax_chats_rendered",
        success: function (data) {
            var chats_before = data.chats_before;
            var chats_after = data.chats_after;
            var minIdFromData = data.min_id_sent;
            var maxIdFromData = data.max_id_sent;
            var replacementChar = '\0';

            chats_before = chats_before.split(replacementChar).join('<wbr>');
            chats_after = chats_after.split(replacementChar).join('<wbr>');

            if (latest_chats_first) {
                $(chats_table).prepend(chats_after);
                $(chats_table).append(chats_before);
            }
            else {
                $(chats_table).append(chats_after);
                $(chats_table).prepend(chats_before);
            }

            // If the number of chats we now have is greater than
            // the number we now want, remove some by chatId
            var currentNumChats = 0;
            if (maxId == 0 && minId == 0) {
                currentNumChats = maxIdFromData - minIdFromData + 1;
            }
            else {
                currentNumChats = maxId - minId + 1;
                if (minIdFromData > 0 && minIdFromData < minId) {
                    currentNumChats = currentNumChats + (minId - minIdFromData);
                }
                if (maxIdFromData > 0 && maxIdFromData > maxId) {
                    currentNumChats = currentNumChats + (maxIdFromData - maxId);
                }
            }

            if (currentNumChats > number_of_chats) {
                if (latest_chats_first) {
                    // remove <number_of_chats> chats with lowest Ids
                    var newMinId = Math.max(maxId, maxIdFromData) - number_of_chats + 1;
                    removeChats(minId, newMinId - 1);
                    minId = newMinId;
                }
                else {
                    // remove <number_of_chats> chats with highest Ids
                    var newMaxId = Math.max(maxId - (maxId - number_of_chats), 1);
                    removeChats(newMaxId + 1, maxId);
                    maxId = newMaxId;
                }
            }

            // update variables
            if (minId == 0
                || (minIdFromData > 0 && minIdFromData < minId)) {
                minId = minIdFromData;
            }
            if (maxIdFromData > maxId) {
                maxId = maxIdFromData;
            }
            //alert("minId: " + minId + ", maxId: " + maxId);
            numChats = parseInt(number_of_chats);
            busyWithPageUpdate = false;
        }
    });
}

// remove all chats from startId to endId from page
function removeChats(startId, endId) {
    for (i = startId; i <= endId; i++) {
        $("table#chats_table tr#chat" + i).remove();
    }
}

function send_chat(chat_string) {
    $.ajax({
        type: "POST",
        data: {
            chat_string: chat_string
        },
        url: "/send_chat/",
        success: function (data) {
        }
    });
}

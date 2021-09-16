async function get_notification(notification){
    var base = window.location.origin + '/hod/latest_notification';
    $.ajax({
        url: base,
        type: 'GET',
        async: true,
        data: {"which_notification": notification},
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            if(notification=='exam'){
                $("#enotification-dimmer").removeClass("dimmer")
                $("#enotification-display").html(result)
            }
            else{
                $("#notification-dimmer").removeClass("dimmer")
                $("#notification-display").html(result)
            }
        },
        error: function(result){
            if(notification=='exam'){
                $("#fetch-exam").html("Failed to fectch")
            }
            else{
                $("#fetch-noti").html("Failed to fectch")
            }
        }
    })
}
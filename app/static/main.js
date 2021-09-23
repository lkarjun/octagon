function startStreaming() {

    var mediaSupport = 'mediaDevices' in navigator;

    if( mediaSupport && null == cameraStream ) {
        navigator.mediaDevices.getUserMedia( { video: true } )
        .then( function( mediaStream ) {
            cameraStream = mediaStream;
            stream.srcObject = mediaStream;
            stream.play();
        })
            .catch( function( err ) {
            $("#btn_login").hide()
            alert("Unable to access camera: " + err );
            console.log( "Unable to access camera: " + err );
        });
        }
    else {
        alert( 'Your browser does not support media devices.' );
        return;
    }
    }

// Stop Streaming
function stopStreaming() {

    if( null != cameraStream ) {

        var track = cameraStream.getTracks()[ 0 ];

        track.stop();
        stream.load();
        cameraStream = null;
    }
    }

function captureSnapshot() {

        if( null != cameraStream ) {

        var ctx = capture.getContext( '2d' );
        var img = new Image();

        ctx.drawImage( stream, 0, 0, capture.width, capture.height );
        var dataURL = capture.toDataURL("image/jpeg");
        return dataURL;
    }
}

function upload(image_data){
    $("#btn_login").addClass("loading disabled");
    user = $('#username').val()
    data = JSON.stringify({"file": image_data.split(',')[1], "username": user});
    $.ajax({
        type: 'POST',
        url: '/login',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(data){
            window.location.href = window.location.origin + data;
        },
        error: function(data){
            swal("Not authorized. So, reloading page").then((value) => {location.reload();});
        },
    })
}


function capit(){
    $("#btn_login").hide()
    data = captureSnapshot();
    stopStreaming();
    if ($('#username').val() == null){
        swal(`Kindly please choose you're name from the select box. 
              If you're name is not there then please contact 
              admin or techincal staff.`).then((value) => {location.reload();});
    }
    else{
        $("#recognizing-spinner").show()
        $("#password").val(data.split(',')[1])
    }
}

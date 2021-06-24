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
        url: '/analyse',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(data){
            if (data == true){
                window.location.href = '/workspace'
            }
            console.log(data);
            alert(data);
        },
        error: function(data){
        alert(data);
        },
    })
}


function capit(){
    data = captureSnapshot();
    stopStreaming();
    upload(data);
}
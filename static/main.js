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
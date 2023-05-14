// Set constraints for the video stream
var constraints =
{
    video:{
        width: 1920,
        height: 1080 ,
        frameRate:30,
        facingMode: "environment", 
        audio: false,
        aspectRatio:0.5625 
    }
};
// Define constants
const cameraView = document.querySelector("#camera--view");
    cameraOutput = document.querySelector("#camera--output");
    cameraSensor = document.querySelector("#camera--sensor");
    cameraTrigger = document.querySelector("#camera--trigger");
    cancelButton = document.querySelector("#cancel-button");
    confirmButton = document.querySelector("#confirm-button");
    clickPhotoSection = document.querySelector("#clickPhoto");
    clickPhotoConfirmSection = document.querySelector("#clickPhotoConfirm");
    productStatusModal = document.querySelector("#productStatusModal");
    modalBody = document.querySelector("#clickPhotoConfirm");
// Access the device camera and stream to cameraView
function cameraStart() {
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream
    })
    .catch(function(error) {
        $('#Error404').modal('show');
        $('#Error404').find('.modal-title').text("Oops. Something is broken.", error); 
        console.log("Oops. Something is broken.", error);
    });
}
// Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/png");
    cameraOutput.classList.add("taken");
    clickPhotoSection.style.display = "none";
    clickPhotoConfirmSection.style.display = "flex";
    cameraOutput.style.display = "block";
};

// Take a picture when cameraTrigger is tapped
cancelButton.onclick = function() {
    clickPhotoSection.style.display = "flex";
    clickPhotoConfirmSection.style.display = "none";
    cameraOutput.style.display = "none";
};

confirmButton.onclick = function() {
    var imagebase64data = cameraOutput.src;  
    imagebase64data = imagebase64data.replace('data:image/png;base64,', '');  
    jQuery.ajax({  
        type: 'POST',  
        url: '/upload', 
        data:{"image_data": imagebase64data},  
        contentType: 'application/x-www-form-urlencoded',   
        success: function (out) {  
            $('#productStatusModal').modal('show');
            $('#productStatusModal').find('.modal-title').text(out.status);
        },
        error: function (out) {  
            $('#productStatusModalUnsuccesfull').modal('show');
            $('#productStatusModalUnsuccesfull').find('.modal-title').text("Upload unsuccessful!!");      
        } 
    });
    cancelButton.click();
};

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);
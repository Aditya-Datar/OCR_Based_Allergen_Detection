// Set constraints for the video stream
var constraints =
{
    video:{
        frameRate:30,
        facingMode: "environment", 
        audio: false
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
    document.getElementById("image-upload").click();
    clickPhotoSection.style.display = "none";
    clickPhotoConfirmSection.style.display = "flex";
    cameraOutput.style.display = "block";
    cameraOutput.style.width = "100%";
    cameraOutput.style.height = "70%";
};

// Take a picture when cameraTrigger is tapped
cancelButton.onclick = function() {
    clickPhotoSection.style.display = "flex";
    clickPhotoConfirmSection.style.display = "none";
    cameraOutput.style.display = "none";
};

confirmButton.onclick = function() {
    $('#loadingModal').modal('show');
    $('#loadingModal').find('.modal-title').text("Computing Results 🔃");
    var imagebase64data = cameraOutput.src;  
    imagebase64data = imagebase64data.replace('data:image/jpeg;base64,', '');
    console.log({"image_data": imagebase64data, "windowWidth": window.innerWidth, "windowHeight":(window.innerHeight * 0.7)});
    jQuery.ajax({  
        type: 'POST',  
        url: '/upload', 
        data:{"image_data": imagebase64data, "windowWidth": window.innerWidth, "windowHeight":(window.innerHeight * 0.7)},  
        contentType: 'application/x-www-form-urlencoded',   
        success: function (out) {  
            if(out.status)
            {
                $('#productSafe').modal('show');
                $('#productSafe').find('.modal-title').text("Product is safe to use ✅");
            }
            else
            {
                $('#productNotSafe').modal('show');
                $('#productNotSafe').find('.modal-title').text("Product is not safe to use ❌");
            }
            
        },
        error: function (out) {  
            setTimeout(function () {
                $('#loadingModal').modal('hide');
            }, 1000);
            $('#productStatusModalUnsuccesfull').modal('show');
            $('#productStatusModalUnsuccesfull').find('.modal-title').text("Upload unsuccessful!!");
            

        } 
    }).done(() => {
        $('#loadingModal').modal('hide');
    });
    cancelButton.click();
};

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);
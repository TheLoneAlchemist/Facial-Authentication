
var base64_image = null;
console.log("starting app");

(function () {
    var width = 320;
    var height = 0;
    var streaming = false;
    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;

    function startup() {
        video = document.getElementById('video');
        canvas = document.getElementById('canvas');
        photo = document.getElementById('photo');
        startbutton = document.getElementById('startbutton');

        navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (error) {
                console.log("Error Stream: " + error)
            });

        video.addEventListener('canplay', function (ev) {
            if (!streaming) {
                height = video.videoHeight / (video.videoWidth / width);

                if (isNaN(height)) {
                    height = width / (4 / 3);
                }

                video.setAtrribute('width', width);
                video.setAtrribute('height', height);
                canvas.setAtrribute('width', width);
                canvas.setAtrribute('height', height);
                streaming = true;
            }
        }, false);

        startbutton.addEventListener('click', function (ev) {
            console.log("Capturing image")

            takepicture();
            ev.preventDefault();
        }, false);
        clearphoto();
    }

    function clearphoto() {
        var context = canvas.getContext('2d');
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);

        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
    }

    function takepicture() {

        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            var data = canvas.toDataURL('image/png');
            photo.setAttribute('src', data);
            document.getElementById('imgstring').value = canvas.toDataURL()
            base64_image = canvas.toDataURL()
        }
        else {
            clearphoto();
        }
    }
    startup()




})()

console.log($('input[name = csrfmiddlewaretoken]').val())
$(document).on('submit', '#post-form', function (e) {
    let email = document.getElementById('email');
    console.log("________________________________________")
    console.log(email.value)
    let image64 = document.getElementById('imgstring').value;
    console.log(image64)

    // $.ajax({
    //     type: "POST",
    //     url: "/signup",
    //     csrfmiddlewaretoken: $('input[name = csrfmiddlewaretoken]').val(),
    //     data: { email: email, image64: "hii" }
    // })

    e.preventDefault();
    $.ajax({
        method: "POST",
        url: "/signup",
        headers: { "X-CSRFToken": $('input[name = csrfmiddlewaretoken]').val() },

        data: {
            fname: $('#fname').val(),
            lname: $('#lname').val(),
            email: $('#email').val(),
            password1: $('#password1').val(),
            password2: $('#password2').val(),
            image64: $('#imgstring').val(),
        },
        success: function (data) {
            $('#notify').removeAttr('hidden')
            if (data == 'signup') {
                $('#notify').attr('class','bg-green-100');
                $('#msg').html('Sign up Successful! Redirecting to home page... ');
                var delay = 2000;
                var url = "/login";
                setTimeout(function () {
                    window.location = url;
                }, delay);
            } else {

                $('#msg').html(data);
            }
        },
        error: function () {
            console.log("Something went wrong!...")
        }
    })


});

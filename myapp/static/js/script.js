/* document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const audioPlayer = document.getElementById('audioPlayer');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(uploadForm);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                audioPlayer.src = data.audio_url;
                audioPlayer.controls = true;
            } else {
                alert('Error processing PDF. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


$( function()
{
    $( 'audio' ).audioPlayer();
}); */
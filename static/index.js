document.addEventListener("DOMContentLoaded", (event) => {
    const recordButton = document.getElementById('recordButton');
    const transcriptDiv = document.getElementById('transcript');
    const signLanguageAnimationDiv = document.getElementById('signLanguageAnimation');

    let recognition;
    let mediaRecorder;
    let audioChunks = [];

    function startRecording() {
        console.log("Recording started");

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function(stream) {
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
                mediaRecorder.addEventListener('dataavailable', function(event) {
                    audioChunks.push(event.data);
                });
                mediaRecorder.start();
            })
            .catch(function(error) {
                console.error('Error accessing microphone:', error);
            });

        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function(event) {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            transcriptDiv.innerHTML = finalTranscript + '<span style="color: gray;">' + interimTranscript + '</span>';
        };

        recognition.start();
    }

    function stopRecording() {
        console.log("Recording stopped");
        mediaRecorder.stop();
        recognition.stop();

        mediaRecorder.addEventListener('stop', function() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioChunks = [];

            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');

            $.ajax({
                url: '/transcribe',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    if (response.error) {
                        transcriptDiv.innerHTML = 'Error: ' + response.error;
                    } else {
                        transcriptDiv.innerHTML = response.transcript;


                        console.log("Transcribed Text", response.transcript)


                        // Send the transcribed text to the text-to-sign-language route
                        $.ajax({
                            url: '/text_to_sign_language',
                            type: 'POST',
                            data: { text: response.transcript },
                            success: function(response) {
                                
                                
                                console.log("Animation Message", response)

                                // Update the sign language animation div with the generated HTML
                                signLanguageAnimationDiv.innerHTML = response.animation;
                            },

                            error: function(xhr, status, error) {


                                console.error('This is your Error:', error);
                            }
                        });
                    }
                },
                error: function(xhr, status, error) {

                    console.log("Error is right here 3")

                    console.error('Error:', error);
                }
            });
        });
    }

    recordButton.addEventListener('mousedown', startRecording);
    recordButton.addEventListener('mouseup', stopRecording);
});
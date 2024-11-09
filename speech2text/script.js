let mediaRecorder;
let audioChunks = [];
const recordButton = document.getElementById('recordButton');
const statusText = document.getElementById('status');
const resultsDiv = document.getElementById('results');
const audioPlayer = document.getElementById('audioPlayer');

recordButton.addEventListener('click', async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    statusText.textContent = "Recording...";
    recordButton.textContent = "Stop Recording";

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioFile = new File([audioBlob], 'recording.mp3', { type: 'audio/mp3' });
        await sendAudio(audioFile);
        audioChunks = [];
    };

    mediaRecorder.start();
}

function stopRecording() {
    statusText.textContent = "Stopped";
    recordButton.textContent = "Start Recording";
    mediaRecorder.stop();
}

async function sendAudio(audioFile) {
    statusText.textContent = "Sending audio...";
    const formData = new FormData();
    formData.append('audio', audioFile);

    try {
        const response = await fetch('http://127.0.0.1:5000/transcribe', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();  // Parsing the response as JSON

        if (result.status === "incomplete") {
            // Caso con chiavi mancanti
            resultsDiv.innerHTML = `
                <p>The following keys are missing: ${result.missing_keys.join(", ")}</p>
                `;

            if (result.audio) {
                // Decodifica e carica l'audio nel player
                const audioBlob = base64ToBlob(result.audio, "audio/mp3");
                const audioURL = URL.createObjectURL(audioBlob);
                audioPlayer.src = audioURL;
                audioPlayer.style.display = "block"; // Mostra il player audio
            }

        } else if (result.status === "complete") {
            // Caso con tutte le chiavi presenti
            resultsDiv.innerHTML = `
                <p>All keys are present.</p>
                <pre>${JSON.stringify(result.data, null, 2)}</pre>
                `;
            audioPlayer.style.display = "none"; // Nascondi il player audio
        }

    } catch (error) {
        console.error('Error sending audio:', error);
        statusText.textContent = "Error sending audio.";
    }
}

// Funzione per convertire la stringa base64 in un Blob audio
function base64ToBlob(base64, mimeType) {
    const byteCharacters = atob(base64);
    const byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
        const slice = byteCharacters.slice(offset, offset + 512);
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }
        byteArrays.push(new Uint8Array(byteNumbers));
    }
    return new Blob(byteArrays, { type: mimeType });
}

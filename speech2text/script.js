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

       const result = await response.json(); // Parsing della risposta come JSON

        if (result.status === "incomplete" || result.status === "complete") {
            displayResults(result);
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

function displayResults(data) {
    // Svuota il contenuto attuale di resultsDiv
    resultsDiv.innerHTML = "";

    // Ottieni il JSON completo dalla risposta
    const fullJson = data.data;

    // Genera dinamicamente input per ogni chiave del JSON
    for (const [key, value] of Object.entries(fullJson)) {
        const inputContainer = document.createElement('div');
        inputContainer.classList.add('input-container');

        const label = document.createElement('label');
        label.textContent = key;

        const input = document.createElement('input');
        input.type = 'text';
        input.value = value || ""; // Lascia vuoti i campi mancanti

        inputContainer.appendChild(label);
        inputContainer.appendChild(input);
        resultsDiv.appendChild(inputContainer);
    }

    // Visualizza i campi mancanti
    if (data.missing_keys.length > 0) {
        const missingMessage = document.createElement('p');
        missingMessage.textContent = `Mancano i seguenti campi: ${data.missing_keys.join(', ')}`;
        resultsDiv.appendChild(missingMessage);
    }

    // Mostra l'audio solo se incluso nella risposta
    if (data.audio) {
        const audioBlob = base64ToBlob(data.audio, "audio/mp3");
        const audioURL = URL.createObjectURL(audioBlob);
        audioPlayer.src = audioURL;
        audioPlayer.style.display = "block"; // Mostra il player audio
    } else {
        audioPlayer.style.display = "none"; // Nascondi il player audio se non incluso
    }
}

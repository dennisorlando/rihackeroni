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


        // Ottieni il contenitore dei campi
        const fieldsContainer = document.getElementById('fieldsContainer');
        fieldsContainer.innerHTML = ''; // Svuota il contenitore prima di riempirlo con nuovi dati

        if (result.status === "incomplete") {
            // Caso con chiavi mancanti
            resultsDiv.innerHTML = `
                <p>The following keys are missing: ${result.missing_keys.join(", ")}</p>
                `;

             displayFields(result.missing_keys, true); // Mostra i campi mancanti



        } else if (result.status === "complete") {
            // Caso con tutte le chiavi presenti
            resultsDiv.innerHTML = `
                <p>All keys are present.</p>
                <pre>${JSON.stringify(result.data, null, 2)}</pre>
                `;
           displayFields(result.data, false); // Mostra i dati completi
        }
 audioPlayer.style.display = "none"; 

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

function displayFields(data, isMissing) {
    const fieldsContainer = document.getElementById('fieldsContainer');

    // Itera su ogni chiave nel dato ricevuto
    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            // Crea un box per ogni campo
            const fieldWrapper = document.createElement('div');
            fieldWrapper.classList.add('field-wrapper');

            // Crea un label per il campo
            const label = document.createElement('label');
            label.setAttribute('for', key);
            label.textContent = key;

            // Crea un box di input (vuoto per i campi mancanti, compilato per i dati completi)
            const input = document.createElement('input');
            input.type = 'text';
            input.id = key;
            input.name = key;
            input.value = isMissing ? '' : data[key]; // Se mancante, lascia il campo vuoto, altrimenti metti il valore

            // Aggiungi il label e l'input nel contenitore
            fieldWrapper.appendChild(label);
            fieldWrapper.appendChild(input);
            fieldsContainer.appendChild(fieldWrapper);
        }
    }
}

/* ========================================
   ISITTRUE - FRONTEND APPLICATION
   ======================================== */

// ===== TAB SWITCHING =====
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and contents
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        btn.classList.add('active');
        const tabId = btn.getAttribute('data-tab') + '-tab';
        document.getElementById(tabId).classList.add('active');
        
        // Clear results when switching tabs
        clearResult();
    });
});

// ===== TEXT ANALYSIS =====
async function analyzeText() {
    const text = document.getElementById('textInput').value.trim();
    
    if (!text) {
        showError('Veuillez entrer un texte');
        return;
    }
    
    await sendAnalysisRequest({ text });
}

// ===== URL ANALYSIS =====
async function analyzeUrl() {
    const url = document.getElementById('urlInput').value.trim();
    
    if (!url) {
        showError('Veuillez entrer une URL');
        return;
    }
    
    if (!isValidUrl(url)) {
        showError('URL invalide');
        return;
    }
    
    await sendAnalysisRequest({ text: url });
}

// ===== IMAGE HANDLING =====
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const imageCaption = document.getElementById('imageCaption');
const analyzeImageBtn = document.getElementById('analyzeImageBtn');

// Upload area events
uploadArea.addEventListener('click', () => imageInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.opacity = '0.7';
});
uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.opacity = '1';
});
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.opacity = '1';
    if (e.dataTransfer.files.length > 0) {
        handleImageSelect(e.dataTransfer.files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleImageSelect(e.target.files[0]);
    }
});

function handleImageSelect(file) {
    if (!file.type.startsWith('image/')) {
        showError('Veuillez sélectionner une image');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        uploadArea.style.display = 'none';
        imagePreview.style.display = 'block';
        analyzeImageBtn.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

async function analyzeImage() {
    if (!previewImg.src) {
        showError('Veuillez sélectionner une image');
        return;
    }
    
    const caption = imageCaption.value.trim();
    await sendAnalysisRequest({
        text: caption,
        image: previewImg.src
    });
}

// ===== AUDIO HANDLING =====
let mediaRecorder;
let audioChunks = [];
let recordingStartTime;
let timerInterval;

const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const recordingTime = document.getElementById('recordingTime');
const timer = document.getElementById('timer');
const audioPlayer = document.getElementById('audioPlayer');
const audioPlayback = document.getElementById('audioPlayback');
const audioInput = document.getElementById('audioInput');
const analyzeAudioBtn = document.getElementById('analyzeAudioBtn');

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioUrl;
            audioPlayback.style.display = 'block';
            analyzeAudioBtn.style.display = 'block';
            
            // Stop stream
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        recordBtn.style.display = 'none';
        stopBtn.style.display = 'block';
        recordingTime.style.display = 'block';
        recordingStartTime = Date.now();
        startTimer();
    } catch (e) {
        showError('Erreur d\'accès au microphone: ' + e.message);
    }
}

function stopRecording() {
    mediaRecorder.stop();
    recordBtn.style.display = 'block';
    stopBtn.style.display = 'none';
    recordingTime.style.display = 'none';
    clearInterval(timerInterval);
}

function startTimer() {
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        timer.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 100);
}

audioInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        const audioUrl = URL.createObjectURL(file);
        audioPlayer.src = audioUrl;
        audioPlayback.style.display = 'block';
        analyzeAudioBtn.style.display = 'block';
    }
});

async function analyzeAudio() {
    const audioSrc = audioPlayer.src;
    if (!audioSrc) {
        showError('Veuillez enregistrer ou charger un audio');
        return;
    }
    
    try {
        // Convert audio URL to blob
        const response = await fetch(audioSrc);
        const blob = await response.blob();
        const reader = new FileReader();
        
        reader.onload = async (e) => {
            await sendAnalysisRequest({
                text: '',
                audio: e.target.result
            });
        };
        reader.readAsDataURL(blob);
    } catch (e) {
        showError('Erreur lors du traitement de l\'audio');
    }
}

// ===== API COMMUNICATION =====
async function sendAnalysisRequest(data) {
    showLoading();
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erreur serveur');
        }
        
        const result = await response.json();
        showResult(result.result);
    } catch (error) {
        showError(error.message || 'Erreur lors de l\'analyse');
    } finally {
        hideLoading();
    }
}

// ===== UI HELPERS =====
function showLoading() {
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('errorContainer').style.display = 'none';
    document.getElementById('loadingContainer').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingContainer').style.display = 'none';
}

function showResult(text) {
    document.getElementById('errorContainer').style.display = 'none';
    document.getElementById('resultText').textContent = text;
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('resultContainer').scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('loadingContainer').style.display = 'none';
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorContainer').style.display = 'block';
}

function clearResult() {
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('errorContainer').style.display = 'none';
    document.getElementById('loadingContainer').style.display = 'none';
    document.getElementById('textInput').value = '';
    document.getElementById('urlInput').value = '';
    document.getElementById('imageCaption').value = '';
    
    // Reset image preview
    uploadArea.style.display = 'block';
    imagePreview.style.display = 'none';
    analyzeImageBtn.style.display = 'none';
    previewImg.src = '';
    
    // Reset audio
    audioPlayback.style.display = 'none';
    analyzeAudioBtn.style.display = 'none';
    audioPlayer.src = '';
}

// ===== VALIDATION =====
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeTab = document.querySelector('.tab-btn.active').getAttribute('data-tab');
        
        switch(activeTab) {
            case 'text':
                analyzeText();
                break;
            case 'url':
                analyzeUrl();
                break;
            case 'image':
                analyzeImage();
                break;
            case 'audio':
                analyzeAudio();
                break;
        }
    }
});

// ===== INITIALIZATION =====
console.log('✅ IsItTrue Frontend Initialized');

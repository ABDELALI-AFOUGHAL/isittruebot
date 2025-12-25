// ==================== IsItTrue v4.0 JavaScript ====================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Bind form submission
    document.getElementById('analysisForm').addEventListener('submit', handleFormSubmit);
    
    // Bind temperature change
    document.getElementById('temperature').addEventListener('change', function() {
        this.nextElementSibling.textContent = (parseFloat(this.value) * 100).toFixed(0) + '%';
    });
    
    // Hide error on text input
    document.getElementById('textInput').addEventListener('input', function() {
        document.getElementById('errorSection').classList.add('d-none');
    });
    
    console.log('✅ IsItTrue v4.0 initialized');
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const text = document.getElementById('textInput').value.trim();
    const requestType = document.querySelector('input[name="requestType"]:checked').value;
    const temperature = parseFloat(document.getElementById('temperature').value);
    
    // Validate input
    if (!text) {
        showError('Please enter some text to analyze');
        return;
    }
    
    // Show loading
    showLoading(true);
    hideResults();
    hideError();
    
    try {
        const payload = {
            text: text,
            request_type: requestType,
            temperature: temperature
        };
        
        console.log('📨 Sending request:', payload);
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            timeout: 45000
        });
        
        const data = await response.json();
        console.log('📥 Response received:', data);
        
        showLoading(false);
        
        if (!response.ok) {
            showError(data.error || `Server error: ${response.status}`);
            return;
        }
        
        if (data.success === false || data.error) {
            showError(data.error || 'Unknown error occurred');
            return;
        }
        
        // Show results
        showResults(data.result, data.type);
        
    } catch (error) {
        showLoading(false);
        console.error('❌ Request error:', error);
        showError(`Network error: ${error.message}`);
    }
}

/**
 * Show loading spinner
 */
function showLoading(show) {
    const section = document.getElementById('loadingSection');
    if (show) {
        section.classList.remove('d-none');
    } else {
        section.classList.add('d-none');
    }
}

/**
 * Show results
 */
function showResults(result, type) {
    document.getElementById('resultContent').textContent = result;
    document.getElementById('resultType').textContent = `Type: ${formatType(type)}`;
    document.getElementById('resultsSection').classList.remove('d-none');
    
    // Scroll to results
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').classList.remove('d-none');
}

/**
 * Hide results
 */
function hideResults() {
    document.getElementById('resultsSection').classList.add('d-none');
}

/**
 * Hide error
 */
function hideError() {
    document.getElementById('errorSection').classList.add('d-none');
}

/**
 * Reset form
 */
function resetForm() {
    document.getElementById('analysisForm').reset();
    document.getElementById('textInput').focus();
    hideResults();
    hideError();
}

/**
 * Format request type for display
 */
function formatType(type) {
    const types = {
        'fact_check': '✓ Fact-Check',
        'ai_detection': '🤖 AI Detection',
        'general_chat': '💬 General Chat'
    };
    return types[type] || type;
}

/**
 * Add keyboard shortcut: Ctrl+Enter to submit
 */
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('analysisForm');
        if (form) form.dispatchEvent(new Event('submit'));
    }
});

// Log app info
console.log('%c🤖 IsItTrue v4.0', 'font-size: 16px; font-weight: bold; color: #0066cc;');
console.log('%cFriendly AI Agent | Fact-Checking | AI Detection | General Chat', 'color: #666;');

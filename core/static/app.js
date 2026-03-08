// --- SYMBIOTE OS: FRONTEND KERNEL ---

/**
 * HEARTBEAT: Checks if the AI Engine is online.
 * Updates the #status-led and #status-text based on the backend /status endpoint.
 */
async function updateStatus() {
    try {
        const response = await fetch('/status');
        const data = await response.json();
        const led = document.getElementById('status-led');
        const statusText = document.getElementById('status-text');

        if (data.status === 'online') {
            led.style.backgroundColor = '#00f2ff'; // Electric Blue
            led.style.boxShadow = '0 0 15px #00f2ff, 0 0 30px #00f2ff';
            if (statusText) statusText.innerText = 'AI ENGINE: ACTIVE';
        } else {
            led.style.backgroundColor = '#ff4444'; // Tactical Red
            led.style.boxShadow = '0 0 10px #ff4444';
            if (statusText) statusText.innerText = 'AI ENGINE: OFFLINE';
        }
    } catch (err) {
        console.error("Status Check Failed:", err);
    }
}

/**
 * INTELLIGENCE RETRIEVAL: Sends the query to the RAG engine.
 * Maps to your HTML function askBrain().
 */
async function askBrain() {
    const input = document.getElementById('queryInput');
    const output = document.getElementById('queryResponse');
    const question = input.value.trim();

    if (!question) return;

    output.innerHTML = `<span style="color: #00f2ff;">ANALYZING NEURAL NODES...</span>`;
    
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();
        
        // Render Gemini's synthesis
        output.innerHTML = `<div class="fade-in">${data.answer}</div>`;
    } catch (err) {
        output.innerHTML = `<span style="color: #ff4444;">SYNTHESIS ERROR: Core Connection Timeout.</span>`;
    }
}

/**
 * TERMINAL COMMANDS: Processes commands from the bottom terminal.
 * Maps to your HTML function runCmd().
 */
async function runCmd() {
    const input = document.getElementById('term-input');
    const output = document.getElementById('term-output');
    const cmd = input.value.trim();

    if (!cmd) return;

    // Display local command echo
    output.innerHTML += `<div><span style="color: #00f2ff;">></span> ${cmd}</div>`;
    input.value = '';

    try {
        const response = await fetch('/terminal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: cmd })
        });
        const data = await response.json();
        
        output.innerHTML += `<div style="color: #aaa; margin-bottom: 10px;">${data.output}</div>`;
        output.scrollTop = output.scrollHeight; 
    } catch (err) {
        output.innerHTML += `<div style="color: #ff4444;">SYSTEM ERROR: Terminal interface failure.</div>`;
    }
}

/**
 * HELPER: Fills the query input when a project card is clicked.
 */
function autoFillQuery(projectName) {
    const input = document.getElementById('queryInput');
    input.value = `Give me a tactical summary of project ${projectName}`;
    input.focus();
}

// --- INITIALIZATION ---

// Poll status every 5 seconds to keep the LED updated
setInterval(updateStatus, 5000);

// Initialize system on window load
window.onload = () => {
    updateStatus();
    console.log("Symbiote OS Frontend Loaded.");
};
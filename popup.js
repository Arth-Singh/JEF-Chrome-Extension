document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('textInput');
    const testType = document.getElementById('testType');
    const runButton = document.getElementById('runTest');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    const errorDiv = document.getElementById('error');

    runButton.addEventListener('click', async function() {
        const text = textInput.value.trim();
        const selectedTest = testType.value;

        if (!text) {
            showError('Please enter some text to test.');
            return;
        }

        hideAll();
        showLoading();

        try {
            const response = await chrome.runtime.sendMessage({
                action: 'runTest',
                test: selectedTest,
                text: text
            });

            if (response.success) {
                displayResults(response.result, selectedTest);
            } else {
                showError(response.error || 'An error occurred while running the test.');
            }
        } catch (error) {
            showError('Failed to communicate with the extension. Please try again.');
            console.error('Error:', error);
        }
    });

    function showLoading() {
        loadingDiv.classList.remove('hidden');
    }

    function hideLoading() {
        loadingDiv.classList.add('hidden');
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        hideLoading();
    }

    function hideAll() {
        errorDiv.classList.add('hidden');
        resultsDiv.classList.add('hidden');
        hideLoading();
    }

    function displayResults(result, testType) {
        hideLoading();
        resultsDiv.classList.remove('hidden');
        
        let html = '';
        
        if (result.score !== undefined) {
            html += `<div class="result-item">
                <strong>Score:</strong> ${result.score.toFixed(2)}
            </div>`;
        }
        
        if (result.percentage !== undefined) {
            html += `<div class="result-item">
                <strong>Percentage:</strong> ${result.percentage.toFixed(2)}%
            </div>`;
        }
        
        if (result.total_possible_score !== undefined) {
            html += `<div class="result-item">
                <strong>Total Possible Score:</strong> ${result.total_possible_score}
            </div>`;
        }
        
        if (result.matches && result.matches.length > 0) {
            html += `<div class="result-item">
                <strong>Matches Found:</strong>
                <ul>`;
            result.matches.forEach(match => {
                html += `<li>${escapeHtml(match)}</li>`;
            });
            html += `</ul></div>`;
        }
        
        if (result.missing && result.missing.length > 0) {
            html += `<div class="result-item">
                <strong>Missing Elements:</strong>
                <ul>`;
            result.missing.forEach(item => {
                html += `<li>${escapeHtml(item)}</li>`;
            });
            html += `</ul></div>`;
        }
        
        if (testType === 'score') {
            if (result.tiananmen_score !== undefined) {
                html += `<div class="result-item">
                    <strong>Tiananmen Score:</strong> ${result.tiananmen_score.toFixed(2)}
                </div>`;
            }
            if (result.nerve_agent_score !== undefined) {
                html += `<div class="result-item">
                    <strong>Nerve Agent Score:</strong> ${result.nerve_agent_score.toFixed(2)}
                </div>`;
            }
            if (result.meth_score !== undefined) {
                html += `<div class="result-item">
                    <strong>Methamphetamine Score:</strong> ${result.meth_score.toFixed(2)}
                </div>`;
            }
            if (result.harry_potter_score !== undefined) {
                html += `<div class="result-item">
                    <strong>Harry Potter Score:</strong> ${result.harry_potter_score.toFixed(2)}
                </div>`;
            }
        }
        
        resultsContent.innerHTML = html;
    }
    
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
});
// script.js
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const text = document.getElementById('textInput').value.trim();
    const mood = document.querySelector('.emoji-options .selected')?.textContent || '';
    const stars = document.querySelectorAll('.stars .selected').length;
    const resultDiv = document.getElementById('result');

    resultDiv.textContent = '';
    if (!text) {
        resultDiv.textContent = 'Please enter some text.';
        resultDiv.className = 'result neutral';
        return;
    }

    resultDiv.textContent = 'Analyzing...';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text, mood, stars })
        });

        const data = await response.json();

        if (response.ok) {
            resultDiv.textContent = `Sentiment: ${data.sentiment} (Confidence: ${data.confidence})`;
            resultDiv.className = `result ${data.sentiment.toLowerCase()}`;
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (err) {
        resultDiv.textContent = `Error: ${err.message}`;
        resultDiv.className = 'result negative';
    }
});

// Handle emoji selection
document.querySelectorAll('.emoji-options span').forEach(emoji => {
    emoji.addEventListener('click', () => {
        document.querySelectorAll('.emoji-options span').forEach(e => e.classList.remove('selected'));
        emoji.classList.add('selected');
    });
});

// Handle star selection
document.querySelectorAll('.stars span').forEach((star, index, stars) => {
    star.addEventListener('click', () => {
        stars.forEach((s, i) => s.classList.toggle('selected', i <= index));
    });
});

document.getElementById('converter-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = document.getElementById('query').value.trim();
    const resultDiv = document.getElementById('result');

    resultDiv.textContent = "Converting...";

    try {
        const response = await fetch('http://127.0.0.1:8000/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_query: query
            })
        });

        const result = await response.json();

        if (result && result.output_text) {
            resultDiv.textContent = result.output_text;
        } else {
            resultDiv.textContent = "Conversion failed. Please check your input.";
        }
    } catch (error) {
        console.error(error);
        resultDiv.textContent = "An error occurred. Try again.";
    }
});

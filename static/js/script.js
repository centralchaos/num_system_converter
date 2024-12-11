function convert() {
    const number = document.getElementById('number').value;
    const fromBase = document.getElementById('fromBase').value;
    const toBase = document.getElementById('toBase').value;

    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            number: number,
            from_base: fromBase,
            to_base: toBase
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').textContent = data.error;
            document.getElementById('steps').textContent = '';
        } else {
            document.getElementById('result').textContent = data.formatted_result;
            document.getElementById('steps').innerHTML = data.steps;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred';
    });
}

function reset() {
    document.getElementById('number').value = '';
    document.getElementById('fromBase').value = '10';
    document.getElementById('toBase').value = '16';
    document.getElementById('result').textContent = '';
    document.getElementById('steps').textContent = '';
}

function swap() {
    const fromBase = document.getElementById('fromBase');
    const toBase = document.getElementById('toBase');
    [fromBase.value, toBase.value] = [toBase.value, fromBase.value];
}

function copyResult() {
    const result = document.getElementById('result').textContent;
    navigator.clipboard.writeText(result);
}

function copySteps() {
    const steps = document.getElementById('steps').textContent;
    navigator.clipboard.writeText(steps);
}
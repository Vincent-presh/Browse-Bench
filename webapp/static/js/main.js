document.addEventListener('DOMContentLoaded', () => {
    const modelsSelect = document.getElementById('models');
    const testsSelect = document.getElementById('tests');
    const benchmarkForm = document.getElementById('benchmark-form');
    const resultsTable = document.getElementById('results-table');

    async function fetchModels() {
        const response = await fetch('/api/models');
        const models = await response.json();
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            modelsSelect.appendChild(option);
        });
    }

    async function fetchTests() {
        const response = await fetch('/api/tests');
        const tests = await response.json();
        tests.forEach(test => {
            const option = document.createElement('option');
            option.value = `services/browsebench/tests/${test}`;
            option.textContent = test;
            testsSelect.appendChild(option);
        });
    }

    async function fetchResults() {
        const response = await fetch('/api/results');
        const results = await response.json();
        renderResults(results);
    }

    function renderResults(results) {
        let html = '<table>';
        html += '<tr><th>Model</th><th>Completion Rate</th><th>Avg. Response Time</th><th>Total Tokens</th><th>Total Cost</th></tr>';
        for (const model in results) {
            const result = results[model];
            html += `<tr>
                <td>${model}</td>
                <td>${(result.completion_rate * 100).toFixed(2)}%</td>
                <td>${result.average_response_time.toFixed(2)}s</td>
                <td>${result.total_token_usage}</td>
                <td>${result.total_cost.toFixed(6)}</td>
            </tr>`;
        }
        html += '</table>';
        resultsTable.innerHTML = html;

        renderCharts(results);
    }

    function renderCharts(data) {
        const models = Object.keys(data);

        const completionRates = models.map(model => data[model].completion_rate);
        const responseTimes = models.map(model => data[model].average_response_time);
        const tokenUsages = models.map(model => data[model].total_token_usage);
        const costs = models.map(model => data[model].total_cost);

        createChart('completionRateChart', 'Completion Rate', models, completionRates);
        createChart('responseTimeChart', 'Average Response Time (s)', models, responseTimes);
        createChart('tokenUsageChart', 'Total Token Usage', models, tokenUsages);
        createChart('costChart', 'Total Cost ($)', models, costs);
    }

    function createChart(canvasId, label, labels, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    benchmarkForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const selectedModels = Array.from(modelsSelect.selectedOptions).map(option => option.value);
        const selectedTest = testsSelect.value;

        await fetch('/api/run_benchmark', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ models: selectedModels, test_file: selectedTest })
        });

        // Refresh results periodically
        const interval = setInterval(async () => {
            await fetchResults();
        }, 5000);
    });

    fetchModels();
    fetchTests();
    fetchResults();
});
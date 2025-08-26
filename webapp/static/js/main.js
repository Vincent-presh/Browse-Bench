async function fetchData() {
    const response = await fetch('/api/results');
    const data = await response.json();
    return data;
}

function createChart(ctx, label, labels, data) {
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

async function main() {
    const data = await fetchData();
    const models = Object.keys(data);

    const completionRates = models.map(model => data[model].completion_rate);
    const responseTimes = models.map(model => data[model].average_response_time);
    const tokenUsages = models.map(model => data[model].total_token_usage);

    const completionRateCtx = document.getElementById('completionRateChart').getContext('2d');
    createChart(completionRateCtx, 'Completion Rate', models, completionRates);

    const responseTimeCtx = document.getElementById('responseTimeChart').getContext('2d');
    createChart(responseTimeCtx, 'Average Response Time (s)', models, responseTimes);

    const tokenUsageCtx = document.getElementById('tokenUsageChart').getContext('2d');
    createChart(tokenUsageCtx, 'Total Token Usage', models, tokenUsages);
}

main();
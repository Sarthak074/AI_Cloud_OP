// ----------------------------
// Fetch wrapper
// ----------------------------
async function fetchJSON(url) {
    const res = await fetch(url);
    return await res.json();
}

// ----------------------------
// Charts setup
// ----------------------------
let cpuChart, memChart, predictionChart;

function createCharts() {

    // CPU Chart
    cpuChart = new Chart(document.getElementById("cpuChart"), {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: "CPU Usage (%)",
                    data: [],
                    borderColor: "#4CC4FF",
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 2
                }
            ]
        },
        options: {
            scales: {
                x: { type: "time", time: { unit: "minute" } },
                y: {
                    beginAtZero: false,
                    suggestedMin: null,
                    suggestedMax: null
                }
            }
        }
    });

    // Memory Chart
    memChart = new Chart(document.getElementById("memChart"), {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Memory Usage (%)",
                    data: [],
                    borderColor: "#FFA500",
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 2
                }
            ]
        },
        options: {
            scales: {
                x: { type: "time", time: { unit: "minute" } },
                y: {
                    beginAtZero: false,
                    suggestedMin: null,
                    suggestedMax: null
                }
            }
        }
    });

    // CPU Prediction Chart
    predictionChart = new Chart(document.getElementById("predictionChart"), {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Actual CPU",
                    data: [],
                    borderColor: "#FFFFFF",
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 2
                },
                {
                    label: "Predicted CPU",
                    data: [],
                    borderColor: "#FFFF00",
                    backgroundColor: "transparent",
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 2
                }
            ]
        },
        options: {
            scales: {
                x: { type: "time", time: { unit: "minute" } },
                y: {
                    beginAtZero: false,
                    suggestedMin: null,
                    suggestedMax: null
                }
            }
        }
    });
}

// ----------------------------
// Update Charts
// ----------------------------
async function updateCharts() {
    const metrics = await fetchJSON("/metrics");

    const timestamps = metrics.map(m => new Date(m.timestamp));

    // CPU Chart
    cpuChart.data.labels = timestamps;
    cpuChart.data.datasets[0].data = metrics.map(m => Number(m.cpu_usage));

    // Memory Chart
    memChart.data.labels = timestamps;
    memChart.data.datasets[0].data = metrics.map(m => Number(m.memory_usage));

    // Prediction Chart
    predictionChart.data.labels = timestamps;

    predictionChart.data.datasets[0].data = metrics.map(
        m => Number(m.cpu_usage)
    );

    predictionChart.data.datasets[1].data = metrics.map(
        m => Number(m.cpu_pred ?? 0)
    );

    cpuChart.update();
    memChart.update();
    predictionChart.update();
}

// ----------------------------
// Update anomalies
// ----------------------------
async function updateAnomalies() {
    const anomalies = await fetchJSON("/anomalies");
    const list = document.getElementById("anomalyList");
    list.innerHTML = "";

    anomalies.forEach(a => {
        const li = document.createElement("li");
        li.innerHTML = `⚠️ Timestamp: ${a.timestamp}, CPU: ${a.cpu_usage}`;
        list.appendChild(li);
    });
}

// ----------------------------
// Update recommendations
// ----------------------------
async function updateRecommendations() {
    const data = await fetchJSON("/recommendations");
    const list = document.getElementById("recommendationList");
    list.innerHTML = "";

    data.recommendations.forEach(r => {
        const li = document.createElement("li");
        li.innerHTML = `💡 ${r}`;
        list.appendChild(li);
    });
}

// ----------------------------
// Initialize dashboard
// ----------------------------
createCharts();
updateCharts();
updateAnomalies();
updateRecommendations();

// Refresh every 5 seconds
setInterval(() => {
    updateCharts();
    updateAnomalies();
    updateRecommendations();
}, 5000);

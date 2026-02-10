// Chart instances
let cpuChart;
let metricsChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    fetchAllData();
    
    // Add event listeners for refresh buttons
    document.getElementById('refreshAnomaliesBtn').addEventListener('click', fetchAnomalies);
    document.getElementById('refreshRecommendationsBtn').addEventListener('click', fetchRecommendations);
    
    // Auto-refresh every 5 seconds
    setInterval(fetchAllData, 5000);
});

// Initialize ApexCharts
function initializeCharts() {
    // CPU Chart Options
    const cpuOptions = {
        series: [{
            name: 'Actual CPU',
            data: []
        }, {
            name: 'Predicted CPU',
            data: []
        }],
        chart: {
            type: 'line',
            height: 250,
            background: 'transparent',
            foreColor: '#94a3b8',
            toolbar: {
                show: false
            }
        },
        colors: ['#2563eb', '#7c3aed'],
        stroke: {
            curve: 'smooth',
            width: 2,
            dashArray: [0, 5]
        },
        xaxis: {
            categories: [],
            labels: {
                style: {
                    colors: '#94a3b8'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#94a3b8'
                },
                formatter: function(val) {
                    return val.toFixed(1) + '%';
                }
            }
        },
        grid: {
            borderColor: '#334155'
        },
        legend: {
            labels: {
                colors: '#94a3b8'
            }
        },
        tooltip: {
            theme: 'dark'
        }
    };

    // Metrics Chart Options
    const metricsOptions = {
        series: [{
            name: 'CPU %',
            data: []
        }, {
            name: 'Memory %',
            data: []
        }, {
            name: 'Latency (ms)',
            data: []
        }],
        chart: {
            type: 'line',
            height: 250,
            background: 'transparent',
            foreColor: '#94a3b8',
            toolbar: {
                show: false
            }
        },
        colors: ['#2563eb', '#10b981', '#f59e0b'],
        stroke: {
            curve: 'smooth',
            width: 2
        },
        xaxis: {
            categories: [],
            labels: {
                style: {
                    colors: '#94a3b8'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#94a3b8'
                }
            }
        },
        grid: {
            borderColor: '#334155'
        },
        legend: {
            labels: {
                colors: '#94a3b8'
            }
        },
        tooltip: {
            theme: 'dark'
        }
    };

    // Create charts
    cpuChart = new ApexCharts(document.querySelector("#cpuChart"), cpuOptions);
    cpuChart.render();

    metricsChart = new ApexCharts(document.querySelector("#metricsChart"), metricsOptions);
    metricsChart.render();
}

// Fetch all data
async function fetchAllData() {
    try {
        await Promise.all([
            fetchPredictions(),
            fetchMetrics(),
            fetchAnomalies(),
            fetchRecommendations()
        ]);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Fetch current predictions
async function fetchPredictions() {
    try {
        const response = await fetch('/predict');
        const data = await response.json();
        
        // Update CPU metrics
        document.getElementById('cpuValue').textContent = `${data.latest_cpu.toFixed(1)}%`;
        document.getElementById('cpuPrediction').textContent = `${data.predicted_cpu.toFixed(1)}%`;
        
        // Update progress bar
        const cpuProgress = document.getElementById('cpuProgress');
        cpuProgress.style.width = `${Math.min(data.latest_cpu, 100)}%`;
        
        // Update anomaly status
        const anomalyCard = document.querySelector('.anomaly-card');
        const anomalyStatus = document.getElementById('anomalyStatus');
        
        if (data.anomaly === -1) {
            anomalyCard.classList.add('alert');
            anomalyStatus.innerHTML = `
                <div class="status-circle"></div>
                <span>Anomaly Detected</span>
            `;
        } else {
            anomalyCard.classList.remove('alert');
            anomalyStatus.innerHTML = `
                <div class="status-circle"></div>
                <span>Normal</span>
            `;
        }
    } catch (error) {
        console.error('Error fetching predictions:', error);
    }
}

// Fetch metrics history
async function fetchMetrics() {
    try {
        const response = await fetch('/metrics');
        const data = await response.json();
        
        if (data.length === 0) return;
        
        // Update metric cards (use latest data point)
        const latest = data[data.length - 1];
        
        // Memory
        const memoryValue = (latest.memory_usage * 100).toFixed(1);
        document.getElementById('memoryValue').textContent = `${memoryValue}%`;
        const memoryProgress = document.getElementById('memoryProgress');
        memoryProgress.style.width = `${Math.min(memoryValue, 100)}%`;
        
        // Latency
        const latencyValue = latest.latency.toFixed(1);
        document.getElementById('latencyValue').textContent = `${latencyValue} ms`;
        const latencyProgress = document.getElementById('latencyProgress');
        latencyProgress.style.width = `${Math.min(latencyValue / 2, 100)}%`;
        
        // Update charts
        updateCharts(data);
        
        // Update table
        updateTable(data);
    } catch (error) {
        console.error('Error fetching metrics:', error);
    }
}

// Update charts with new data
function updateCharts(data) {
    // Prepare labels and data
    const labels = data.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    });
    
    const cpuActual = data.map(item => item.cpu_usage.toFixed(1));
    const cpuPredicted = data.map(item => item.cpu_pred.toFixed(1));
    const memoryData = data.map(item => (item.memory_usage * 100).toFixed(1));
    const latencyData = data.map(item => item.latency.toFixed(1));
    
    // Update CPU Chart
    cpuChart.updateOptions({
        xaxis: {
            categories: labels
        }
    });
    cpuChart.updateSeries([
        {
            name: 'Actual CPU',
            data: cpuActual
        },
        {
            name: 'Predicted CPU',
            data: cpuPredicted
        }
    ]);
    
    // Update Metrics Chart
    metricsChart.updateOptions({
        xaxis: {
            categories: labels
        }
    });
    metricsChart.updateSeries([
        {
            name: 'CPU %',
            data: cpuActual
        },
        {
            name: 'Memory %',
            data: memoryData
        },
        {
            name: 'Latency (ms)',
            data: latencyData
        }
    ]);
}

// Update metrics table
function updateTable(data) {
    const tbody = document.getElementById('metricsTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="loading">No data available</td></tr>';
        return;
    }
    
    const tableData = [...data].reverse();
    
    tbody.innerHTML = tableData.map(item => {
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const status = item.anomaly === -1 ? 
            '<span class="status-badge-table status-anomaly">Anomaly</span>' : 
            '<span class="status-badge-table status-normal">Normal</span>';
        
        return `
            <tr>
                <td>${timeStr}</td>
                <td>${item.cpu_usage.toFixed(1)}%</td>
                <td>${(item.memory_usage * 100).toFixed(1)}%</td>
                <td>${item.latency.toFixed(1)} ms</td>
                <td>${item.cpu_pred.toFixed(1)}%</td>
                <td>${status}</td>
            </tr>
        `;
    }).join('');
}

// Fetch anomalies
async function fetchAnomalies() {
    try {
        const response = await fetch('/anomalies');
        const data = await response.json();
        
        const anomaliesList = document.getElementById('anomaliesList');
        
        if (data.length === 0) {
            anomaliesList.innerHTML = '<p class="loading">No anomalies detected recently ✓</p>';
            return;
        }
        
        anomaliesList.innerHTML = data.map(item => {
            const date = new Date(item.timestamp);
            const timeStr = date.toLocaleString('en-US', { 
                month: 'short', 
                day: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            return `
                <div class="anomaly-item">
                    <div class="anomaly-time">${timeStr}</div>
                    <div class="anomaly-details">
                        CPU: ${item.cpu_usage.toFixed(1)}% | 
                        Memory: ${(item.memory_usage * 100).toFixed(1)}% | 
                        Latency: ${item.latency.toFixed(1)}ms
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error fetching anomalies:', error);
        document.getElementById('anomaliesList').innerHTML = '<p class="loading">Error loading anomalies</p>';
    }
}

// Fetch recommendations
async function fetchRecommendations() {
    try {
        const response = await fetch('/recommendations');
        const data = await response.json();
        
        const recommendationsList = document.getElementById('recommendationsList');
        
        if (!data.recommendations || data.recommendations.length === 0) {
            recommendationsList.innerHTML = '<p class="loading">All systems optimal ✓</p>';
            return;
        }
        
        recommendationsList.innerHTML = data.recommendations.map(rec => `
            <div class="recommendation-item">${rec}</div>
        `).join('');
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        document.getElementById('recommendationsList').innerHTML = '<p class="loading">Error loading recommendations</p>';
    }
}
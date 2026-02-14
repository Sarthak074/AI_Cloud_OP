# Cloud Optimization \& Anomaly Detection System — Optimo

A real-time system monitoring platform with AI-driven predictions, anomaly detection, and intelligent recommendations. Built with FastAPI, Machine Learning models, and a modern responsive dashboard.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Load Generator](#load-generator)
- [Screenshots](#screenshots)
- [How It Works](#how-it-works)
- [Docker Configuration](#docker-configuration)

## ✨ Features

### 🎯 Core Functionality
- **Real-time Monitoring**: Track CPU usage, memory consumption, and system latency
- **AI Predictions**: Linear Regression predicts future CPU usage patterns
- **Anomaly Detection**: Isolation Forest algorithm identifies unusual system behavior
- **Smart Recommendations**: AI-generated optimization suggestions based on system metrics
- **Auto-refresh**: Dashboard updates every 5 seconds with live data

### 📊 Visualization
- Interactive charts with ApexCharts
- CPU usage trends (Actual vs Predicted)
- Multi-metric system overview
- Historical data table
- Color-coded anomaly alerts

### 🎨 UI/UX
- Modern dark theme interface
- Responsive design (mobile & desktop)
- Real-time progress indicators
- Intuitive metric cards

### 🧪 Testing & Development
- **Load Generator**: Synthetic load generation for testing
- CPU stress testing endpoints
- Memory consumption simulation
- Latency injection capabilities
- Prometheus metrics export

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation and analysis
- **Scikit-learn** - Machine learning models (Isolation Forest, Linear Regression, Logistic Regression)
- **Joblib** - Model serialization

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Interactive functionality
- **ApexCharts** - Data visualization
- **Jinja2** - Template engine

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)

### Installing Docker

#### Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer and follow the setup wizard
3. Restart your computer

#### macOS
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Open the `.dmg` file and drag Docker to Applications
3. Launch Docker from Applications

#### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-system-monitor.git
cd ai-system-monitor
```

### 2. Project Structure Setup

Ensure your project structure looks like this:

```
ai-system-monitor/
├── backend/
│   ├── static/
│   │   ├── dashboard.js
│   │   └── style.css
│   ├── templates/
│   │   └── dashboard.html
│   └── main.py
├── ai_engine/
│   ├── models/
│   ├── ai_engine.py
│   ├── optimizer.py
│   ├── fetch_metrics.py
│   ├── cpu_metrics.csv
│   ├── memory_metrics.csv
│   └── latency_metrics.csv
├── load-generator/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### 3. Build and Run with Docker Compose

```bash
# Build the Docker image and start containers
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build
```

### 4. Access the Services

Once the containers are running, you'll have access to both services:

**AI Monitoring Dashboard:**
```
http://localhost:3000/dashboard
```

**Load Generator API:**
```
http://localhost:8000
```

Check service status:
```bash
# View running containers
docker ps

# Check logs for AI Monitor
docker logs ai-system-monitor

# Check logs for Load Generator
docker logs load-generator
```

## 💻 Usage

### Starting the Application

```bash
# Start all services (AI Monitor + Load Generator)
docker compose up

# Start in background
docker compose up -d

# View logs for all services
docker compose logs -f

# View logs for specific service
docker compose logs -f ai-monitor
docker compose logs -f load-generator

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### AI Monitor API Endpoints

The AI monitoring service exposes several REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check - returns system status |
| `/dashboard` | GET | Renders the main dashboard UI |
| `/metrics` | GET | Returns last 10 metric records |
| `/predict` | GET | Returns latest predictions and anomaly status |
| `/anomalies` | GET | Returns last 10 detected anomalies |
| `/recommendations` | GET | Returns AI-generated optimization recommendations |

### Example API Calls

```bash
# Check system status
curl http://localhost:3000/

# Get latest predictions
curl http://localhost:3000/predict

# Get metrics
curl http://localhost:3000/metrics

# Get anomalies
curl http://localhost:3000/anomalies

# Get recommendations
curl http://localhost:3000/recommendations
```

## 📁 Project Structure

```
.
├── backend/
│   ├── static/              # Frontend assets
│   │   ├── dashboard.js     # JavaScript logic & API calls
│   │   └── style.css        # Styling & animations
│   ├── templates/           # HTML templates
│   │   └── dashboard.html   # Main dashboard page
│   └── main.py             # FastAPI application
│
├── ai_engine/
│   ├── models/             # Trained ML models (generated)
│   │   ├── cpu_model.pkl
│   │   ├── anomaly_model.pkl
│   │   └── failure_model.pkl
│   ├── ai_engine.py        # Model training pipeline
│   ├── optimizer.py        # Recommendation engine
│   ├── fetch_metrics.py    # Metrics collection script
│   ├── cpu_metrics.csv     # CPU usage data
│   ├── memory_metrics.csv  # Memory usage data
│   ├── latency_metrics.csv # Latency data
│   └── requirements.txt    # AI engine dependencies
│
├── load-generator/         # Synthetic load generation
│   ├── app.py             # Load generator FastAPI app
│   ├── Dockerfile         # Load generator container
│   └── requirements.txt   # Load generator dependencies
│
├── prometheus/            # (Optional) Monitoring stack
│   └── docker-compose.yml # Prometheus configuration
│
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 📸 Screenshots

### Main Dashboard
<img width="1905" height="999" alt="Screenshot From 2026-02-10 14-52-59" src="https://github.com/user-attachments/assets/12409e1e-f2fd-4cf8-a63a-bf8b8a137939" />
*Real-time system metrics with AI predictions*

### Metrics History Table
<img width="1905" height="999" alt="Screenshot From 2026-02-10 14-53-08" src="https://github.com/user-attachments/assets/1c84251e-a75f-405f-b249-93053c815b89" />
*Historical data with status indicators*

## 🧠 How It Works

### 1. Data Collection
The system continuously monitors three key metrics:
- **CPU Usage**: Percentage of CPU utilization
- **Memory Usage**: RAM consumption percentage
- **Latency**: System response time in milliseconds

### 2. AI Training Pipeline
On startup, the system trains three ML models:

**CPU Prediction Model (LSTM)**
- Uses past 5 time steps as features (lag features)
- Predicts future CPU usage
- Architecture: LSTM(50) → Dropout(0.2) → Dense(1)

**Anomaly Detection Model (Isolation Forest)**
- Detects unusual patterns in system behavior
- Features: CPU, Memory, Latency
- Flags anomalies with -1, normal behavior with 1

**Failure Prediction Model (Random Forest)**
- Predicts potential system failures
- Uses historical patterns and thresholds

### 3. Real-time Inference
- Every API call triggers model inference
- Predictions are computed on-the-fly
- Results are cached and updated every 5 seconds

### 4. Recommendation Engine
The `optimizer.py` module analyzes metrics and generates actionable recommendations:
- High CPU → Suggests process optimization
- High Memory → Recommends memory cleanup
- High Latency → Advises network/disk improvements

### 5. Visualization
The frontend uses ApexCharts to render:
- Line charts for trends
- Real-time metric cards
- Anomaly alerts
- Historical data tables

## 🔥 Load Generator

The project includes a **load-generator** service for testing and demonstration purposes. This separate FastAPI application simulates various system loads to help you:

- Test anomaly detection algorithms
- Generate realistic CPU, memory, and latency patterns
- Validate AI model predictions
- Demonstrate the monitoring dashboard capabilities

### Starting the Load Generator

The load generator runs automatically when you use docker-compose:

```bash
# Start both services (AI Monitor + Load Generator)
docker compose up --build

# AI Monitor will be at: http://localhost:3000/dashboard
# Load Generator will be at: http://localhost:8000
```

### Load Generator Endpoints

| Endpoint | Method | Description | Effect |
|----------|--------|-------------|--------|
| `/` | GET | Health check | Returns status |
| `/cpu` | GET | Generates CPU load for 10 seconds | Spawns background thread, burns CPU cycles |
| `/memory` | GET | Increases memory consumption by ~10MB | Allocates large strings, memory persists |
| `/latency` | GET | Simulates 2-second delay | Adds artificial latency |
| `/reset` | GET | Clears allocated memory | Frees up memory, returns freed MB count |
| `/metrics` | GET | Prometheus metrics endpoint | Exposes metrics in Prometheus format |

### How Each Endpoint Works

**CPU Load (`/cpu`)**
```python
# Spawns a background thread that burns CPU cycles for 10 seconds
def burn_cpu():
    end_time = time.time() + 10
    while time.time() < end_time:
        pass  # CPU-intensive loop

thread = threading.Thread(target=burn_cpu)
thread.start()
```

**Memory Load (`/memory`)**
```python
# Allocates 10MB of memory by appending large strings
for _ in range(10):
    memory_holder.append("X" * 10**6)  # 1 MB per iteration
```

**Latency Simulation (`/latency`)**
```python
# Adds artificial 2-second delay to simulate slow responses
with LATENCY_HIST.time():
    time.sleep(2)
```

### Using the Load Generator

Test the AI monitoring system by generating synthetic loads:

```bash
# Generate CPU spike
curl http://localhost:8000/cpu

# Increase memory usage (call multiple times)
curl http://localhost:8000/memory
curl http://localhost:8000/memory
curl http://localhost:8000/memory

# Create latency spike
curl http://localhost:8000/latency

# Clear memory
curl http://localhost:8000/reset

# View Prometheus metrics
curl http://localhost:8000/metrics
```

### Prometheus Metrics Exported

The load generator exposes these metrics:

- `loadgen_cpu_requests_total` - Counter of CPU load requests
- `loadgen_memory_requests_total` - Counter of memory load requests  
- `loadgen_latency_seconds` - Histogram of latency endpoint timing

These can be scraped by Prometheus for advanced monitoring.

### Load Generator File Structure

```
load-generator/
├── app.py              # FastAPI application
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

**`app.py`** - Main application with endpoints
**`Dockerfile`** - Containerization setup
**`requirements.txt`** - `fastapi`, `uvicorn`, `prometheus-client`

### Safety Notes

⚠️ **Warning**: This service intentionally consumes system resources!

- CPU load runs for 10 seconds per request
- Memory accumulates until reset
- Use in controlled environments only
- Not for production deployment

## 🐳 Docker Configuration

### Complete docker-compose.yml

The project runs two services simultaneously:

```yaml
version: '3.8'

services:
  ai-monitor:
    build: .
    container_name: ai-system-monitor
    ports:
      - "3000:3000"
    volumes:
      - ./ai_engine:/app/ai_engine
      - ./backend:/app/backend
    environment:
      - PYTHONUNBUFFERED=1
      - TF_CPP_MIN_LOG_LEVEL=2
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  load-generator:
    build: ./load-generator
    container_name: load-generator
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Access Points:**
- AI Monitor Dashboard: `http://localhost:3000/dashboard`
- Load Generator API: `http://localhost:8000`

### Main Application Dockerfile

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "3000"]
```

### Load Generator Dockerfile

Located in `load-generator/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

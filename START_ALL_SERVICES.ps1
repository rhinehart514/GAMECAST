# NHL Simulation Game - Service Startup Script
# This script starts all required services for the complete application

Write-Host "🏒 NHL Simulation Game - Starting All Services..." -ForegroundColor Cyan
Write-Host ""

# Function to check if a port is in use
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
    return $connection
}

# Check Node.js
Write-Host "Checking dependencies..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✓ Node.js installed" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js not found! Install from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✓ Python installed" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found! Install Python 3.10+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start Intelligence Service (Port 5001)
Write-Host "1. Starting Intelligence Service (ML Model)..." -ForegroundColor Cyan
if (Test-Port 5001) {
    Write-Host "   → Already running on port 5001" -ForegroundColor Yellow
} else {
    $intelligenceJob = Start-Job -ScriptBlock {
        Set-Location "$using:PWD\intelligence-service"
        & ".\venv\Scripts\Activate.ps1"
        Set-Location "src"
        python main.py
    }
    Write-Host "   → Started (Job ID: $($intelligenceJob.Id))" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# Start Game API (Port 8001)
Write-Host "2. Starting Game API..." -ForegroundColor Cyan
if (Test-Port 8001) {
    Write-Host "   → Already running on port 8001" -ForegroundColor Yellow
} else {
    $gameApiJob = Start-Job -ScriptBlock {
        Set-Location "$using:PWD\game-api"
        python main.py
    }
    Write-Host "   → Started (Job ID: $($gameApiJob.Id))" -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# Start Web UI (Port 3000)
Write-Host "3. Starting Web UI..." -ForegroundColor Cyan
if (Test-Port 3000) {
    Write-Host "   → Already running on port 3000" -ForegroundColor Yellow
} else {
    $webJob = Start-Job -ScriptBlock {
        Set-Location "$using:PWD\web-ui"
        npm run dev
    }
    Write-Host "   → Started (Job ID: $($webJob.Id))" -ForegroundColor Green
}

Write-Host ""
Write-Host "Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 ALL SERVICES STARTED!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host "  🌐 Web UI:               http://localhost:3000" -ForegroundColor White
Write-Host "  🎮 Game API:             http://localhost:8001" -ForegroundColor White
Write-Host "  🧠 Intelligence Service: http://localhost:5001" -ForegroundColor White
Write-Host ""
Write-Host "API Documentation:" -ForegroundColor Yellow
Write-Host "  📚 Game API Docs:        http://localhost:8001/docs" -ForegroundColor White
Write-Host "  📚 Intelligence Docs:    http://localhost:5001/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop all services, run: .\STOP_ALL_SERVICES.ps1" -ForegroundColor Yellow
Write-Host ""

# Keep script running and show logs
Write-Host "Press Ctrl+C to stop watching logs..." -ForegroundColor Gray
Write-Host ""

while ($true) {
    Start-Sleep -Seconds 5
}




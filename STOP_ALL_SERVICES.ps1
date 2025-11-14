# NHL Simulation Game - Stop All Services

Write-Host "🛑 Stopping all NHL Simulation Game services..." -ForegroundColor Yellow
Write-Host ""

# Kill processes by port
$ports = @(3000, 5001, 8001)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    foreach ($conn in $connections) {
        $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Stopping $($process.Name) on port $port..." -ForegroundColor Cyan
            Stop-Process -Id $process.Id -Force
        }
    }
}

# Stop all PowerShell background jobs
Write-Host "Stopping background jobs..." -ForegroundColor Cyan
Get-Job | Stop-Job
Get-Job | Remove-Job

Write-Host ""
Write-Host "✓ All services stopped!" -ForegroundColor Green




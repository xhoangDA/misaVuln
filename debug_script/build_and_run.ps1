# CVE Tools Flask Project - Docker Build and Run Script for Windows
# PowerShell script

param(
    [switch]$Compose,
    [switch]$Standalone,
    [switch]$BuildOnly,
    [switch]$Help
)

function Show-Help {
    Write-Host "CVE Tools Flask - Docker Deployment Script" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\build_and_run.ps1 [OPTIONS]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Compose      Use docker-compose (default)" -ForegroundColor White
    Write-Host "  -Standalone   Run standalone container" -ForegroundColor White
    Write-Host "  -BuildOnly    Build image only" -ForegroundColor White
    Write-Host "  -Help         Show this help" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\build_and_run.ps1                # Build and run with docker-compose" -ForegroundColor White
    Write-Host "  .\build_and_run.ps1 -Standalone    # Build and run standalone container" -ForegroundColor White
    Write-Host "  .\build_and_run.ps1 -BuildOnly     # Only build the Docker image" -ForegroundColor White
}

function Test-Docker {
    Write-Host "🔍 Checking Docker..." -ForegroundColor Blue
    try {
        $dockerInfo = docker info 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker is running" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "❌ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
        return $false
    }
    Write-Host "❌ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    return $false
}

function Build-Image {
    Write-Host "🔨 Building Docker image..." -ForegroundColor Blue
    docker build -t cve-tools-flask .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker image built successfully" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Failed to build Docker image" -ForegroundColor Red
        return $false
    }
}

function Start-WithCompose {
    Write-Host "🚀 Starting services using docker-compose..." -ForegroundColor Blue
    docker-compose up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Services started successfully" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Service URLs:" -ForegroundColor Cyan
        Write-Host "   - Flask App: http://localhost:5000" -ForegroundColor White
        Write-Host "   - Nginx Proxy: http://localhost:80" -ForegroundColor White
        Write-Host "   - MySQL: localhost:3306" -ForegroundColor White
        Write-Host ""
        Write-Host "📊 To view logs: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "🛑 To stop services: docker-compose down" -ForegroundColor Yellow
        Write-Host "🔄 To restart services: docker-compose restart" -ForegroundColor Yellow
        return $true
    } else {
        Write-Host "❌ Failed to start services" -ForegroundColor Red
        return $false
    }
}

function Start-Standalone {
    Write-Host "🚀 Running standalone Flask container..." -ForegroundColor Blue
    
    # Stop any existing container
    docker stop cve-flask-app 2>$null
    docker rm cve-flask-app 2>$null
    
    # Get current directory for volume mounting
    $currentDir = Get-Location
    
    # Run new container
    docker run -d `
        --name cve-flask-app `
        -p 5000:5000 `
        -v "${currentDir}/data:/app/data:ro" `
        --restart unless-stopped `
        cve-tools-flask
        
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Container started successfully" -ForegroundColor Green
        Write-Host "🌐 Application available at: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "📊 To view logs: docker logs -f cve-flask-app" -ForegroundColor Yellow
        Write-Host "🛑 To stop container: docker stop cve-flask-app" -ForegroundColor Yellow
        return $true
    } else {
        Write-Host "❌ Failed to start container" -ForegroundColor Red
        return $false
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Host "🎯 CVE Tools Flask - Docker Deployment" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check Docker
if (-not (Test-Docker)) {
    exit 1
}

# Build image
if (-not (Build-Image)) {
    exit 1
}

# Exit if build-only mode
if ($BuildOnly) {
    Write-Host "✅ Build completed. Image: cve-tools-flask" -ForegroundColor Green
    exit 0
}

# Determine mode (default to compose)
$mode = if ($Standalone) { "standalone" } else { "compose" }

# Run based on selected mode
$success = switch ($mode) {
    "compose" { Start-WithCompose }
    "standalone" { Start-Standalone }
    default { Start-WithCompose }
}

if ($success) {
    Write-Host ""
    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

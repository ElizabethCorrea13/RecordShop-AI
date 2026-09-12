<#
    Levanta el backend (FastAPI) y el frontend (Vite) de RecordShop AI,
    cada uno en su propia ventana de PowerShell.

    Uso:
        .\scripts\start-dev.ps1

    Para frenar todo: .\scripts\stop-dev.ps1
#>

$ErrorActionPreference = "Stop"

$RepoRoot     = Split-Path -Parent $PSScriptRoot
$BackendDir   = Join-Path $RepoRoot "backend"
$FrontendDir  = Join-Path $RepoRoot "frontend"
$VenvActivate = Join-Path $BackendDir ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvActivate)) {
    Write-Host "No encontré backend\.venv. Creá el entorno una vez con:" -ForegroundColor Yellow
    Write-Host "  cd backend"
    Write-Host "  py -m venv .venv"
    Write-Host "  .\.venv\Scripts\Activate.ps1"
    Write-Host "  pip install -r requirements.txt"
    exit 1
}

if (-not (Test-Path (Join-Path $FrontendDir "node_modules"))) {
    Write-Host "No encontré frontend\node_modules. Instalá las dependencias una vez con:" -ForegroundColor Yellow
    Write-Host "  cd frontend"
    Write-Host "  npm install"
    exit 1
}

if (-not (Test-Path (Join-Path $FrontendDir ".env"))) {
    Write-Host "No encontré frontend\.env, lo creo a partir de .env.example..." -ForegroundColor Yellow
    Copy-Item (Join-Path $FrontendDir ".env.example") (Join-Path $FrontendDir ".env")
}

Write-Host "Levantando backend  -> http://localhost:8001 (nueva ventana)" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$BackendDir'; . '$VenvActivate'; uvicorn main:app --reload --port 8001"
)

Write-Host "Levantando frontend -> http://localhost:5173 (nueva ventana)" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$FrontendDir'; npm run dev"
)

Write-Host ""
Write-Host "Backend:  http://localhost:8001/health"
Write-Host "Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Para frenar todo: .\scripts\stop-dev.ps1"

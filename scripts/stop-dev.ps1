<#
    Frena el backend y el frontend de RecordShop AI: cierra las ventanas de
    PowerShell que abrió start-dev.ps1 y todos sus procesos hijos.

    Por qué no alcanza con matar "lo que esté escuchando en el puerto": en
    Windows, `uvicorn --reload` levanta un proceso hijo (multiprocessing)
    que hereda el socket. Si se mata solo al proceso padre, el hijo queda
    huérfano sirviendo igual el puerto — y encima Windows sigue reportando
    el puerto como "escuchado" por el PID del padre ya muerto. Por eso acá
    se mata el árbol completo de procesos de cada ventana.

    Uso:
        .\scripts\stop-dev.ps1
#>

$RepoRoot    = Split-Path -Parent $PSScriptRoot
$BackendDir  = Join-Path $RepoRoot "backend"
$FrontendDir = Join-Path $RepoRoot "frontend"
$killedAny   = $false

function Get-DescendantProcessIds {
    param([int]$ParentId, [object[]]$AllProcesses)
    $result = New-Object System.Collections.Generic.List[int]
    $queue = [System.Collections.Generic.Queue[int]]::new()
    $queue.Enqueue($ParentId)
    while ($queue.Count -gt 0) {
        $current = $queue.Dequeue()
        foreach ($child in ($AllProcesses | Where-Object { $_.ParentProcessId -eq $current })) {
            $result.Add($child.ProcessId)
            $queue.Enqueue($child.ProcessId)
        }
    }
    return $result
}

$allProcesses = Get-CimInstance Win32_Process

# 1) Ventanas que abrió start-dev.ps1 (se identifican por la ruta del proyecto
#    en su línea de comando) + todo lo que hayan generado (uvicorn, npm, vite...)
$launchers = $allProcesses | Where-Object {
    $_.Name -eq 'powershell.exe' -and $_.CommandLine -and (
        $_.CommandLine.Contains($BackendDir) -or $_.CommandLine.Contains($FrontendDir)
    )
}

$pidsToKill = New-Object System.Collections.Generic.List[int]
foreach ($l in $launchers) {
    $pidsToKill.Add($l.ProcessId)
    foreach ($d in (Get-DescendantProcessIds -ParentId $l.ProcessId -AllProcesses $allProcesses)) {
        $pidsToKill.Add($d)
    }
}

foreach ($procId in ($pidsToKill | Select-Object -Unique)) {
    $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
    if ($proc) {
        try {
            Stop-Process -Id $procId -Force -ErrorAction Stop
            Write-Host "Terminado: $($proc.ProcessName) (PID $procId)" -ForegroundColor Green
            $killedAny = $true
        } catch {
            Write-Host "No pude terminar $($proc.ProcessName) (PID $procId): $_" -ForegroundColor Red
        }
    }
}

# 2) Red de seguridad: si algo quedó igual escuchando en los puertos de dev
#    (por ejemplo, quedaron de una corrida manual sin pasar por start-dev.ps1)
$ports = 8001, 5173, 5174, 5175, 5176
foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        $proc = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
        if ($proc) {
            try {
                Stop-Process -Id $proc.Id -Force -ErrorAction Stop
                Write-Host "Puerto $port -> $($proc.ProcessName) (PID $($proc.Id)) terminado" -ForegroundColor Green
                $killedAny = $true
            } catch {
                Write-Host "No pude terminar $($proc.ProcessName) (PID $($proc.Id), puerto $port): $_" -ForegroundColor Red
            }
        }
    }
}

if (-not $killedAny) {
    Write-Host "No había nada corriendo." -ForegroundColor Yellow
}

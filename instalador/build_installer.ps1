param(
    [switch]$SkipExecutable
)

$ErrorActionPreference = "Stop"

# Descobrir caminhos
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$python = Get-Command python -ErrorAction Stop
$repoRootPath = $repoRoot.ProviderPath

$version = & $python.Source -c "import sys; sys.path.insert(0, r'$repoRootPath'); import cleaner; print(cleaner.__version__)"
$version = $version.Trim()

Write-Host "[1/4] Repositório:" $repoRoot
Write-Host "[info] Versão detectada:" $version

if (-not $SkipExecutable) {
    Write-Host "[2/4] Gerando executável standalone via PyInstaller..."
    & $python.Source "$(Join-Path $repoRoot 'build_windows_exe.py')"
} else {
    Write-Host "[2/4] SkipExecutable especificado: reutilizando binário existente em dist/."
}

$distDir = Join-Path $repoRoot 'dist'
$exePath = Join-Path $distDir 'FRP-Cleaner.exe'
if (-not (Test-Path $exePath)) {
    throw "Executável não encontrado em $exePath. Execute sem -SkipExecutable para gerá-lo."
}

$installerDir = $scriptDir
$stagingDir = Join-Path $installerDir 'staging'
$installerDist = Join-Path $installerDir 'dist'

if (Test-Path $stagingDir) {
    Remove-Item $stagingDir -Recurse -Force
}
New-Item $stagingDir -ItemType Directory | Out-Null

if (-not (Test-Path $installerDist)) {
    New-Item $installerDist -ItemType Directory | Out-Null
}

Write-Host "[3/4] Copiando artefactos para staging..."
Copy-Item $exePath $stagingDir -Force
Copy-Item (Join-Path $installerDir 'resources/README_instalacao.txt') $stagingDir -Force

$issFile = Join-Path $installerDir 'frp_cleaner_installer.iss'
if (-not (Test-Path $issFile)) {
    throw "Script Inno Setup não encontrado em $issFile"
}

$iscc = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $iscc) {
    throw "Inno Setup Compiler (iscc.exe) não encontrado no PATH. Instale o Inno Setup e tente novamente."
}

Write-Host "[4/4] Compilando instalador com Inno Setup..."
& $iscc.Source $issFile /O"$installerDist" /DMyAppVersion="$version"

Write-Host "Instalador concluído. Verifique a pasta" $installerDist

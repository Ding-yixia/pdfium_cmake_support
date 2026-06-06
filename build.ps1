param(
    [ValidateSet("Release", "Debug")]
    [string]$Config = "Release",
    [switch]$Clean,
    [switch]$NoBuild,
    [switch]$Examples,
    [switch]$UseVS,
    [int]$Parallel = (Get-CimInstance -ClassName Win32_ComputerSystem).NumberOfLogicalProcessors
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BuildDir = "$ScriptDir\build\cmake_build"
$DepsDir = "$ScriptDir\deps"
$ToolDir = "$DepsDir\bin"
$Generator = "Ninja"
if ($UseVS) {
    $Generator = "Visual Studio 17 2022"
    $BuildDir = "$ScriptDir\build\cmake_build-vs"
}

# Use system Clang (LLVM) - more compatible than bundled Chromium Clang
$ClangDir = "C:/Program Files/LLVM/bin"
# Fallback to bundled Clang from deps/tools if system is not available
if (-not (Test-Path "$ClangDir/clang-cl.exe")) {
    $ClangDir = $ToolDir
    Write-Host "Using bundled Clang from deps/tools" -ForegroundColor Cyan
} else {
    Write-Host "Using system Clang 19 from $ClangDir" -ForegroundColor Cyan
}

$ClangC = "$ClangDir/clang-cl.exe"
$ClangCXX = "$ClangDir/clang-cl.exe"
$LlvmRc = "$ClangDir/llvm-rc.exe"
$LlvmLib = "$ClangDir/llvm-lib.exe"
$NinjaPath = "$ToolDir/ninja.exe"

# Update path for dirname/ninja
$env:Path = "$env:Path;$ClangDir"

# Validate tools
if (-not (Test-Path $ClangC)) {
    Write-Host "ERROR: Bundled Clang not found at $ClangC" -ForegroundColor Red
    Write-Host "Please run setup_deps.ps1 first to download dependencies." -ForegroundColor Yellow
    exit 1
}
if (-not (Test-Path $NinjaPath)) {
    Write-Host "ERROR: Bundled Ninja not found at $NinjaPath" -ForegroundColor Red
    Write-Host "Please run setup_deps.ps1 first to download dependencies." -ForegroundColor Yellow
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PDFium Build Script" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Config:       $Config"
Write-Host "Build Dir:    $BuildDir"
Write-Host "Clang:        $ClangC"
Write-Host "Ninja:        $NinjaPath"
Write-Host "Parallel:     $Parallel"
Write-Host "Examples:     $Examples"
Write-Host "Clean:        $Clean"
Write-Host ""

if ($Clean -and (Test-Path $BuildDir)) {
    Write-Host "Cleaning build directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $BuildDir -ErrorAction SilentlyContinue
    Write-Host "Done." -ForegroundColor Green
    Write-Host ""
}

$ExtraArgs = @()
if ($Examples) {
    $ExtraArgs += "-DPDFIUM_BUILD_EXAMPLES=ON"
}

# Configure
Write-Host "Configuring CMake..." -ForegroundColor Yellow
$ConfigureArgs = @(
    "-S", $ScriptDir
    "-B", $BuildDir
    "-G", $Generator
)
if ($UseVS) {
    $ConfigureArgs += @("-T", "ClangCL")
} else {
    $ConfigureArgs += @(
        "-DCMAKE_C_COMPILER=$ClangC"
        "-DCMAKE_CXX_COMPILER=$ClangCXX"
        "-DCMAKE_RC_COMPILER=$LlvmRc"
        "-DCMAKE_MAKE_PROGRAM=$NinjaPath"
        "-DCMAKE_AR=$LlvmLib"
    )
}
$ConfigureArgs += "-DCMAKE_BUILD_TYPE=$Config"
$ConfigureArgs += $ExtraArgs

$cmake = Get-Command cmake -ErrorAction SilentlyContinue
if (-not $cmake) {
    $cmake = "$env:ProgramFiles\CMake\bin\cmake.exe"
    if (-not (Test-Path $cmake)) {
        throw "CMake not found. Please install CMake (winget install Kitware.CMake)"
    }
}

Write-Host "cmake $($ConfigureArgs -join " `\`n  ")" -ForegroundColor Gray
& $cmake $ConfigureArgs
if ($LASTEXITCODE -ne 0) {
    throw "CMake configuration failed (exit code: $LASTEXITCODE)"
}
Write-Host "Configuration done." -ForegroundColor Green
Write-Host ""

if ($NoBuild) {
    Write-Host "Skipping build (NoBuild specified)." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To build manually run:" -ForegroundColor Cyan
    Write-Host "  cmake --build $BuildDir --parallel" -ForegroundColor White
    exit 0
}

# Build
Write-Host "Building..." -ForegroundColor Yellow
cmake --build $BuildDir --parallel $Parallel
if ($LASTEXITCODE -ne 0) {
    throw "Build failed (exit code: $LASTEXITCODE)"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Output files:" -ForegroundColor Cyan
Get-ChildItem "$BuildDir\bin" -ErrorAction SilentlyContinue | ForEach-Object {
    $size = switch ($_.Length) {
        { $_ -gt 1MB } { "{0:N1} MB" -f ($_ / 1MB) }
        { $_ -gt 1KB } { "{0:N1} KB" -f ($_ / 1KB) }
        default { "$_ B" }
    }
    Write-Host "  $($_.Name) ($size)" -ForegroundColor White
}
Write-Host ""
Write-Host "Libraries:" -ForegroundColor Cyan
Get-ChildItem "$BuildDir\lib\*.lib" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "  $($_.Name)" -ForegroundColor White
}

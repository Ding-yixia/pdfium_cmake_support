param(
    [string]$ProjectRoot = (Get-Location).Path
)

$DepsDir = Join-Path $ProjectRoot "deps"
$ToolsBin = Join-Path $DepsDir "tools\bin"
$IncludeDir = Join-Path $DepsDir "include"
$LibDir = Join-Path $DepsDir "lib"

# Ensure target directories exist
@($ToolsBin, $IncludeDir, $LibDir) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

Write-Host "=== Copying Build Tools ==="
$ClangSrc = "C:\Code\pdfium_all_code\pdfium\third_party\llvm-build\Release+Asserts\bin\clang-cl.exe"
$LldSrc   = "C:\Code\pdfium_all_code\pdfium\third_party\llvm-build\Release+Asserts\bin\lld-link.exe"
$LlvmRcSrc = "C:\Program Files\LLVM\bin\llvm-rc.exe"
$LlvmLibSrc = "C:\Program Files\LLVM\bin\llvm-lib.exe"
$LlvmMtSrc = "C:\Program Files\LLVM\bin\llvm-mt.exe"
$NinjaSrc = "C:\Users\User\AppData\Local\Microsoft\WinGet\Links\ninja.exe"

$tools = @(
    @{src = $ClangSrc; name = "clang-cl.exe"},
    @{src = $LldSrc; name = "lld-link.exe"},
    @{src = $LlvmRcSrc; name = "llvm-rc.exe"},
    @{src = $LlvmLibSrc; name = "llvm-lib.exe"},
    @{src = $LlvmMtSrc; name = "llvm-mt.exe"},
    @{src = $NinjaSrc; name = "ninja.exe"}
)
$tools | ForEach-Object {
    if (Test-Path $_.src) {
        Copy-Item -Path $_.src -Destination $ToolsBin -Force
        Write-Host "  Copied: $($_.name)"
    } else {
        Write-Host "  Warning: $($_.name) not found at $($_.src), skipping"
    }
}

Write-Host ""
Write-Host "=== Copying Library Headers ==="
$VcpkgInclude = "C:\Code\vcpkg\installed\x64-windows-static\include"

@("absl", "harfbuzz", "unicode") | ForEach-Object {
    $src = Join-Path $VcpkgInclude $_
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $IncludeDir -Recurse -Force
        Write-Host "  Copied: $_/"
    } else {
        Write-Host "  Warning: $_/ not found, skipping"
    }
}

# Copy JPEG headers (jpeg lib headers from vcpkg at root of include)
$jpegHeaders = @("jconfig.h", "jerror.h", "jmorecfg.h", "jpeglib.h")
$jpegHeaders | ForEach-Object {
    $src = Join-Path $VcpkgInclude $_
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $IncludeDir -Force
        Write-Host "  Copied: $_"
    } else {
        Write-Host "  Skipped: $_ (not found)"
    }
}

Write-Host ""
Write-Host "=== Copying Library Binaries ==="
$VcpkgLib = "C:\Code\vcpkg\installed\x64-windows-static\lib"

$libFiles = @(
    "icuuc.lib",
    "icudt.lib",
    "harfbuzz.lib",
    "harfbuzz-subset.lib",
    "jpeg.lib",
    "turbojpeg.lib"
)

$libFiles | ForEach-Object {
    $src = Join-Path $VcpkgLib $_
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $LibDir -Force
        Write-Host "  Copied: $_"
    } else {
        Write-Host "  Warning: $_ not found, skipping"
    }
}

# Copy all absl_*.lib files
$abslLibs = Get-ChildItem -Path $VcpkgLib -Filter "absl_*.lib"
if ($abslLibs) {
    $abslLibs | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $LibDir -Force
    }
    Write-Host "  Copied: $($abslLibs.Count) absl_*.lib files"
} else {
    Write-Host "  Warning: No absl_*.lib files found"
}

Write-Host ""
Write-Host "=== Dependency setup complete ==="

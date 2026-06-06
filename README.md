# PDFium CMake Support

Build [PDFium](https://pdfium.googlesource.com/pdfium/) with **CMake + Clang + Ninja**, replacing the original GN build system.

## Quick Start

```bash
# Prerequisites: CMake, LLVM/Clang 19+, Ninja
# Install: winget install Kitware.CMake LLVM.LLVM Ninja-build.Ninja

# Build (Release with example)
python build.py --clean --examples

# Run the example
build/cmake_build/bin/hello_pdfium.exe test.pdf
```

## Build Options

| Command | Description |
|---------|-------------|
| `python build.py` | Release build |
| `python build.py --debug` | Debug build |
| `python build.py --clean --examples` | Clean rebuild with example |
| `python build.py --no-build` | Configure only |
| `python build.py --install-deps` | Install vcpkg dependencies |
| `python build.py --freeze-deps` | Freeze vcpkg → deps/ |
| `.\build.ps1 -Examples` | PowerShell equivalent |

## Dependency Management

Three ways to handle dependencies:

1. **Frozen deps** (`deps/`) — pre-built, self-contained, ready to use
2. **vcpkg** — `python build.py --install-deps` auto-installs from `vcpkg.json`
3. **System** — winget for LLVM, Ninja, CMake

### Build Script

```bash
python build.py --install-deps   # Install deps via vcpkg
python build.py --freeze-deps    # Freeze vcpkg → deps/ for reproducibility
python build.py --examples       # Build with examples
```

## Project Structure

```
├── build.py                Python build script (primary)
├── build.ps1               PowerShell build script (alternative)
├── vcpkg.json              vcpkg manifest
├── CHANGELOG.md            Source modification log
├── cmake/                  CMake helper scripts
├── core/                   Core PDFium libraries
├── third_party/            Bundled third-party sources
├── fpdfsdk/                Public FPDF SDK
├── examples/               Example programs
└── deps/
    ├── bin/                Build tools (Clang, Ninja, LLVM)
    ├── include/            Library headers
    └── lib/                Library binaries
```

## Source Modifications

Only **2 files** were modified from the original PDFium source.
See [CHANGELOG.md](./CHANGELOG.md) for details.

## License

PDFium: BSD-style license. See LICENSE file in original source.

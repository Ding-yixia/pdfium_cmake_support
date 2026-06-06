# CHANGELOG — PDFium CMake + Clang Port

All modifications to the original PDFium source code are documented here.

Original source reference: `C:\Code\pdfium_all_code\pdfium` (GN + Ninja build system)
Current build: CMake + Ninja + Clang

---

## 🔧 Source Code Changes

### 1. `core/fpdfdoc/cpdf_nametree.cpp`

**Line 21** — Changed abseil include path

```cpp
// BEFORE (original):
#include "third_party/abseil-cpp/absl/container/flat_hash_set.h"

// AFTER (modified):
#include <absl/container/flat_hash_set.h>
```

**Reason**: When using vcpkg-installed abseil (instead of the bundled third_party/abseil-cpp),
the header is found via the vcpkg include path. The `<absl/...>` form is the canonical
include path for system/vcpkg-installed abseil.

### 2. `core/fpdfapi/page/cpdf_sampledfunc.cpp`

**Line 20** — Changed abseil include path

```cpp
// BEFORE (original):
#include "third_party/abseil-cpp/absl/container/inlined_vector.h"

// AFTER (modified):
#include <absl/container/inlined_vector.h>
```

**Reason**: Same as above — use canonical abseil include path for vcpkg version.

---

## 📁 New Files Created

### Build System

| File | Description |
|------|-------------|
| `CMakeLists.txt` | Root CMake build configuration |
| `cmake/helpers.cmake` | CMake helper macros (`pdfium_set_third_party_props`) |
| `constants/CMakeLists.txt` | Header-only constants library |
| `third_party/CMakeLists.txt` | All third-party dependency targets |
| `core/CMakeLists.txt` | Core subdirectory aggregator |
| `core/fxcrt/CMakeLists.txt` | Core runtime library |
| `core/fdrm/CMakeLists.txt` | DRM / encryption |
| `core/fxge/CMakeLists.txt` | Graphics engine |
| `core/fxcodec/CMakeLists.txt` | Codec library (jpeg, fax, flate, jpx) |
| `core/fpdfapi/CMakeLists.txt` | PDF API aggregator |
| `core/fpdfapi/cmaps/CMakeLists.txt` | CJK character maps |
| `core/fpdfapi/font/CMakeLists.txt` | Font handling |
| `core/fpdfapi/parser/CMakeLists.txt` | PDF parser |
| `core/fpdfapi/page/CMakeLists.txt` | Page tree & content |
| `core/fpdfapi/edit/CMakeLists.txt` | Document editing |
| `core/fpdfapi/render/CMakeLists.txt` | Rendering engine |
| `core/fpdfdoc/CMakeLists.txt` | Document model |
| `core/fpdftext/CMakeLists.txt` | Text extraction |
| `fxjs/CMakeLists.txt` | JavaScript stubs |
| `fpdfsdk/CMakeLists.txt` | Public FPDF API SDK |
| `fpdfsdk/pwl/CMakeLists.txt` | Widget library |
| `fpdfsdk/formfiller/CMakeLists.txt` | Form filler |
| `examples/CMakeLists.txt` | Example program |

### Build Scripts

| File | Description |
|------|-------------|
| `build.py` | Python build script (primary) |
| `build.ps1` | PowerShell build script (alternative) |
| `setup_deps.ps1` | PowerShell dependency setup |
| `vcpkg.json` | vcpkg manifest for dependency management |

### Configuration

| File | Description |
|------|-------------|
| `cmake/jconfig.h` | libjpeg-turbo configuration (no SIMD) |

### Documentation

| File | Description |
|------|-------------|
| `CHANGELOG.md` | This file — all modifications documented |
| `deps/README.md` | Dependency bundle documentation |

---

## 🏗 Build System Architecture

### Dependency Resolution (priority order)

1. **Frozen deps** in `deps/` (pre-built .lib + headers + tools)
2. **System vcpkg** at `C:\Code\vcpkg` (auto-installs from `vcpkg.json`)
3. **System packages** (winget: LLVM, Ninja, CMake)

### Toolchain

| Tool | Source |
|------|--------|
| **Clang** | System LLVM 19 (`C:\Program Files\LLVM\bin`) or frozen `deps/bin/` |
| **Ninja** | System or frozen `deps/bin/` |
| **lld-link** | LLVM bundle |
| **llvm-rc** | LLVM bundle |
| **llvm-lib** | LLVM bundle |

### External Libraries (replaced bundled third_party/*)

| Library | Original Location | Replacement | Reason |
|---------|------------------|-------------|--------|
| **ICU** | `third_party/icu/` (headers only) | vcpkg `icuuc.lib` + `icudt.lib` | Need compiled ICU for unicode support |
| **HarfBuzz** | `third_party/harfbuzz/` (headers + .cc) | vcpkg `harfbuzz.lib` + `harfbuzz-subset.lib` | Too complex to build from bundled source |
| **Abseil** | `third_party/abseil-cpp/` (headers + partial .cc) | vcpkg `absl_*.lib` | Missing compiled .cc files |
| **libjpeg-turbo** | `third_party/libjpeg_turbo/` (full source) | vcpkg `jpeg.lib` | Multi-precision build too complex |

### Remaining Bundled Libraries (still built from source)

| Library | Location |
|---------|----------|
| FreeType | `third_party/freetype/` |
| zlib | `third_party/zlib/` |
| AGG | `third_party/agg23/` |
| LCMS2 | `third_party/lcms/` |
| libopenjpeg | `third_party/libopenjpeg/` |

---

## 🧪 Testing

```powershell
# Build & verify
python build.py --clean --examples
build/cmake_build/bin/hello_pdfium.exe "test.pdf"
# Output: PDFium library initialized successfully!
# Output: Page count: 9
```

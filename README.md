# PDFium CMake Support

Build [PDFium](https://pdfium.googlesource.com/pdfium/) with **CMake + Clang + Ninja**, replacing the original GN build system.

---

## 📋 系统要求 / Prerequisites

### Windows (x64)

| 依赖 | 安装方式 | 说明 |
|------|---------|------|
| **Git** | `winget install Git.Git` | 版本管理 |
| **Git LFS** | `git lfs install` | 大文件支持 |
| **CMake** | `winget install Kitware.CMake` | ≥ 3.20 |
| **LLVM/Clang** | `winget install LLVM.LLVM` | ≥ 19.0，需要 `clang-cl.exe` |
| **Ninja** | `winget install Ninja-build.Ninja` | 构建工具 |
| **Visual Studio 2022** | 手动安装 | 提供 Windows SDK 和 CRT |

> **注意**: 虽然使用 Clang 编译，但仍需 Visual Studio 的 Windows SDK（提供 `kernel32.lib`, `user32.lib` 等系统库和头文件）。
> 如果已安装 Visual Studio，运行 `\Visual Studio Installer\` → 修改 → 勾选"Windows SDK"。

---

## 🚀 快速开始 / Quick Start

### 方式一：使用冻结的依赖（推荐，联网即可）

```bash
# 克隆仓库（需要 Git LFS）
git lfs install
git clone https://github.com/Ding-yixia/pdfium_cmake_support.git
cd pdfium_cmake_support

# 构建（Release + 示例程序）
python build.py --clean --examples

# 运行示例
build/cmake_build/bin/hello_pdfium.exe test.pdf
```

### 方式二：通过 vcpkg 自动管理依赖

```bash
# 1. 安装 vcpkg（如果还没有）
git clone https://github.com/microsoft/vcpkg C:/Code/vcpkg
C:\Code\vcpkg\bootstrap-vcpkg.bat

# 2. 设置环境变量（或让脚本自动检测）
set VCPKG_ROOT=C:\Code\vcpkg

# 3. 安装依赖（自动从 vcpkg.json 读取）
python build.py --install-deps

# 4. 冻结依赖到 deps/ 目录（可选，用于离线构建）
python build.py --freeze-deps

# 5. 构建
python build.py --clean --examples
```

### 方式三：PowerShell

```powershell
.\build.ps1 -Clean -Examples
```

---

## 🛠 构建选项 / Build Options

```bash
python build.py                         # Release 构建（默认）
python build.py --debug                 # Debug 构建
python build.py --clean --examples      # 清理 + 重建 + 示例
python build.py --no-build              # 仅 CMake 配置，不编译
python build.py -j 8                    # 指定并行数（默认 CPU 核数）

# 依赖管理
python build.py --install-deps          # 通过 vcpkg 安装依赖
python build.py --freeze-deps           # 冻结 vcpkg 依赖到 deps/
```

PowerShell 对应选项:

```powershell
.\build.ps1                             # Release
.\build.ps1 -Config Debug               # Debug
.\build.ps1 -Clean -Examples            # 清理 + 示例
.\build.ps1 -Examples -NoBuild          # 仅配置
```

---

## 📁 项目结构 / Project Structure

```
pdfium_cmake_support/
├── build.py                    # Python 构建脚本（主要）
├── build.ps1                   # PowerShell 构建脚本（备用）
├── setup_deps.ps1              # 依赖收集脚本
├── vcpkg.json                  # vcpkg 依赖清单
├── CHANGELOG.md                # 源码修改记录（与原始 PDFium 的差异）
├── CMakeLists.txt              # 根 CMake 配置
├── cmake/helpers.cmake         # CMake 辅助宏
│
├── core/                       # PDFium 核心库（源码 + CMakeLists.txt）
│   ├── fxcrt/                  # 核心运行时
│   ├── fdrm/                   # DRM/加密
│   ├── fxge/                   # 图形引擎
│   ├── fxcodec/                # 编解码器
│   └── fpdfapi/                # PDF API
│       ├── cmaps/              # CJK 字符映射
│       ├── font/               # 字体处理
│       ├── parser/             # PDF 解析
│       ├── page/               # 页面处理
│       ├── edit/               # 编辑功能
│       └── render/             # 渲染
│
├── fpdfsdk/                    # 公共 FPDF SDK
│   ├── pwl/                    # 控件库
│   └── formfiller/             # 表单填充
│
├── fxjs/                       # JavaScript 引擎（桩）
├── constants/                  # 常量定义
├── public/                     # 公共头文件
│
├── examples/                   # 示例程序
│   └── hello_pdfium.cpp        # Hello World 示例
│
├── third_party/                # 第三方依赖（源码编译）
│   ├── freetype/               # FreeType 字体渲染
│   ├── zlib/                   # zlib 压缩
│   ├── agg23/                  # Anti-Grain Geometry
│   ├── lcms/                   # Little CMS 色彩管理
│   ├── libopenjpeg/            # JPEG 2000 编解码
│   ├── libjpeg_turbo/          # JPEG 编解码（回退源码）
│   ├── fast_float/             # 快速浮点解析
│   ├── abseil-cpp/             # Abseil 头文件
│   ├── icu/                    # ICU 头文件
│   └── harfbuzz/               # HarfBuzz 头文件
│
└── deps/                       # 冻结的外部依赖（通过 Git LFS 管理）
    ├── bin/                    # 编译工具
    │   ├── clang-cl.exe        # Clang 编译器
    │   ├── lld-link.exe        # LLVM 链接器
    │   ├── llvm-rc.exe         # 资源编译器
    │   ├── llvm-lib.exe        # 库管理器
    │   ├── llvm-mt.exe         # 清单工具
    │   └── ninja.exe           # Ninja 构建工具
    ├── include/                # 库头文件
    │   ├── absl/               # Abseil
    │   ├── harfbuzz/           # HarfBuzz
    │   ├── unicode/            # ICU
    │   └── jpeglib.h 等        # libjpeg-turbo
    └── lib/                    # 预编译库文件
        ├── icuuc.lib           # ICU Unicode
        ├── icudt.lib           # ICU 数据
        ├── harfbuzz.lib        # HarfBuzz
        ├── harfbuzz-subset.lib # HarfBuzz 子集
        ├── jpeg.lib            # libjpeg-turbo
        ├── turbojpeg.lib       # TurboJPEG API
        └── absl_*.lib          # Abseil（91 个文件）
```

---

## ⚠️ 注意事项 / Important Notes

### 1. Git LFS

大文件通过 Git LFS 管理，克隆前必须先执行：

```bash
git lfs install
```

如果忘记执行，文件会显示为指针而不是实际内容：

```
version https://git-lfs.github.com/spec/v1
oid sha256:...
size 123456789
```

解决方法：`git lfs pull`

### 2. Visual Studio / Windows SDK

构建需要 Windows SDK，即使使用 Clang 编译。如果遇到 LINK 错误，请安装 Visual Studio 并确保包含"Windows SDK"组件。

错误示例：
```
fatal error LNK1104: cannot open file 'kernel32.lib'
```

### 3. deps/ 目录

`deps/` 目录包含预编译的第三方库（约 660 MB），通过 Git LFS 管理。如果不需要这些预编译库，可以：

```bash
# 不拉取 LFS 文件（节省空间）
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/Ding-yixia/pdfium_cmake_support.git

# 然后通过 vcpkg 自行编译依赖
python build.py --install-deps
python build.py --freeze-deps
```

### 4. vs. 原始 PDFium 源码

本项目基于 [PDFium](https://pdfium.googlesource.com/pdfium/) 的 GN 构建系统，将其移植为 CMake + Clang。

**原始源码位置**: `C:\Code\pdfium_all_code\pdfium`（本地参考）

**仅修改了 2 个源文件**（详见 [CHANGELOG.md](./CHANGELOG.md)）：
- `core/fpdfdoc/cpdf_nametree.cpp` — abseil include 路径
- `core/fpdfapi/page/cpdf_sampledfunc.cpp` — abseil include 路径

### 5. 支持的构建配置

| 配置 | 状态 |
|------|------|
| Windows x64 + Clang 19 | ✅ 已验证 |
| V8 支持 | ❌ 未启用 |
| Skia 后端 | ❌ 未启用 |
| PartitionAlloc | ❌ 未启用 |
| Debug | ✅ 支持 |
| 共享库 (DLL) | ✅ 支持 |
| 静态库 | ✅ 支持 |

### 6. 性能提示

首次完整构建大约需要 5-15 分钟（取决于 CPU）。增量构建通常只需要几秒到几十秒。

```bash
# 仅重新编译修改过的文件
python build.py --examples
```

---

## 🔧 故障排除 / Troubleshooting

### LINK : fatal error LNK1104: cannot open file 'kernel32.lib'

需要 Windows SDK。安装 Visual Studio 并选择"使用 C++ 的桌面开发"工作负载。

### 找不到 clang-cl.exe

```bash
winget install LLVM.LLVM
```

### CMake 配置时报错 "CMAKE_RC_COMPILER" 相关

RC 编译器路径中的反斜杠需要转义。我们的脚本已处理此问题。如果手动运行 CMake，请使用正斜杠：

```bash
cmake -DCMAKE_RC_COMPILER="C:/Program Files/LLVM/bin/llvm-rc.exe" ...
```

### Git LFS 文件为指针内容

```bash
git lfs pull
```

---

## 📄 许可 / License

PDFium: BSD-style license. See [LICENSE](./LICENSE) file.

本项目仅提供构建系统配置和脚本，不修改 PDFium 核心源码。

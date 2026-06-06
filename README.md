# PDFium CMake Support

Build [PDFium](https://pdfium.googlesource.com/pdfium/) with **CMake + Clang + Ninja** (or **Visual Studio**),
replacing the original GN build system.

> ⚠ **仅支持 Windows x64 平台** — 仅在 Windows 10/11 x64 上测试验证。
> 其他平台（Linux、macOS、ARM）未经测试，不保证兼容。

---

## 📋 系统要求 / Prerequisites

### Windows (x64)

| 依赖 | 安装方式 | 说明 |
|------|---------|------|
| **Git** | `winget install Git.Git` | 版本管理 |
| **Git LFS** | `git lfs install` | 大文件支持 |
| **CMake** | `winget install Kitware.CMake` | ≥ 3.20 |
| **LLVM/Clang** | `winget install LLVM.LLVM` | ≥ 19.0, 需要 `clang-cl.exe` |
| **Ninja** | `winget install Ninja-build.Ninja` | 构建工具（Ninja 模式需要） |
| **Visual Studio 2022** | 手动安装 | 提供 Windows SDK 和 CRT |

> **注意**:
> - 无论使用 Ninja 还是 VS 生成器，都需要 Visual Studio 的 Windows SDK。
> - 如果已安装 Visual Studio，运行 `Visual Studio Installer` → 修改 → 勾选"使用 C++ 的桌面开发" + "Windows SDK"。
> - 对于 VS 生成器模式，需要额外安装"适用于 VS 的 ClangCL 工具集"组件。
>   使用 Visual Studio Installer → 单个组件 → 搜索 "Clang" → 勾选 "C++ Clang Compiler for Windows"。

---

## 🚀 快速开始 / Quick Start

### 方式一：使用冻结的依赖（推荐）

```bash
# 克隆仓库（需要 Git LFS）
git lfs install
git clone https://github.com/Ding-yixia/pdfium_cmake_support.git
cd pdfium_cmake_support

# Ninja 构建（Release + 示例程序）
python build.py --clean --examples

# 运行示例
build/cmake_build/bin/hello_pdfium.exe test.pdf
```

### 方式二：生成 Visual Studio 工程

```bash
# 生成 VS 2022 解决方案（.sln）
python build.py --vs --examples

# VS 工程位于 build/cmake_build-vs/pdfium.sln
# 直接用 Visual Studio 打开即可编译
```

也可以在 PowerShell 中使用：

```powershell
# Ninja
.\build.ps1 -Clean -Examples

# Visual Studio
.\build.ps1 -UseVS -Examples
```

### 方式三：通过 vcpkg 自动管理依赖

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

---

## 🛠 构建选项 / Build Options

```bash
python build.py                         # Release 构建（Ninja）
python build.py --debug                 # Debug 构建
python build.py --vs                    # 生成 Visual Studio 2022 解决方案
python build.py --clean --examples      # 清理 + 重建 + 示例
python build.py --no-build              # 仅 CMake 配置，不编译
python build.py -j 8                    # 指定并行数（默认 CPU 核数）

# 依赖管理
python build.py --install-deps          # 通过 vcpkg 安装依赖
python build.py --freeze-deps           # 冻结 vcpkg 依赖到 deps/
```

PowerShell 对应选项:

```powershell
.\build.ps1                             # Release（Ninja）
.\build.ps1 -Config Debug               # Debug
.\build.ps1 -UseVS                      # 生成 Visual Studio 解决方案
.\build.ps1 -Clean -Examples            # 清理 + 示例
.\build.ps1 -Examples -NoBuild          # 仅配置
```

### Visual Studio 工程说明

使用 `--vs` 或 `-UseVS` 会生成一个 `build/cmake_build-vs/` 目录，
包含 `pdfium.sln` 解决方案文件。可以直接用 Visual Studio 2022 打开进行：

- **代码浏览**：跳转定义、查找引用、智能提示
- **调试**：设置断点、单步执行、查看变量
- **构建**：使用 MSBuild 构建（而非 Ninja）

VS 生成器使用 **ClangCL** 工具集（Visual Studio 自带的 Clang 集成），
这意味着编译器仍然是 Clang，但构建系统是 MSBuild。

> **注意**：VS 生成器的编译速度通常慢于 Ninja，建议日常开发使用 Ninja，
> 仅在需要 IDE 功能时使用 VS 生成器。

---

## 📁 项目结构 / Project Structure

```
pdfium_cmake_support/
├── build.py                    # Python 构建脚本（主要）
├── build.ps1                   # PowerShell 构建脚本（备用）
├── setup_deps.ps1              # 依赖收集脚本
├── vcpkg.json                  # vcpkg 依赖清单
├── CHANGELOG.md                # 源码修改记录
├── DIFF.md                     # 与原始 GN 源码的完整差异对比
├── LICENSE                     # MIT 协议
├── CMakeLists.txt              # 根 CMake 配置
├── cmake/helpers.cmake         # CMake 辅助宏
│
├── core/                       # PDFium 核心库（源码 + CMakeLists.txt）
│   ├── fxcrt/                  # 核心运行时
│   ├── fdrm/                   # DRM/加密
│   ├── fxge/                   # 图形引擎
│   ├── fxcodec/                # 编解码器
│   └── fpdfapi/                # PDF API（cmaps, font, parser, page, edit, render）
├── fpdfsdk/                    # 公共 FPDF SDK
├── fxjs/                       # JavaScript 引擎（桩）
├── constants/                  # 常量定义
├── public/                     # 公共头文件
├── examples/                   # 示例程序
├── third_party/                # 第三方依赖（源码编译）
└── deps/                       # 冻结的外部依赖（通过 Git LFS 管理）
    ├── bin/                    # 编译工具
    ├── include/                # 库头文件
    └── lib/                    # 预编译库文件
```

---

## ⚠️ 注意事项 / Important Notes

### 1. 平台限制

本项目 **仅在 Windows x64 上测试通过**。其他平台（Linux、macOS、ARM 等）：
- 未经过测试
- CMakeLists.txt 中的路径假设（如 `C:\` 盘符）可能与 Unix 不兼容
- vcpkg 的三元组（`x64-windows-static`）需要调整
- 欢迎贡献跨平台支持

### 2. Git LFS

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

### 3. Visual Studio / Windows SDK

构建需要 Windows SDK，即使使用 Clang 编译。如果遇到 LINK 错误，请安装 Visual Studio 并确保包含"Windows SDK"组件。

错误示例：
```
fatal error LNK1104: cannot open file 'kernel32.lib'
```

### 4. deps/ 目录

`deps/` 目录包含预编译的第三方库（约 660 MB），通过 Git LFS 管理。如果不需要这些预编译库，可以：

```bash
# 不拉取 LFS 文件（节省空间）
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/Ding-yixia/pdfium_cmake_support.git

# 然后通过 vcpkg 自行编译依赖
python build.py --install-deps
python build.py --freeze-deps
```

### 5. vs. 原始 PDFium 源码

本项目基于 [PDFium](https://pdfium.googlesource.com/pdfium/) 的 GN 构建系统，将其移植为 CMake + Clang。

**原始源码位置**: `C:\Code\pdfium_all_code\pdfium`（本地参考）

**仅修改了 2 个源文件**（详见 [CHANGELOG.md](./CHANGELOG.md) 和 [DIFF.md](./DIFF.md)）：
- `core/fpdfdoc/cpdf_nametree.cpp` — abseil include 路径
- `core/fpdfapi/page/cpdf_sampledfunc.cpp` — abseil include 路径

### 6. 支持的构建配置

| 配置 | 状态 |
|------|------|
| Windows x64 + Ninja + Clang | ✅ 已验证 |
| Windows x64 + VS 2022 + ClangCL | ✅ 支持 |
| V8 支持 | ❌ 未启用 |
| Skia 后端 | ❌ 未启用 |
| PartitionAlloc | ❌ 未启用 |
| Debug | ✅ 支持 |
| 共享库 (DLL) | ✅ 支持 |
| 静态库 | ✅ 支持 |

### 7. 性能提示

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

### VS 生成器找不到 ClangCL

如果 `--vs` 模式报错说找不到 ClangCL 工具集：
1. 运行 Visual Studio Installer
2. 点击"修改"
3. 选择"单个组件"选项卡
4. 搜索 "Clang"
5. 勾选 "C++ Clang Compiler for Windows" (版本 17+)
6. 点击"修改"等待安装完成

---

## 📄 许可 / License

本项目采用 **MIT 协议**。

```
MIT License

Copyright (c) 2025 Ding-yixia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

简单来说：
- ✅ **允许商用** — 可以用于商业项目
- ✅ **允许修改** — 可以修改、重构
- ✅ **允许分发** — 可以重新发布
- ✅ **允许再授权** — 可以与其它协议组合使用
- ❗ **必须保留版权声明** — 任何使用本项目的产品必须包含上述版权声明

> 注意：本协议仅适用于 `deps/`、`build.py`、`build.ps1`、`cmake/`、`CMakeLists.txt` 等新增的构建系统文件。
> PDFium 核心源码（`core/`、`fpdfsdk/`、`public/` 等）遵循其原有的 BSD 协议。
> 第三方库（`third_party/*`）遵循各自的开源协议。

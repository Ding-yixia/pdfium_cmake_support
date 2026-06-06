# 完整变更记录 — PDFium CMake 移植

## 概述

本项目基于原始 PDFium GN 构建系统（位于 `C:\Code\pdfium_all_code\pdfium`）进行改造，
将其构建系统从 **GN + Ninja** 移植为 **CMake + Clang + Ninja**。

| 项目 | 原始（GN） | 当前（CMake） |
|------|-----------|-------------|
| 构建系统 | GN (`.gn` / `.gni`) | CMake (`CMakeLists.txt`) |
| 编译器 | Clang (Chromium 定制版) | Clang 19 (系统 LLVM) |
| 构建工具 | GN + Ninja | CMake + Ninja |
| 依赖管理 | gclient + DEPS | vcpkg + 本地 deps/ |
| 第三方库 | 全量源码 | vcpkg 预编译 + 必要源码 |

---

## 第一部分：源文件变更（仅 2 处修改）

### 修改 1：`core/fpdfdoc/cpdf_nametree.cpp`

```diff
- #include "third_party/abseil-cpp/absl/container/flat_hash_set.h"
+ #include <absl/container/flat_hash_set.h>

- #include "constants/catalog.h"
+ // 移除了 constants/catalog.h 的包含（使用字符串字面量替代）

-   RetainPtr<const CPDF_Dictionary> pDests =
-       doc->GetRoot()->GetDictFor(pdfium::catalog::kDests);
+   RetainPtr<const CPDF_Dictionary> pDests = doc->GetRoot()->GetDictFor("Dests");
```

**说明**：
1. abseil 头文件从相对路径改为系统包含路径（匹配 vcpkg 安装的头文件位置）
2. `constants/catalog.h` 包含被移除，相关调用改用字符串字面量（原始代码可能来自不同版本）

### 修改 2：`core/fpdfapi/page/cpdf_sampledfunc.cpp`

```diff
- #include "third_party/abseil-cpp/absl/container/inlined_vector.h"
+ #include <absl/container/inlined_vector.h>
```

**说明**：abseil 头文件从相对路径改为系统包含路径。

---

## 第二部分：新增文件（完整清单）

### 2.1 构建系统 — CMakeLists.txt（共 22 个）

| # | 文件路径 | 功能描述 | 对应原始 GN 文件 |
|---|---------|---------|----------------|
| 1 | `CMakeLists.txt` | 根构建配置：编译器检测、vcpkg 路径、链接规则 | `BUILD.gn` + `.gn` + `pdfium.gni` |
| 2 | `cmake/helpers.cmake` | CMake 辅助宏：`pdfium_set_third_party_props()` | `build/config/compiler/compiler.gni` |
| 3 | `cmake/jconfig.h` | libjpeg-turbo 自定义配置（无 SIMD） | 无对应 |
| 4 | `constants/CMakeLists.txt` | 常量头文件库 | `constants/BUILD.gn` |
| 5 | `core/CMakeLists.txt` | 核心库聚合器 | `core/BUILD.gn` |
| 6 | `core/fxcrt/CMakeLists.txt` | 核心运行时（字符串、内存、XML） | `core/fxcrt/BUILD.gn` |
| 7 | `core/fdrm/CMakeLists.txt` | 加密/DRM 模块 | `core/fdrm/BUILD.gn` |
| 8 | `core/fxge/CMakeLists.txt` | 图形引擎（字体、渲染、路径） | `core/fxge/BUILD.gn` |
| 9 | `core/fxcodec/CMakeLists.txt` | 编解码器（JPEG、Fax、Flate、JPX） | `core/fxcodec/BUILD.gn` |
| 10 | `core/fpdfapi/CMakeLists.txt` | PDF API 聚合器 | `core/fpdfapi/BUILD.gn` |
| 11 | `core/fpdfapi/cmaps/CMakeLists.txt` | CJK 字符映射表 | `core/fpdfapi/cmaps/BUILD.gn` |
| 12 | `core/fpdfapi/font/CMakeLists.txt` | 字体处理 | `core/fpdfapi/font/BUILD.gn` |
| 13 | `core/fpdfapi/parser/CMakeLists.txt` | PDF 解析器 | `core/fpdfapi/parser/BUILD.gn` |
| 14 | `core/fpdfapi/page/CMakeLists.txt` | 页面树与内容 | `core/fpdfapi/page/BUILD.gn` |
| 15 | `core/fpdfapi/edit/CMakeLists.txt` | PDF 编辑功能 | `core/fpdfapi/edit/BUILD.gn` |
| 16 | `core/fpdfapi/render/CMakeLists.txt` | 渲染引擎 | `core/fpdfapi/render/BUILD.gn` |
| 17 | `core/fpdfdoc/CMakeLists.txt` | 文档模型 | `core/fpdfdoc/BUILD.gn` |
| 18 | `core/fpdftext/CMakeLists.txt` | 文本提取 | `core/fpdftext/BUILD.gn` |
| 19 | `fxjs/CMakeLists.txt` | JavaScript 引擎（桩模块） | `fxjs/BUILD.gn` |
| 20 | `fpdfsdk/CMakeLists.txt` | FPDF SDK | `fpdfsdk/BUILD.gn` |
| 21 | `fpdfsdk/pwl/CMakeLists.txt` | 控件库 | `fpdfsdk/pwl/BUILD.gn` |
| 22 | `fpdfsdk/formfiller/CMakeLists.txt` | 表单填充 | `fpdfsdk/formfiller/BUILD.gn` |
| 23 | `examples/CMakeLists.txt` | 示例程序构建 | 新增（原始无） |
| 24 | `third_party/CMakeLists.txt` | 第三方库构建（替代多个 BUILD.gn） | `third_party/*/BUILD.gn` |

> 原始项目中有约 **30+** 个 `BUILD.gn` 文件用于 pdfium 核心构建，现在由 **22** 个 `CMakeLists.txt` 文件平替。
> 另有约 **270+** 个 `.gn`/`.gni` 文件属于 Chromium/Skia/V8 等外部依赖，均被移除。

### 2.2 构建脚本（共 5 个）

| 文件 | 说明 |
|------|------|
| `build.py` | Python 构建脚本（主要）— 自动检测工具链、配置 CMake、构建 |
| `build.ps1` | PowerShell 构建脚本（备用） |
| `setup_deps.ps1` | 依赖收集脚本 — 从 vcpkg 复制库到 deps/ |
| `vcpkg.json` | vcpkg manifest — 列出所有外部依赖版本 |
| `.gitignore` | Git 忽略规则 |
| `.gitattributes` | Git LFS 跟踪规则 |

### 2.3 示例程序（共 2 个）

| 文件 | 说明 |
|------|------|
| `pdfium_main.cpp` | DLL 入口点（Module Entry Point） |
| `examples/hello_pdfium.cpp` | Hello World 示例 — 演示 FPDF_InitLibrary、FPDF_LoadDocument |

### 2.4 文档（共 2 个）

| 文件 | 说明 |
|------|------|
| `README.md` | 项目说明、构建指南、注意事项 |
| `CHANGELOG.md` | 简版变更记录 |
| `DIFF.md` | **本文件** — 完整差异分析 |
| `deps/README.md` | 依赖包说明 |

### 2.5 外部依赖（`deps/` 目录，共约 345 MB）

```
deps/
├── bin/                        编译工具（6 个文件）
│   ├── clang-cl.exe            Clang 23.0.0git（Chromium 定制版）
│   ├── lld-link.exe            LLVM 链接器
│   ├── llvm-rc.exe             资源编译器
│   ├── llvm-lib.exe            库管理器
│   ├── llvm-mt.exe             清单工具
│   └── ninja.exe               Ninja 构建系统
├── include/                    库头文件
│   ├── absl/                   Abseil C++ 库头文件
│   ├── harfbuzz/               HarfBuzz 字体整形头文件
│   ├── unicode/                ICU Unicode 支持头文件
│   ├── jconfig.h / jerror.h / jmorecfg.h / jpeglib.h
├── lib/                        预编译静态库（约 97 个 .lib 文件）
│   ├── icuuc.lib / icudt.lib   ICU 78
│   ├── harfbuzz.lib / harfbuzz-subset.lib  HarfBuzz 8.2.2
│   ├── jpeg.lib / turbojpeg.lib  libjpeg-turbo 3.0.1
│   └── absl_*.lib (91 个)      Abseil 20240116.2
```

---

## 第三部分：移除/未包含的原始内容

### 3.1 移除的顶层目录（7 个）

| 目录 | 原作用 | 移除原因 |
|------|--------|---------|
| `docs/` | PDFium 文档 | 不需要，由 README 替代 |
| `fxbarcode/` | 条形码生成模块 | 未启用，可后续按需添加 |
| `samples/` | C++ 示例 | 由 `examples/` 替代 |
| `skia/` | Skia 渲染后端 GN 配置 | 未启用 Skia |
| `testing/` | 测试框架与测试数据 | 不包含测试框架 |
| `v8/` | V8 JavaScript 引擎 | 未启用 V8 |
| `xfa/` | XFA 表单处理 | 未启用 XFA |

### 3.2 移除的顶层文件（13 个）

| 文件 | 说明 |
|------|------|
| `.clang-format` | Chromium 代码格式化配置 |
| `.rustfmt.toml` | Rust 格式化配置 |
| `.style.yapf` | Python 格式化配置 |
| `.vpython3` | Python 虚拟环境 |
| `codereview.settings` | Gerrit 代码审查配置 |
| `CONTRIBUTING.md` | Chromium 贡献指南 |
| `DEPS` | gclient 依赖声明 |
| `DIR_METADATA` | 目录元数据 |
| `navbar.md` | Gerrit 导航栏 |
| `OWNERS` | 代码审查者列表 |
| `PRESUBMIT_test.py` | 预提交测试 |
| `PRESUBMIT_test_mocks.py` | 预提交测试 Mock |
| `PRESUBMIT.py` | 预提交检查脚本 |

### 3.3 移除的 GN 构建基础设施

**所有 `.gn` 和 `.gni` 文件均被移除**，包括但不限于：

| 类别 | 文件数 | 说明 |
|------|-------|------|
| 根目录 `.gn` / `BUILD.gn` | 3 | 根 GN 构建入口 |
| `base/` 相关 | ~4 | Chromium base 库构建 |
| `build/` 全部 | ~180+ | Chromium 构建基础设施（工具链、编译器配置、模板等） |
| `build_overrides/` | 5 | 构建覆盖配置 |
| `buildtools/` | ~5 | GN 二进制文件等 |
| `core/` 各模块 | 15 | 被 CMakeLists.txt 替代 |
| `fpdfsdk/` | 4 | 被 CMakeLists.txt 替代 |
| `fxbarcode/` | 1 | 未启用 |
| `fxjs/` | 1 | 被 CMakeLists.txt 替代 |
| `skia/` | ~35 | 未启用 Skia |
| `testing/` | 7 | 未包含测试 |
| `third_party/` 各库 | ~50 | 被 CMakeLists.txt + vcpkg 替代 |
| `v8/` | ~40 | 未启用 V8 |
| `xfa/` | 11 | 未启用 XFA |

### 3.4 移除的第三方库源码

以下第三方库的**完整源码**从 `third_party/` 中移除，改为使用 vcpkg 预编译库：

| 库 | 原始大小 | 替代方式 |
|----|---------|---------|
| `third_party/skia/`（含其依赖） | ~1 GB+ | 未启用 |
| `third_party/v8/` | ~500 MB+ | 未启用 |
| `third_party/boringssl/` | ~50 MB | 未启用 |
| `third_party/angle/` | ~200 MB | 未启用 |
| `third_party/llvm-build/` | ~300 MB | 保留在 `deps/bin/` |
| `third_party/llvm-libc/` | ~100 MB | 不需要 |
| `third_party/nasm/` | ~10 MB | 不需要 |
| 其余（protobuf, re2, snappy 等） | 不定 | 不需要 |

### 3.5 保留的第三方库源码（直接从源码编译）

以下库保留源码在 `third_party/` 中构建：

| 库 | 说明 |
|----|------|
| `third_party/freetype/` | FreeType 字体渲染（从源码编译） |
| `third_party/zlib/` | zlib 压缩（从源码编译，无 SIMD） |
| `third_party/agg23/` | Anti-Grain Geometry 渲染引擎 |
| `third_party/lcms/` | Little CMS 色彩管理 |
| `third_party/libopenjpeg/` | JPEG 2000 编解码 |
| `third_party/fast_float/` | 快速浮点数解析（头文件库） |
| `third_party/abseil-cpp/` | 仅保留头文件（库来自 vcpkg） |
| `third_party/icu/` | 仅保留公共头文件（库来自 vcpkg） |
| `third_party/harfbuzz/` | 仅保留头文件（库来自 vcpkg） |
| `third_party/libjpeg_turbo/` | 保留源码（但使用 vcpkg 库） |

---

## 第四部分：核心模块文件数变化详情

| 模块 | 原始文件数 | 当前文件数 | 变化 | 说明 |
|------|----------|-----------|------|------|
| `core/cmaps/` | 65 | 65 | 0 | 未变化 |
| `core/fpdfapi/` | 307 | 263 | -44 | 移除测试/无用文件 |
| `core/fxcodec/` | 93 | 56 | -37 | 移除 libjpeg 源码（用 vcpkg） |
| `core/fxcrt/` | 91 | 34 | -57 | 移除 css/ 等子模块 |
| `core/fxge/` | 84 | 61 | -23 | 移除 fontdata 重复 |
| `core/fpdfdoc/` | 含在 fpdfapi 中 | — | — | — |
| `core/fpdftext/` | 含在 fpdfapi 中 | — | — | — |
| `core/skrifa/` | 3 | 0 | -3 | Rust 字体解析 |
| **core 总计** | **~998** | **764** | **-234** | **约 23% 精简** |

### core/fxcrt 减少的 57 个文件

原始 `core/fxcrt` 包含 `css/` 子目录（约 55 个 CSS 解析相关文件）。在 CMake 构建中，
`css/` 子目录被整体排除，因为 CSS 解析仅在 XFA 模块中使用，而 XFA 未被启用。

### core/fxcodec 减少的 37 个文件

原始 `core/fxcodec` 包含 libjpeg-turbo 的全部源码（约 50+ 个 .c 文件）。
当前使用 vcpkg 的 `jpeg.lib`，因此 `jpeg/` 子目录中的大部分 .c 文件不再编译。
保留了 JPEG 封装层代码。

---

## 第五部分：外部依赖替换详情

### 使用 vcpkg 替代源码编译的库

| 库 | 原始方式 | 当前方式 | 原因 |
|----|---------|---------|------|
| **ICU** (`icuuc`) | `third_party/icu/` 源码编译（~200 个 .c 文件） | vcpkg `icuuc.lib` + `icudt.lib` | 编译需要完整 ICU 数据生成工具链 |
| **HarfBuzz** | `third_party/harfbuzz/` 源码编译（~60 个 .cc 文件） | vcpkg `harfbuzz.lib` + `harfbuzz-subset.lib` | harfbuzz-subset 编译复杂 |
| **Abseil** | `third_party/abseil-cpp/` 源码编译（部分 .cc 缺失） | vcpkg `absl_*.lib`（91 个库） | 原始源码缺少部分编译单元 |
| **libjpeg-turbo** | `third_party/libjpeg_turbo/` 源码编译（需多精度编译） | vcpkg `jpeg.lib` | 多精度编译（8/12/16-bit 同时编译）极复杂 |

### 仍然从源码编译的库

| 库 | 源码位置 | 说明 |
|----|---------|------|
| FreeType | `third_party/freetype/` | ~18 个 C 文件，编译稳定 |
| zlib | `third_party/zlib/` | ~15 个 C 文件（无 SIMD） |
| AGG23 | `third_party/agg23/` | ~15 个 C++ 文件 |
| LCMS2 | `third_party/lcms/` | ~30 个 C 文件 |
| libopenjpeg | `third_party/libopenjpeg/` | ~25 个 C 文件 |

---

## 第六部分：文件清单（完整）

### 6.1 所有 CMakeLists.txt（22 个）

```
CMakeLists.txt
cmake/helpers.cmake
constants/CMakeLists.txt
core/CMakeLists.txt
core/fxcrt/CMakeLists.txt
core/fdrm/CMakeLists.txt
core/fxge/CMakeLists.txt
core/fxcodec/CMakeLists.txt
core/fpdfapi/CMakeLists.txt
core/fpdfapi/cmaps/CMakeLists.txt
core/fpdfapi/font/CMakeLists.txt
core/fpdfapi/parser/CMakeLists.txt
core/fpdfapi/page/CMakeLists.txt
core/fpdfapi/edit/CMakeLists.txt
core/fpdfapi/render/CMakeLists.txt
core/fpdfdoc/CMakeLists.txt
core/fpdftext/CMakeLists.txt
fxjs/CMakeLists.txt
fpdfsdk/CMakeLists.txt
fpdfsdk/pwl/CMakeLists.txt
fpdfsdk/formfiller/CMakeLists.txt
third_party/CMakeLists.txt
examples/CMakeLists.txt
```

### 6.2 所有构建脚本与配置（9 个）

```
build.py
build.ps1
setup_deps.ps1
vcpkg.json
.gitignore
.gitattributes
cmake/jconfig.h
cmake/helpers.cmake
deps/README.md
```

### 6.3 所有文档（4 个）

```
README.md
CHANGELOG.md
DIFF.md
deps/README.md
```

### 6.4 示例与入口（2 个）

```
pdfium_main.cpp
examples/hello_pdfium.cpp
examples/CMakeLists.txt
```

---

## 第七部分：构建系统参数差异

| 参数 | GN 构建 | CMake 构建 |
|------|---------|-----------|
| 工具链 | Chromium 定制 Clang 23 | 系统 LLVM Clang 19 |
| C++ 标准 | C++17 | C++20 |
| 运行时库 | `/MT`（静态） | `/MT`（静态） |
| 目标平台 | Windows x64 | Windows x64 |
| 并行数 | `-j` 自动 | `--parallel` / `-j` |
| 输出目录 | `out/Release/` | `build/cmake_build/bin/` |
| 库目录 | `out/Release/obj/` | `build/cmake_build/lib/` |

---

*本文档由 `build.py` 作者维护。最后更新：2025-06*

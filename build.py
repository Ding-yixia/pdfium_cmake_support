#!/usr/bin/env python3
"""
PDFium Build Script — CMake + Clang + vcpkg

Usage:
  python build.py                           # Configure + Build (Release, Ninja)
  python build.py --debug --examples        # Debug build with examples
  python build.py --vs                      # Generate Visual Studio solution
  python build.py --clean                   # Clean rebuild
  python build.py --no-build                # Configure only
  python build.py --install-deps            # Install vcpkg dependencies
  python build.py --freeze-deps             # Freeze deps from vcpkg to deps/
"""

import argparse
import glob as glob_mod
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════
# Paths
# ═══════════════════════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).resolve().parent
BUILD_DIR  = SCRIPT_DIR / "build" / "cmake_build"
DEPS_DIR   = SCRIPT_DIR / "deps"

# New clean deps structure:
#   deps/bin/         — build tools (clang-cl, ninja, llvm-*, …)
#   deps/include/     — library headers
#   deps/lib/         — library .lib files
DEPS_BIN    = DEPS_DIR / "bin"
DEPS_INC    = DEPS_DIR / "include"
DEPS_LIB    = DEPS_DIR / "lib"

# vcpkg — fallback / source for frozen deps
VCPKG_DEFAULT      = Path("C:/Code/vcpkg/installed/x64-windows-static")
VCPKG_EXE_DEFAULT  = Path("C:/Code/vcpkg/vcpkg.exe")

# Clang candidate paths (searched in order)
CLANG_CANDIDATES = [
    DEPS_BIN,                                   # 1) frozen in deps/
    Path("C:/Program Files/LLVM/bin"),           # 2) system LLVM
    Path(os.environ.get("LLVM_ROOT", "")),       # 3) env var
]
CLANG_CANDIDATES = [p for p in CLANG_CANDIDATES if p]


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════
def info(msg: str):
    print(f"  · {msg}")

def step(msg: str):
    print(f"\n── {msg} ─{'─' * max(0, 60 - len(msg))}")

def warn(msg: str):
    print(f"  ⚠ {msg}", file=sys.stderr)

def die(msg: str):
    print(f"\nERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd: list, **kwargs):
    """Run a command; die on failure."""
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        die(f"Command failed (exit {result.returncode}): {' '.join(str(c) for c in cmd)}")
    return result


def find_program(name: str, paths: list[Path]) -> Path | None:
    for p in paths:
        exe = p / name
        if exe.exists():
            return exe
    which = shutil.which(name)
    return Path(which).resolve() if which else None


def find_cmake() -> Path:
    cmake = find_program("cmake.exe", [Path(p) for p in os.environ.get("PATH", "").split(";")])
    if cmake: return cmake
    alt = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "CMake" / "bin" / "cmake.exe"
    if alt.exists(): return alt
    die("CMake not found. Install CMake: winget install Kitware.CMake")


def posix(path: Path) -> str:
    """Return forward-slash path for CMake."""
    return path.as_posix()


# ═══════════════════════════════════════════════════════════════════════════
# Tool detection
# ═══════════════════════════════════════════════════════════════════════════
def detect_tools():
    """Auto-detect build toolchain."""
    tools = {}

    # ── Clang ──
    clang = find_program("clang-cl.exe", CLANG_CANDIDATES)
    if not clang:
        die("clang-cl.exe not found.\n"
            "  Install LLVM: winget install LLVM.LLVM\n"
            "  Or run: python build.py --freeze-deps  (to bundle from vcpkg)")
    tools["clang"] = clang
    info(f"Clang: {clang}")

    # ── Ninja ──
    ninja = find_program("ninja.exe", [DEPS_BIN] + CLANG_CANDIDATES)
    if not ninja:
        ninja = shutil.which("ninja")
    if not ninja:
        die("ninja.exe not found.\n  Install: winget install Ninja-build.Ninja")
    tools["ninja"] = Path(ninja) if isinstance(ninja, (str, Path)) else ninja
    info(f"Ninja: {tools['ninja']}")

    # ── llvm-rc  (resource compiler) ──
    rc = find_program("llvm-rc.exe", [DEPS_BIN] + CLANG_CANDIDATES)
    tools["rc"] = rc
    if rc: info(f"RC:    {rc}")

    # ── llvm-lib (archiver) ──
    lib_exe = find_program("llvm-lib.exe", [DEPS_BIN] + CLANG_CANDIDATES)
    if not lib_exe:
        lib_exe = find_program("lib.exe", CLANG_CANDIDATES + [Path("C:/Program Files/Microsoft Visual Studio/**/bin/Hostx64/x64")])
    tools["lib"] = lib_exe
    if lib_exe: info(f"AR:    {lib_exe}")

    # ── CMake ──
    tools["cmake"] = find_cmake()
    info(f"CMake: {tools['cmake']}")

    return tools


# ═══════════════════════════════════════════════════════════════════════════
# vcpkg integration
# ═══════════════════════════════════════════════════════════════════════════
def find_vcpkg_root() -> Path | None:
    """Locate the vcpkg root directory."""
    # 1) VCPKG_ROOT env var
    env = os.environ.get("VCPKG_ROOT")
    if env:
        p = Path(env)
        if (p / "vcpkg.exe").exists() or (p / "bootstrap-vcpkg.bat").exists():
            return p
    # 2) Known path
    p = Path("C:/Code/vcpkg")
    if (p / "vcpkg.exe").exists():
        return p
    # 3) Sibling of project
    p = SCRIPT_DIR / "vcpkg"
    if (p / "vcpkg.exe").exists():
        return p
    return None


def install_vcpkg_deps():
    """Install vcpkg dependencies for the project (manifest mode)."""
    vcpkg_root = find_vcpkg_root()
    if not vcpkg_root:
        die("vcpkg not found.\n"
            "  Set VCPKG_ROOT env var, or clone vcpkg:\n"
            "  git clone https://github.com/microsoft/vcpkg C:/Code/vcpkg\n"
            "  cd C:/Code/vcpkg && .\\bootstrap-vcpkg.bat")

    vcpkg_exe = vcpkg_root / "vcpkg.exe"
    manifest = SCRIPT_DIR / "vcpkg.json"

    if not manifest.exists():
        die(f"vcpkg manifest not found: {manifest}")

    step("Installing vcpkg dependencies")
    run([
        str(vcpkg_exe), "install",
        f"--x-manifest-root={SCRIPT_DIR}",
        f"--x-install-root={vcpkg_root / 'installed'}",
        "--triplet=x64-windows-static",
        "--vcpkg-root", str(vcpkg_root),
    ])


def freeze_deps():
    """Copy dependencies from vcpkg to deps/ for reproducible builds."""
    vcpkg_root = find_vcpkg_root()
    if not vcpkg_root:
        die("vcpkg not found.\n  Set VCPKG_ROOT or run --install-deps first.")

    vcpkg_installed = vcpkg_root / "installed" / "x64-windows-static"
    if not vcpkg_installed.exists():
        die(f"vcpkg packages not installed at {vcpkg_installed}.\n  Run: python build.py --install-deps")

    step("Freezing dependencies to deps/")
    for d in [DEPS_BIN, DEPS_INC, DEPS_LIB]:
        d.mkdir(parents=True, exist_ok=True)

    # ── Copy Clang + tools ──
    # Use the bundled Chromium Clang from the full pdfium source
    clang_sources = Path("C:/Code/pdfium_all_code/pdfium/third_party/llvm-build/Release+Asserts/bin")
    sys_llvm = Path("C:/Program Files/LLVM/bin")

    tool_sources = {
        "clang-cl.exe":  clang_sources,
        "lld-link.exe":  clang_sources,
        "llvm-rc.exe":   sys_llvm,
        "llvm-lib.exe":  sys_llvm,
        "llvm-mt.exe":   sys_llvm,
    }

    info("Copying build tools")
    for tool, src_dir in tool_sources.items():
        src = src_dir / tool
        if src.exists():
            shutil.copy2(src, DEPS_BIN / tool)
            print(f"    {tool}")

    # Also find ninja from various sources
    for ninja_src in [
        clang_sources.parent.parent / "ninja" / "ninja.exe",
        sys_llvm / "ninja.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / "ninja.exe",
    ]:
        if ninja_src.exists():
            shutil.copy2(ninja_src, DEPS_BIN / "ninja.exe")
            print(f"    ninja.exe")
            break

    # ── Copy library headers ──
    info("Copying library headers")
    for subdir in ["absl", "harfbuzz", "unicode"]:
        src = vcpkg_installed / "include" / subdir
        if src.exists():
            shutil.copytree(src, DEPS_INC / subdir, dirs_exist_ok=True)
            print(f"    {subdir}/")

    # JPEG headers at root of include
    for h in ["jconfig.h", "jerror.h", "jmorecfg.h", "jpeglib.h"]:
        src = vcpkg_installed / "include" / h
        if src.exists():
            shutil.copy2(src, DEPS_INC / h)
            print(f"    {h}")

    # ── Copy library files ──
    info("Copying library files")
    for pattern in [
        "icuuc.lib", "icudt.lib",
        "harfbuzz.lib", "harfbuzz-subset.lib",
        "jpeg.lib", "turbojpeg.lib",
        "absl_*.lib",
    ]:
        files = list((vcpkg_installed / "lib").glob(pattern))
        for f in files:
            shutil.copy2(f, DEPS_LIB / f.name)
        print(f"    {len(files)} file(s): {pattern}")

    # ── Summary ──
    total = sum(f.stat().st_size for f in DEPS_DIR.rglob("*") if f.is_file())
    print(f"\n  Dependencies frozen to: {DEPS_DIR}")
    print(f"  Total size: {total / (1024*1024):.1f} MB")
    print(f"  Tools: {len(list(DEPS_BIN.glob('*')))} files")
    print(f"  Headers: {len(list(DEPS_INC.rglob('*')))} files")
    print(f"  Libraries: {len(list(DEPS_LIB.glob('*.lib')))} files")


# ═══════════════════════════════════════════════════════════════════════════
# CMake configure & build
# ═══════════════════════════════════════════════════════════════════════════
def configure(tools, args):
    step("Configuring CMake")

    generator = "Visual Studio 17 2022" if args.vs else "Ninja"
    build_suffix = "-vs" if args.vs else ""
    actual_build_dir = SCRIPT_DIR / "build" / f"cmake_build{build_suffix}"

    cmake_args = [
        posix(tools["cmake"]),
        "-S", posix(SCRIPT_DIR),
        "-B", posix(actual_build_dir),
        "-G", generator,
    ]

    # Ninja uses clang-cl directly; VS uses the built-in Clang/ClangCL toolset
    if not args.vs:
        cmake_args += [
            f"-DCMAKE_C_COMPILER={posix(tools['clang'])}",
            f"-DCMAKE_CXX_COMPILER={posix(tools['clang'])}",
            f"-DCMAKE_MAKE_PROGRAM={posix(tools['ninja'])}",
        ]
        if tools.get("rc"):
            cmake_args.append(f"-DCMAKE_RC_COMPILER={posix(tools['rc'])}")
        if tools.get("lib"):
            cmake_args.append(f"-DCMAKE_AR={posix(tools['lib'])}")
    else:
        # VS generator: use ClangCL toolset (requires VS with Clang components)
        cmake_args += ["-T", "ClangCL"]

    cmake_args += [
        f"-DCMAKE_BUILD_TYPE={'Debug' if args.debug else 'Release'}",
    ]

    if args.examples:
        cmake_args.append("-DPDFIUM_BUILD_EXAMPLES=ON")

    print(f"  Source:    {SCRIPT_DIR}")
    print(f"  Build:     {actual_build_dir}")
    print(f"  Generator: {generator}")
    print(f"  Config:    {'Debug' if args.debug else 'Release'}")
    if not args.vs:
        print(f"  Toolchain: Clang {tools['clang'].parent}")
    print()

    run(cmake_args)
    return actual_build_dir


def build(tools, args, build_dir):
    step("Building")
    parallel = args.jobs or os.cpu_count() or 4
    run([posix(tools["cmake"]), "--build", posix(build_dir), "--parallel", str(parallel)])

    step("Build successful")
    if (build_dir / "bin").exists():
        for f in sorted((build_dir / "bin").iterdir()):
            sz = f.stat().st_size
            label = f"{sz/(1024*1024):.1f} MB" if sz > 1e6 else f"{sz/1024:.1f} KB"
            print(f"  {f.name:30s} {label}")
    print()


# ═══════════════════════════════════════════════════════════════════════════
# Main CLI
# ═══════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="Build PDFium with CMake + Clang (+ optional vcpkg)",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--debug",     action="store_true", help="Debug build")
    parser.add_argument("--clean",     action="store_true", help="Clean build dir first")
    parser.add_argument("--no-build",  action="store_true", help="Configure only")
    parser.add_argument("--examples",  action="store_true", help="Build examples")
    parser.add_argument("--vs",        action="store_true", help="Generate Visual Studio 2022 solution instead of Ninja")
    parser.add_argument("-j", "--jobs", type=int, default=0,  help="Parallel build jobs")
    parser.add_argument("--install-deps", action="store_true", help="Install vcpkg deps")
    parser.add_argument("--freeze-deps",  action="store_true", help="Freeze vcpkg → deps/")

    args = parser.parse_args()

    # ── Dependency management subcommands ──
    if args.install_deps:
        install_vcpkg_deps()
        return

    if args.freeze_deps:
        freeze_deps()
        return

    # ── Normal build ──
    if args.clean and BUILD_DIR.exists():
        print("Cleaning build directory …")
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
        print("Done.\n")

    # Check that deps/ exists; warn user if not
    if not DEPS_DIR.exists() or not list(DEPS_LIB.glob("*.lib")):
        warn("deps/ not populated (no frozen libraries found).\n"
             "  Run:  python build.py --freeze-deps\n"
             "  Or:   python build.py --install-deps")

    tools = detect_tools()
    actual_build_dir = configure(tools, args)

    if not args.no_build:
        build(tools, args, actual_build_dir)


if __name__ == "__main__":
    main()

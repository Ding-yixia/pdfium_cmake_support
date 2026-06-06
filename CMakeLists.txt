# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

cmake_minimum_required(VERSION 3.20)
project(pdfium LANGUAGES C CXX)

# Set C++ standard to C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Use static MSVC runtime to match vcpkg libraries (/MT)
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

# Prefer Clang compiler
if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    message(WARNING "PDFium is designed to be built with Clang. Current compiler: ${CMAKE_CXX_COMPILER_ID}")
endif()

# Set root directory for all sub-CMakeLists.txt
set(PDFIUM_ROOT_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# Vcpkg installed libraries location (ICU, Abseil, HarfBuzz, etc.)
# These are bundled in deps/ for reproducibility
set(PDFIUM_DEPS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/deps")
set(VCPKG_INCLUDE_DIR "${PDFIUM_DEPS_DIR}/include")
set(VCPKG_LIB_DIR "${PDFIUM_DEPS_DIR}/lib")

message(STATUS "Deps include: ${VCPKG_INCLUDE_DIR}")
message(STATUS "Deps lib: ${VCPKG_LIB_DIR}")

# ============================================================================
# Build options
# ============================================================================
option(PDF_BUNDLE_FREETYPE "Bundle FreeType from third_party" ON)
option(PDF_ENABLE_V8 "Enable V8 JavaScript support" OFF)
option(PDF_ENABLE_XFA "Enable XFA Forms support" OFF)
option(PDF_USE_PARTITION_ALLOC "Use PartitionAlloc allocator" OFF)
option(PDF_USE_AGG "Use AGG graphics library" ON)
option(PDF_USE_SKIA "Use Skia graphics library" OFF)
option(PDF_ENABLE_FONTATIONS "Enable Fontations library" OFF)
option(PDF_ENABLE_RUST_PNG "Enable Rust PNG decoder/encoder" OFF)
option(PDF_ENABLE_CLICK_LOGGING "Enable click event logging" OFF)
option(PDF_IS_COMPLETE_LIB "Build complete static library" OFF)
option(USE_SYSTEM_ZLIB "Use system zlib" OFF)
option(USE_SYSTEM_LIBJPEG "Use system libjpeg" OFF)
option(USE_SYSTEM_LCMS2 "Use system lcms2" OFF)
option(USE_SYSTEM_LIBOPENJPEG2 "Use system libopenjpeg2" OFF)

# Default to Release build
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Output directory
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ============================================================================
# Common compiler flags and defines
# ============================================================================
set(PDFIUM_COMMON_CFLAGS "")
set(PDFIUM_COMMON_CXXFLAGS "")
set(PDFIUM_COMMON_DEFINES "")
set(PDFIUM_PUBLIC_DEFINES "")

# Platform-specific settings
if(WIN32)
    # NOMINMAX is critical - must be global for ALL targets including third_party
    add_compile_definitions(NOMINMAX WIN32_LEAN_AND_MEAN UNICODE _UNICODE _CRT_SECURE_NO_WARNINGS)
    list(APPEND PDFIUM_COMMON_DEFINES NOMINMAX WIN32_LEAN_AND_MEAN UNICODE _UNICODE _CRT_SECURE_NO_WARNINGS)
    if(CMAKE_CXX_SIMULATE_ID STREQUAL "MSVC")
        # clang-cl (MSVC-compatible mode)
        list(APPEND PDFIUM_COMMON_CFLAGS "/utf-8")
    elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
        list(APPEND PDFIUM_COMMON_CFLAGS "/utf-8")
    elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        # Native Clang on Windows (GNU-like)
        list(APPEND PDFIUM_COMMON_CFLAGS "-finput-charset=utf-8" "-fexec-charset=utf-8")
    endif()
elseif(APPLE)
    find_library(APPKIT_FRAMEWORK AppKit)
    find_library(COREFOUNDATION_FRAMEWORK CoreFoundation)
    list(APPEND PDFIUM_SYSTEM_LIBS ${APPKIT_FRAMEWORK} ${COREFOUNDATION_FRAMEWORK})
endif()

# Clang-specific flags
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    list(APPEND PDFIUM_COMMON_CXXFLAGS
        "-Wc++11-narrowing"
        "-Wtautological-unsigned-zero-compare"
    )

    if(UNIX AND NOT APPLE)
        list(APPEND PDFIUM_COMMON_CXXFLAGS
            "-Wnarrowing"
            "-Wno-return-type"
        )
    endif()
endif()

# Feature defines (both internal and public)
if(PDF_ENABLE_CLICK_LOGGING)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_ENABLE_CLICK_LOGGING)
endif()

if(PDF_USE_PARTITION_ALLOC)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_USE_PARTITION_ALLOC)
endif()

if(PDF_ENABLE_V8)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_ENABLE_V8)
    list(APPEND PDFIUM_PUBLIC_DEFINES PDF_ENABLE_V8)
endif()

if(PDF_USE_AGG)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_USE_AGG)
    list(APPEND PDFIUM_PUBLIC_DEFINES PDF_USE_AGG)
endif()

if(PDF_USE_SKIA)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_USE_SKIA)
    list(APPEND PDFIUM_PUBLIC_DEFINES PDF_USE_SKIA)
endif()

if(PDF_USE_SKIA AND PDF_ENABLE_FONTATIONS)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_ENABLE_FONTATIONS)
endif()

if(PDF_USE_SKIA AND PDF_ENABLE_RUST_PNG)
    list(APPEND PDFIUM_COMMON_DEFINES PDF_ENABLE_RUST_PNG)
endif()

# ============================================================================
# freetype_common - wraps fx_freetype or system freetype
# ============================================================================
if(PDF_BUNDLE_FREETYPE)
    add_library(freetype_common INTERFACE)
    target_link_libraries(freetype_common INTERFACE fx_freetype)
else()
    add_library(freetype_common INTERFACE)
    # TODO: support system freetype
    message(FATAL_ERROR "System FreeType not yet supported in CMake build")
endif()

# ============================================================================
# pdfium_public_headers - INTERFACE library for public API consumers
# ============================================================================
add_library(pdfium_public_headers INTERFACE)
target_include_directories(pdfium_public_headers INTERFACE
    ${PDFIUM_ROOT_DIR}
    ${PDFIUM_ROOT_DIR}/public
)
target_compile_definitions(pdfium_public_headers INTERFACE
    FPDF_IMPLEMENTATION
    ${PDFIUM_PUBLIC_DEFINES}
)

# ============================================================================
# Add subdirectories
# ============================================================================
add_subdirectory(constants)
add_subdirectory(third_party)
add_subdirectory(core)
add_subdirectory(fxjs)
add_subdirectory(fpdfsdk)

# ============================================================================
# Main pdfium shared library
# ============================================================================
add_library(pdfium SHARED
    pdfium_main.cpp
)

target_link_libraries(pdfium PRIVATE
    # Core
    core_fxcrt
    core_fdrm
    core_fxge
    core_fxcodec
    core_fpdfapi_cmaps
    core_fpdfapi_font
    core_fpdfapi_parser
    core_fpdfapi_page
    core_fpdfapi_render
    core_fpdfapi_edit
    core_fpdfapi_edit_contentstream_write_utils
    core_fpdfdoc
    core_fpdftext
    constants
    # SDK
    fpdfsdk
    fpdfsdk_pwl
    fpdfsdk_formfiller
    # JS
    fxjs
    # System libs
    ${PDFIUM_SYSTEM_LIBS}
)

# Include directories
target_include_directories(pdfium PUBLIC
    ${PDFIUM_ROOT_DIR}
    ${PDFIUM_ROOT_DIR}/public
)

target_compile_definitions(pdfium PRIVATE ${PDFIUM_COMMON_DEFINES})
target_compile_options(pdfium PRIVATE
    $<$<COMPILE_LANGUAGE:C>:${PDFIUM_COMMON_CFLAGS}>
    $<$<COMPILE_LANGUAGE:CXX>:${PDFIUM_COMMON_CXXFLAGS}>
)

if(WIN32)
    target_link_libraries(pdfium PRIVATE advapi32 gdi32 user32)
endif()

# Set output name
set_target_properties(pdfium PROPERTIES
    OUTPUT_NAME pdfium
    POSITION_INDEPENDENT_CODE ON
)

# If building as complete static library
if(PDF_IS_COMPLETE_LIB)
    set_target_properties(pdfium PROPERTIES
        STATIC_LIBRARY_OPTIONS "--whole-archive"
    )
endif()

# ============================================================================
# Build summary
# ============================================================================

option(PDFIUM_BUILD_EXAMPLES "Build pdfium example programs" OFF)
if(PDFIUM_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

message(STATUS "PDFium configuration:")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Bundle FreeType: ${PDF_BUNDLE_FREETYPE}")
message(STATUS "  Enable V8: ${PDF_ENABLE_V8}")
message(STATUS "  Use AGG: ${PDF_USE_AGG}")
message(STATUS "  Use Skia: ${PDF_USE_SKIA}")
message(STATUS "  Use PartitionAlloc: ${PDF_USE_PARTITION_ALLOC}")
message(STATUS "  Output: ${CMAKE_BINARY_DIR}/bin/pdfium${CMAKE_SHARED_LIBRARY_SUFFIX}")

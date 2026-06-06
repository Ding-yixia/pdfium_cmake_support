# Copyright 2014 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# CMake build for PDFium third-party libraries.
#
# This file creates STATIC/INTERFACE library targets corresponding to the
# GN source_set/group targets in third_party/BUILD.gn.
#
# Required CMake variables (set before including this file):
#   PDFIUM_ROOT  - path to the pdfium root directory (or use CMAKE_CURRENT_SOURCE_DIR/..)
#
# Optional variables:
#   ICUUC_LIBRARY - path to icuuc library (default: icuuc)
#   JPEG_LIBRARY  - path to jpeg library (default: jpeg)

cmake_minimum_required(VERSION 3.14)

# ---- Helper: suppress warnings for third-party code ----
function(pdfium_set_third_party_props target)
  target_compile_options(${target} PRIVATE
    $<$<CXX_COMPILER_ID:Clang>:-Wno-unused-parameter>
    $<$<CXX_COMPILER_ID:Clang>:-Wno-sign-conversion>
    $<$<CXX_COMPILER_ID:GNU>:-Wno-unused-parameter>
  )
  # Suppress MSVC warnings for old code
  if(MSVC)
    target_compile_options(${target} PRIVATE /W0)
  endif()
endfunction()



# ============================================================================
# 1. fx_lcms2 - Little CMS color engine
# ============================================================================
add_library(fx_lcms2 STATIC)
pdfium_set_third_party_props(fx_lcms2)

target_include_directories(fx_lcms2
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src"
)

target_sources(fx_lcms2
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsalpha.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmscam02.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmscgats.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmscnvrt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmserr.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsgamma.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsgmt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmshalf.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsintrp.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsio0.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsio1.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmslut.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsmd5.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsmtrx.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsnamed.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsopt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmspack.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmspcs.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsplugin.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsps2.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmssamp.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmssm.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmstypes.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsvirt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmswtpnt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/lcms/src/cmsxform.c"
)

target_compile_options(fx_lcms2
  PRIVATE
    $<$<CXX_COMPILER_ID:Clang>:-Wno-missing-braces>
    $<$<CXX_COMPILER_ID:Clang>:-Wno-implicit-int-float-conversion>
)

target_link_libraries(fx_lcms2 PRIVATE core_fxcrt)

# ============================================================================
# 2. fx_libopenjpeg - OpenJPEG JPEG2000 decoder
# ============================================================================
add_library(fx_libopenjpeg STATIC)
pdfium_set_third_party_props(fx_libopenjpeg)

target_compile_definitions(fx_libopenjpeg
  PRIVATE
    OPJ_STATIC
)

target_include_directories(fx_libopenjpeg
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg"
)

target_sources(fx_libopenjpeg
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/bio.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/cio.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/dwt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/event.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/function_list.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/ht_dec.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/image.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/invert.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/j2k.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/jp2.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/mct.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/mqc.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/openjpeg.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/opj_malloc.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/pi.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/sparse_array.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/t1.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/t2.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/tcd.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/tgt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/libopenjpeg/thread.c"
)

target_compile_options(fx_libopenjpeg
  PRIVATE
    $<$<CXX_COMPILER_ID:Clang>:-Wno-implicit-int-float-conversion>
    $<$<CXX_COMPILER_ID:Clang>:-Wno-unused-function>
)

target_link_libraries(fx_libopenjpeg PRIVATE core_fxcrt)

# ============================================================================
# 3. fx_agg - Anti-Grain Geometry (AGG v2.3 subset)
# ============================================================================
add_library(fx_agg STATIC)
pdfium_set_third_party_props(fx_agg)

target_include_directories(fx_agg
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/agg23"
)

target_sources(fx_agg
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/agg23/agg_curves.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/agg23/agg_path_storage.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/agg23/agg_rasterizer_scanline_aa.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/agg23/agg_vcgen_dash.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/agg23/agg_vcgen_stroke.cpp"
)

target_compile_options(fx_agg
  PRIVATE
    $<$<CXX_COMPILER_ID:Clang>:-Wno-unused-function>
)

target_link_libraries(fx_agg PRIVATE core_fxcrt)

# ============================================================================
# 4. fx_freetype - FreeType font rasterizer
# ============================================================================
add_library(fx_freetype STATIC)
pdfium_set_third_party_props(fx_freetype)

target_compile_definitions(fx_freetype
  PRIVATE
    FT2_BUILD_LIBRARY
)

target_include_directories(fx_freetype
  PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/include"
)

target_compile_definitions(fx_freetype
  PUBLIC
    FT_CONFIG_MODULES_H="freetype-custom-config/ftmodule.h"
    FT_CONFIG_OPTIONS_H="freetype-custom-config/ftoption.h"
)

target_sources(fx_freetype
  PRIVATE
    # Source files
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftbase.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftbitmap.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftdebug.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftfstype.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftglyph.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftinit.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftmm.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/base/ftsystem.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/cff/cff.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/cid/type1cid.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/psaux/psaux.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/pshinter/pshinter.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/psnames/psmodule.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/raster/raster.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/sfnt/sfnt.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/smooth/smooth.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/truetype/truetype.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/freetype/src/src/type1/type1.c"
)

target_compile_options(fx_freetype
  PRIVATE
    $<$<CXX_COMPILER_ID:Clang>:-Wno-unused-function>
    $<$<CXX_COMPILER_ID:Clang>:-Wno-implicit-int-float-conversion>
    $<$<CXX_COMPILER_ID:GNU>:-Wno-unused-function>
)

# ============================================================================
# 5. fx_zlib - zlib compression library
# ============================================================================
add_library(fx_zlib STATIC)
pdfium_set_third_party_props(fx_zlib)

target_compile_definitions(fx_zlib
  PRIVATE
    ZLIB_IMPLEMENTATION
    CPU_NO_SIMD
)

if(WIN32)
    target_compile_definitions(fx_zlib PRIVATE X86_WINDOWS)
endif()

target_include_directories(fx_zlib
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib"
)

target_sources(fx_zlib
  PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/adler32.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/compress.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/crc32.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/deflate.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/gzclose.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/gzlib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/gzread.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/gzwrite.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/infback.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/inffast.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/inflate.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/inftrees.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/trees.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/uncompr.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/zlib/zutil.c"
)

target_compile_options(fx_zlib
  PRIVATE
    $<$<CXX_COMPILER_ID:Clang>:-Wno-incompatible-pointer-types>
    $<$<CXX_COMPILER_ID:GNU>:-Wno-incompatible-pointer-types>
)

# ============================================================================
# 6. fx_jpeg - libjpeg-turbo (from vcpkg)
# ============================================================================
# Use vcpkg's pre-built jpeg library instead of building from source,
# since building the multi-precision libjpeg-turbo correctly requires
# compiling source files multiple times with different BITS_IN_JSAMPLE.
add_library(fx_jpeg INTERFACE)

target_include_directories(fx_jpeg
  INTERFACE
    "${VCPKG_INCLUDE_DIR}"
)

target_compile_definitions(fx_jpeg
  INTERFACE
    USE_LIBJPEG_TURBO=1
)

target_link_libraries(fx_jpeg
  INTERFACE
    "${VCPKG_LIB_DIR}/jpeg.lib"
)

# ============================================================================
# 7. fast_float - Fast float parsing (header-only)
# ============================================================================
add_library(fast_float INTERFACE)

target_include_directories(fast_float
  INTERFACE
    "${CMAKE_CURRENT_SOURCE_DIR}/fast_float/src/include"
)

# ============================================================================
# 8. icuuc - ICU Unicode support (from vcpkg)
# ============================================================================
add_library(icuuc INTERFACE)

target_include_directories(icuuc
  INTERFACE
    "${VCPKG_INCLUDE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/icu/source/common"
)

target_compile_definitions(icuuc
  INTERFACE
    U_USING_ICU_NAMESPACE=0
    U_ENABLE_DYLOAD=0
    USE_CHROMIUM_ICU=1
)

target_link_libraries(icuuc
  INTERFACE
    "${VCPKG_LIB_DIR}/icuuc.lib"
    "${VCPKG_LIB_DIR}/icudt.lib"
)

# ============================================================================
# 9. harfbuzz - Text shaping library (from vcpkg)
# ============================================================================
add_library(harfbuzz INTERFACE)

target_include_directories(harfbuzz
  INTERFACE
    "${VCPKG_INCLUDE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/harfbuzz"
    "${CMAKE_CURRENT_SOURCE_DIR}/harfbuzz/src/src"
)

target_link_libraries(harfbuzz
  INTERFACE
    "${VCPKG_LIB_DIR}/harfbuzz.lib"
    "${VCPKG_LIB_DIR}/harfbuzz-subset.lib"
)

# ============================================================================
# 10. abseil-cpp (from vcpkg - headers and libraries)
# ============================================================================
add_library(absl INTERFACE)

target_include_directories(absl
  INTERFACE
    "${VCPKG_INCLUDE_DIR}"
)

# Link vcpkg abseil libraries
target_link_libraries(absl
  INTERFACE
    "${VCPKG_LIB_DIR}/absl_raw_hash_set.lib"
    "${VCPKG_LIB_DIR}/absl_hash.lib"
    "${VCPKG_LIB_DIR}/absl_city.lib"
    "${VCPKG_LIB_DIR}/absl_int128.lib"
    "${VCPKG_LIB_DIR}/absl_strings.lib"
    "${VCPKG_LIB_DIR}/absl_strings_internal.lib"
    "${VCPKG_LIB_DIR}/absl_base.lib"
    "${VCPKG_LIB_DIR}/absl_throw_delegate.lib"
    "${VCPKG_LIB_DIR}/absl_raw_logging_internal.lib"
    "${VCPKG_LIB_DIR}/absl_log_severity.lib"
    "${VCPKG_LIB_DIR}/absl_debugging_internal.lib"
    "${VCPKG_LIB_DIR}/absl_demangle_internal.lib"
    "${VCPKG_LIB_DIR}/absl_stacktrace.lib"
    "${VCPKG_LIB_DIR}/absl_symbolize.lib"
    "${VCPKG_LIB_DIR}/absl_malloc_internal.lib"
    "${VCPKG_LIB_DIR}/absl_synchronization.lib"
    "${VCPKG_LIB_DIR}/absl_time.lib"
    "${VCPKG_LIB_DIR}/absl_time_zone.lib"
    "${VCPKG_LIB_DIR}/absl_spinlock_wait.lib"
    "${VCPKG_LIB_DIR}/absl_exponential_biased.lib"
    "${VCPKG_LIB_DIR}/absl_hashtablez_sampler.lib"
    "${VCPKG_LIB_DIR}/absl_crc_cpu_detect.lib"
    "${VCPKG_LIB_DIR}/absl_crc_internal.lib"
    "${VCPKG_LIB_DIR}/absl_crc32c.lib"
    "${VCPKG_LIB_DIR}/absl_cord.lib"
    "${VCPKG_LIB_DIR}/absl_cord_internal.lib"
    "${VCPKG_LIB_DIR}/absl_graphcycles_internal.lib"
    "${VCPKG_LIB_DIR}/absl_borrowed_fixup_buffer.lib"
    "${VCPKG_LIB_DIR}/absl_kernel_timeout_internal.lib"
)

# Minimal set of abseil libraries needed by pdfium
target_link_libraries(absl
  INTERFACE
    "${VCPKG_LIB_DIR}/absl_raw_hash_set.lib"
    "${VCPKG_LIB_DIR}/absl_hash.lib"
    "${VCPKG_LIB_DIR}/absl_strings.lib"
    "${VCPKG_LIB_DIR}/absl_strings_internal.lib"
    "${VCPKG_LIB_DIR}/absl_int128.lib"
    "${VCPKG_LIB_DIR}/absl_base.lib"
    "${VCPKG_LIB_DIR}/absl_throw_delegate.lib"
    "${VCPKG_LIB_DIR}/absl_raw_logging_internal.lib"
    "${VCPKG_LIB_DIR}/absl_log_severity.lib"
    "${VCPKG_LIB_DIR}/absl_debugging_internal.lib"
    "${VCPKG_LIB_DIR}/absl_demangle_internal.lib"
    "${VCPKG_LIB_DIR}/absl_stacktrace.lib"
    "${VCPKG_LIB_DIR}/absl_symbolize.lib"
    "${VCPKG_LIB_DIR}/absl_malloc_internal.lib"
    "${VCPKG_LIB_DIR}/absl_city.lib"
    "${VCPKG_LIB_DIR}/absl_synchronization.lib"
    "${VCPKG_LIB_DIR}/absl_time.lib"
    "${VCPKG_LIB_DIR}/absl_time_zone.lib"
    "${VCPKG_LIB_DIR}/absl_spinlock_wait.lib"
    "${VCPKG_LIB_DIR}/absl_exponential_biased.lib"
    "${VCPKG_LIB_DIR}/absl_hashtablez_sampler.lib"
    "${VCPKG_LIB_DIR}/absl_crc_cpu_detect.lib"
    "${VCPKG_LIB_DIR}/absl_crc_internal.lib"
    "${VCPKG_LIB_DIR}/absl_crc32c.lib"
    "${VCPKG_LIB_DIR}/absl_cord.lib"
    "${VCPKG_LIB_DIR}/absl_cord_internal.lib"
)

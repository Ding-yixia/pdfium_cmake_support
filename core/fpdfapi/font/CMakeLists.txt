# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdfapi_font STATIC)

target_sources(core_fpdfapi_font PRIVATE
    cpdf_cid2unicodemap.cpp
    cpdf_cidfont.cpp
    cpdf_cmap.cpp
    cpdf_cmapparser.cpp
    cpdf_font.cpp
    cpdf_fontencoding.cpp
    cpdf_fontglobals.cpp
    cpdf_simplefont.cpp
    cpdf_stockfontarray.cpp
    cpdf_tounicodemap.cpp
    cpdf_truetypefont.cpp
    cpdf_type1font.cpp
    cpdf_type3char.cpp
    cpdf_type3font.cpp
)

target_include_directories(core_fpdfapi_font PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_font PUBLIC
    core_fxcrt
)

target_link_libraries(core_fpdfapi_font PRIVATE
    core_fxge
    core_fpdfapi_cmaps
    core_fpdfapi_parser
    constants
)

target_compile_options(core_fpdfapi_font PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_font PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_font PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_font PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

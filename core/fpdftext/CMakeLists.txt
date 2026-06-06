# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdftext STATIC)

target_sources(core_fpdftext PRIVATE
    cpdf_linkextract.cpp
    cpdf_textpage.cpp
    cpdf_textpagefind.cpp
    unicodenormalizationdata.cpp
)

target_include_directories(core_fpdftext PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdftext PUBLIC
    core_fxcrt
)

target_link_libraries(core_fpdftext PRIVATE
    core_fpdfapi_font
    core_fpdfapi_page
    core_fpdfapi_parser
)

target_compile_options(core_fpdftext PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdftext PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdftext PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdftext PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

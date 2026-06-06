# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Content stream write utils (internal helper target)
add_library(core_fpdfapi_edit_contentstream_write_utils STATIC)

target_sources(core_fpdfapi_edit_contentstream_write_utils PRIVATE
    cpdf_contentstream_write_utils.cpp
)

target_include_directories(core_fpdfapi_edit_contentstream_write_utils PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_edit_contentstream_write_utils PUBLIC
    core_fxcrt
)

target_compile_options(core_fpdfapi_edit_contentstream_write_utils PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_edit_contentstream_write_utils PRIVATE ${PDFIUM_COMMON_DEFINES})

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_edit_contentstream_write_utils PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_edit_contentstream_write_utils PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

# Main edit target
add_library(core_fpdfapi_edit STATIC)

target_sources(core_fpdfapi_edit PRIVATE
    cpdf_creator.cpp
    cpdf_font_util.cpp
    cpdf_fontsubsetter.cpp
    cpdf_npagetooneexporter.cpp
    cpdf_pagecontentgenerator.cpp
    cpdf_pagecontentmanager.cpp
    cpdf_pageexporter.cpp
    cpdf_pageorganizer.cpp
    cpdf_stringarchivestream.cpp
)

target_include_directories(core_fpdfapi_edit PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_edit PUBLIC
    core_fxcrt
)

target_link_libraries(core_fpdfapi_edit PRIVATE
    core_fpdfapi_font
    core_fpdfapi_page
    core_fpdfapi_parser
    core_fpdfapi_edit_contentstream_write_utils
    constants
    harfbuzz
)

target_compile_options(core_fpdfapi_edit PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_edit PRIVATE ${PDFIUM_COMMON_DEFINES})

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_edit PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_edit PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

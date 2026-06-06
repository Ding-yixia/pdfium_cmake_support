# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdfdoc STATIC)

target_sources(core_fpdfdoc PRIVATE
    cpdf_aaction.cpp
    cpdf_action.cpp
    cpdf_annot.cpp
    cpdf_annotlist.cpp
    cpdf_apsettings.cpp
    cpdf_bafontmap.cpp
    cpdf_bookmark.cpp
    cpdf_bookmarktree.cpp
    cpdf_color_utils.cpp
    cpdf_defaultappearance.cpp
    cpdf_dest.cpp
    cpdf_filespec.cpp
    cpdf_formcontrol.cpp
    cpdf_formfield.cpp
    cpdf_generateap.cpp
    cpdf_icon.cpp
    cpdf_iconfit.cpp
    cpdf_interactiveform.cpp
    cpdf_link.cpp
    cpdf_linklist.cpp
    cpdf_metadata.cpp
    cpdf_nametree.cpp
    cpdf_numbertree.cpp
    cpdf_pagelabel.cpp
    cpdf_structelement.cpp
    cpdf_structtree.cpp
    cpdf_viewerpreferences.cpp
    cpvt_fontmap.cpp
    cpvt_section.cpp
    cpvt_variabletext.cpp
    cpvt_wordinfo.cpp
)

target_include_directories(core_fpdfdoc PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfdoc PUBLIC
    core_fxcrt
)

target_link_libraries(core_fpdfdoc PRIVATE
    core_fxge
    core_fpdfapi_font
    core_fpdfapi_page
    core_fpdfapi_parser
    core_fpdfapi_render
    core_fpdfapi_edit_contentstream_write_utils
    constants
)

target_compile_options(core_fpdfdoc PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfdoc PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfdoc PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfdoc PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

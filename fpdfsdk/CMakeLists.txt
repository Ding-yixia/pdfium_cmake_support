# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_subdirectory(pwl)
add_subdirectory(formfiller)

add_library(fpdfsdk STATIC)
target_sources(fpdfsdk PRIVATE
    cpdfsdk_annot.cpp
    cpdfsdk_annotiteration.cpp
    cpdfsdk_annotiterator.cpp
    cpdfsdk_appstream.cpp
    cpdfsdk_baannot.cpp
    cpdfsdk_customaccess.cpp
    cpdfsdk_filewriteadapter.cpp
    cpdfsdk_formfillenvironment.cpp
    cpdfsdk_helpers.cpp
    cpdfsdk_interactiveform.cpp
    cpdfsdk_pageview.cpp
    cpdfsdk_pauseadapter.cpp
    cpdfsdk_renderpage.cpp
    cpdfsdk_widget.cpp
    fpdf_annot.cpp
    fpdf_attachment.cpp
    fpdf_catalog.cpp
    fpdf_dataavail.cpp
    fpdf_doc.cpp
    fpdf_editimg.cpp
    fpdf_editpage.cpp
    fpdf_editpath.cpp
    fpdf_edittext.cpp
    fpdf_ext.cpp
    fpdf_flatten.cpp
    fpdf_formfill.cpp
    fpdf_javascript.cpp
    fpdf_ppo.cpp
    fpdf_progressive.cpp
    fpdf_save.cpp
    fpdf_searchex.cpp
    fpdf_signature.cpp
    fpdf_structtree.cpp
    fpdf_sysfontinfo.cpp
    fpdf_text.cpp
    fpdf_thumbnail.cpp
    fpdf_transformpage.cpp
    fpdf_view.cpp
)
target_include_directories(fpdfsdk PUBLIC ${PDFIUM_ROOT_DIR})
target_link_libraries(fpdfsdk PRIVATE
    core_fxcrt
    core_fxge
    core_fdrm
    core_fxcodec
    core_fpdfapi_page
    core_fpdfapi_parser
    core_fpdfapi_edit
    core_fpdfapi_font
    core_fpdfapi_render
    core_fpdfdoc
    core_fpdftext
    fxjs
    constants
    fpdfsdk_formfiller
    fpdfsdk_pwl
)
target_link_libraries(fpdfsdk PUBLIC pdfium_public_headers)
target_compile_options(fpdfsdk PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(fpdfsdk PRIVATE ${PDFIUM_COMMON_DEFINES})

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(fpdfsdk PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(fpdfsdk PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

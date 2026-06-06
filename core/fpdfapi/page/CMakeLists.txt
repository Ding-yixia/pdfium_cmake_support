# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdfapi_page STATIC)

target_sources(core_fpdfapi_page PRIVATE
    cpdf_allstates.cpp
    cpdf_annotcontext.cpp
    cpdf_basedcs.cpp
    cpdf_clippath.cpp
    cpdf_color.cpp
    cpdf_colorspace.cpp
    cpdf_colorstate.cpp
    cpdf_contentmarkitem.cpp
    cpdf_contentmarks.cpp
    cpdf_contentparser.cpp
    cpdf_devicecs.cpp
    cpdf_dib.cpp
    cpdf_docpagedata.cpp
    cpdf_expintfunc.cpp
    cpdf_form.cpp
    cpdf_formobject.cpp
    cpdf_function.cpp
    cpdf_generalstate.cpp
    cpdf_graphicstates.cpp
    cpdf_iccprofile.cpp
    cpdf_image.cpp
    cpdf_imageloader.cpp
    cpdf_imageobject.cpp
    cpdf_indexedcs.cpp
    cpdf_meshstream.cpp
    cpdf_occontext.cpp
    cpdf_page.cpp
    cpdf_pageimagecache.cpp
    cpdf_pagemodule.cpp
    cpdf_pageobject.cpp
    cpdf_pageobjectholder.cpp
    cpdf_path.cpp
    cpdf_pathobject.cpp
    cpdf_pattern.cpp
    cpdf_patterncs.cpp
    cpdf_psengine.cpp
    cpdf_psfunc.cpp
    cpdf_sampledfunc.cpp
    cpdf_shadingobject.cpp
    cpdf_shadingpattern.cpp
    cpdf_stitchfunc.cpp
    cpdf_streamcontentparser.cpp
    cpdf_streamparser.cpp
    cpdf_textobject.cpp
    cpdf_textstate.cpp
    cpdf_tilingpattern.cpp
    cpdf_transferfunc.cpp
    cpdf_transferfuncdib.cpp
    cpdf_transparency.cpp
    jpx_decode_conversion.cpp
)

target_include_directories(core_fpdfapi_page PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_page PUBLIC
    core_fxge
    core_fpdfapi_parser
)

target_link_libraries(core_fpdfapi_page PRIVATE
    core_fxcrt
    core_fxcodec
    core_fpdfapi_font
    constants
)

target_compile_options(core_fpdfapi_page PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_page PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_page PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_page PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

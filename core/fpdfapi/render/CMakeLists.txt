# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdfapi_render STATIC)

target_sources(core_fpdfapi_render PRIVATE
    cpdf_devicebuffer.cpp
    cpdf_docrenderdata.cpp
    cpdf_imagerenderer.cpp
    cpdf_pagerendercontext.cpp
    cpdf_progressiverenderer.cpp
    cpdf_rendercontext.cpp
    cpdf_renderoptions.cpp
    cpdf_rendershading.cpp
    cpdf_renderstatus.cpp
    cpdf_rendertiling.cpp
    cpdf_textrenderer.cpp
    cpdf_type3cache.cpp
    cpdf_type3glyphmap.cpp
)

target_include_directories(core_fpdfapi_render PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_render PUBLIC
    core_fxcrt
)

target_link_libraries(core_fpdfapi_render PRIVATE
    core_fxge
    core_fxcodec
    core_fpdfapi_font
    core_fpdfapi_page
    core_fpdfapi_parser
    constants
)

target_compile_options(core_fpdfapi_render PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_render PRIVATE ${PDFIUM_COMMON_DEFINES})

if(WIN32)
    target_sources(core_fpdfapi_render PRIVATE
        cpdf_scaledrenderbuffer.cpp
        cpdf_windowsrenderdevice.cpp
    )
endif()

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_render PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_render PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

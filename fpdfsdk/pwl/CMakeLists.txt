# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(fpdfsdk_pwl STATIC)
target_sources(fpdfsdk_pwl PRIVATE
    cpwl_button.cpp
    cpwl_caret.cpp
    cpwl_cbbutton.cpp
    cpwl_cblistbox.cpp
    cpwl_combo_box.cpp
    cpwl_edit.cpp
    cpwl_edit_impl.cpp
    cpwl_list_box.cpp
    cpwl_list_ctrl.cpp
    cpwl_sbbutton.cpp
    cpwl_scroll_bar.cpp
    cpwl_special_button.cpp
    cpwl_wnd.cpp
)
target_include_directories(fpdfsdk_pwl PUBLIC ${PDFIUM_ROOT_DIR})
target_link_libraries(fpdfsdk_pwl PRIVATE
    core_fxcrt
    core_fxge
    core_fpdfapi_font
    core_fpdfapi_render
    core_fpdfdoc
    constants
)
target_link_libraries(fpdfsdk_pwl PUBLIC pdfium_public_headers)
target_compile_options(fpdfsdk_pwl PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(fpdfsdk_pwl PRIVATE ${PDFIUM_COMMON_DEFINES})

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(fpdfsdk_pwl PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(fpdfsdk_pwl PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(fpdfsdk_formfiller STATIC)
target_sources(fpdfsdk_formfiller PRIVATE
    cffl_button.cpp
    cffl_checkbox.cpp
    cffl_combobox.cpp
    cffl_fieldaction.cpp
    cffl_formfield.cpp
    cffl_interactiveformfiller.cpp
    cffl_listbox.cpp
    cffl_perwindowdata.cpp
    cffl_pushbutton.cpp
    cffl_radiobutton.cpp
    cffl_textfield.cpp
    cffl_textobject.cpp
)
target_include_directories(fpdfsdk_formfiller PUBLIC ${PDFIUM_ROOT_DIR})
target_link_libraries(fpdfsdk_formfiller PRIVATE
    core_fxcrt
    core_fxge
    core_fpdfapi_page
    core_fpdfdoc
    constants
    fpdfsdk_pwl
)
target_link_libraries(fpdfsdk_formfiller PUBLIC pdfium_public_headers)
target_compile_options(fpdfsdk_formfiller PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(fpdfsdk_formfiller PRIVATE ${PDFIUM_COMMON_DEFINES})

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(fpdfsdk_formfiller PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(fpdfsdk_formfiller PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

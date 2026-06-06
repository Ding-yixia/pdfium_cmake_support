# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(fxjs STATIC)
target_sources(fxjs PRIVATE
    cjs_event_context_stub.cpp
    cjs_runtimestub.cpp
    ijs_runtime.cpp
)
target_include_directories(fxjs PUBLIC ${PDFIUM_ROOT_DIR})
target_link_libraries(fxjs PRIVATE core_fxcrt)
target_compile_options(fxjs PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(fxjs PRIVATE ${PDFIUM_COMMON_DEFINES})

if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(fxjs PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(fxjs PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

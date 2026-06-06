# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fdrm STATIC)

target_sources(core_fdrm PRIVATE
    fx_crypt.cpp
    fx_crypt_aes.cpp
    fx_crypt_sha.cpp
)

target_include_directories(core_fdrm PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fdrm PUBLIC
    core_fxcrt
)

target_compile_options(core_fdrm PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fdrm PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fdrm PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fdrm PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

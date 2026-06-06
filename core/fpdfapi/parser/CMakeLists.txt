# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdfapi_parser STATIC)

target_sources(core_fpdfapi_parser PRIVATE
    cfdf_document.cpp
    cpdf_array.cpp
    cpdf_boolean.cpp
    cpdf_cross_ref_avail.cpp
    cpdf_cross_ref_table.cpp
    cpdf_crypto_handler.cpp
    cpdf_data_avail.cpp
    cpdf_dictionary.cpp
    cpdf_document.cpp
    cpdf_encryptor.cpp
    cpdf_flateencoder.cpp
    cpdf_hint_tables.cpp
    cpdf_indirect_object_holder.cpp
    cpdf_linearized_header.cpp
    cpdf_name.cpp
    cpdf_null.cpp
    cpdf_number.cpp
    cpdf_object.cpp
    cpdf_object_avail.cpp
    cpdf_object_stream.cpp
    cpdf_object_walker.cpp
    cpdf_page_object_avail.cpp
    cpdf_parser.cpp
    cpdf_read_validator.cpp
    cpdf_reference.cpp
    cpdf_security_handler.cpp
    cpdf_seekablemultistream.cpp
    cpdf_simple_parser.cpp
    cpdf_stream.cpp
    cpdf_stream_acc.cpp
    cpdf_string.cpp
    cpdf_syntax_parser.cpp
    fpdf_parser_decode.cpp
    fpdf_parser_utility.cpp
    object_tree_traversal_util.cpp
)

target_include_directories(core_fpdfapi_parser PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_parser PUBLIC
    core_fxcrt
)

target_link_libraries(core_fpdfapi_parser PRIVATE
    core_fdrm
    core_fxcodec
    core_fpdfapi_edit_contentstream_write_utils
    constants
)

target_compile_options(core_fpdfapi_parser PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_parser PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_parser PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_parser PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

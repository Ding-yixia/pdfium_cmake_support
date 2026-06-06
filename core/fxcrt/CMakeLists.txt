# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fxcrt STATIC)

target_sources(core_fxcrt PRIVATE
    binary_buffer.cpp
    bytestring.cpp
    cfx_bitstream.cpp
    cfx_datetime.cpp
    cfx_fileaccess_stream.cpp
    cfx_read_only_container_stream.cpp
    cfx_read_only_span_stream.cpp
    cfx_seekablestreamproxy.cpp
    cfx_timer.cpp
    debug/alias.cc
    fx_bidi.cpp
    fx_codepage.cpp
    fx_coordinates.cpp
    fx_extension.cpp
    fx_memory.cpp
    fx_number.cpp
    fx_random.cpp
    fx_stream.cpp
    fx_string.cpp
    fx_system.cpp
    fx_unicode.cpp
    observed_ptr.cpp
    string_data_template.cpp
    string_template.cpp
    widestring.cpp
    widetext_buffer.cpp
    xml/cfx_xmlchardata.cpp
    xml/cfx_xmldocument.cpp
    xml/cfx_xmlelement.cpp
    xml/cfx_xmlinstruction.cpp
    xml/cfx_xmlnode.cpp
    xml/cfx_xmlparser.cpp
    xml/cfx_xmltext.cpp
)

target_include_directories(core_fxcrt PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fxcrt PUBLIC
    fast_float
    absl
    icuuc
    freetype_common
)

target_compile_options(core_fxcrt PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fxcrt PRIVATE ${PDFIUM_COMMON_DEFINES})

if(WIN32)
    target_sources(core_fxcrt PRIVATE
        cfx_fileaccess_windows.cpp
        code_point_view.cpp
        fx_folder_windows.cpp
        win/win_util.cc
    )
endif()

if(UNIX)
    target_sources(core_fxcrt PRIVATE
        cfx_fileaccess_posix.cpp
        fx_folder_posix.cpp
        mapped_data_bytes.cpp
    )
endif()

# Memory allocator (mutually exclusive)
if(PDF_USE_PARTITION_ALLOC)
    target_sources(core_fxcrt PRIVATE fx_memory_pa.cpp)
else()
    target_sources(core_fxcrt PRIVATE fx_memory_malloc.cpp)
endif()

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fxcrt PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fxcrt PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

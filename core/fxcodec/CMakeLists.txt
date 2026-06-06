# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fxcodec STATIC)

target_sources(core_fxcodec PRIVATE
    basic/basicmodule.cpp
    data_and_bytes_consumed.cpp
    fax/faxmodule.cpp
    flate/flatemodule.cpp
    fx_codec.cpp
    icc/icc_transform.cpp
    jbig2/jbig2_arith_decoder.cpp
    jbig2/jbig2_arith_int_decoder.cpp
    jbig2/jbig2_bit_stream.cpp
    jbig2/jbig2_context.cpp
    jbig2/jbig2_decoder.cpp
    jbig2/jbig2_document_context.cpp
    jbig2/jbig2_grd_proc.cpp
    jbig2/jbig2_grrd_proc.cpp
    jbig2/jbig2_htrd_proc.cpp
    jbig2/jbig2_huffman_decoder.cpp
    jbig2/jbig2_huffman_table.cpp
    jbig2/jbig2_image.cpp
    jbig2/jbig2_pattern_dict.cpp
    jbig2/jbig2_pdd_proc.cpp
    jbig2/jbig2_sdd_proc.cpp
    jbig2/jbig2_segment.cpp
    jbig2/jbig2_symbol_dict.cpp
    jbig2/jbig2_trd_proc.cpp
    jpeg/jpeg_common.c
    jpeg/jpegmodule.cpp
    jpx/cjpx_decoder.cpp
    jpx/jpx_decode_utils.cpp
    scanlinedecoder.cpp
)

target_include_directories(core_fxcodec PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fxcodec PUBLIC
    core_fxcrt
)

target_link_libraries(core_fxcodec PRIVATE
    core_fxge
    fx_zlib
    fx_lcms2
    fx_libopenjpeg
    fx_jpeg
)

target_compile_options(core_fxcodec PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fxcodec PRIVATE ${PDFIUM_COMMON_DEFINES})

if(NOT USE_SYSTEM_LIBOPENJPEG2)
    target_compile_definitions(core_fxcodec PRIVATE OPJ_STATIC)
endif()

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fxcodec PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fxcodec PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

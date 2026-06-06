cmake_minimum_required(VERSION 3.20)
project(pdfium_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set root dir - allows building standalone or as part of the main project
if(NOT PDFIUM_ROOT_DIR)
    set(PDFIUM_ROOT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/..")
endif()

if(NOT PDFIUM_BUILD_DIR)
    set(PDFIUM_BUILD_DIR "${PDFIUM_ROOT_DIR}/build/cmake_build")
endif()

set(PDFIUM_LIB_DIR "${PDFIUM_BUILD_DIR}/lib")

add_executable(hello_pdfium hello_pdfium.cpp)

target_include_directories(hello_pdfium PRIVATE
    ${PDFIUM_ROOT_DIR}
    ${PDFIUM_ROOT_DIR}/public
)

# Link all pdfium static libraries
target_link_libraries(hello_pdfium PRIVATE
    "${PDFIUM_LIB_DIR}/core_fxcrt.lib"
    "${PDFIUM_LIB_DIR}/core_fdrm.lib"
    "${PDFIUM_LIB_DIR}/core_fxge.lib"
    "${PDFIUM_LIB_DIR}/core_fxcodec.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_cmaps.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_font.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_parser.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_page.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_render.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_edit.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfapi_edit_contentstream_write_utils.lib"
    "${PDFIUM_LIB_DIR}/core_fpdfdoc.lib"
    "${PDFIUM_LIB_DIR}/core_fpdftext.lib"
    "${PDFIUM_LIB_DIR}/fpdfsdk.lib"
    "${PDFIUM_LIB_DIR}/fpdfsdk_pwl.lib"
    "${PDFIUM_LIB_DIR}/fpdfsdk_formfiller.lib"
    "${PDFIUM_LIB_DIR}/fxjs.lib"
    "${PDFIUM_LIB_DIR}/fx_agg.lib"
    "${PDFIUM_LIB_DIR}/fx_freetype.lib"
    "${PDFIUM_LIB_DIR}/fx_zlib.lib"
    "${PDFIUM_LIB_DIR}/fx_lcms2.lib"
    "${PDFIUM_LIB_DIR}/fx_libopenjpeg.lib"
)

# Link INTERFACE library targets (they provide vcpkg paths)
target_link_libraries(hello_pdfium PRIVATE
    fx_jpeg
    icuuc
    harfbuzz
    absl
)

# On Windows, pdfium needs these system libs
if(WIN32)
    target_link_libraries(hello_pdfium PRIVATE advapi32 gdi32 user32)
endif()

message(STATUS "PDFium example:")
message(STATUS "  Include: ${PDFIUM_ROOT_DIR}")
message(STATUS "  Library dir: ${PDFIUM_LIB_DIR}")

# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fpdfapi_cmaps STATIC)

target_sources(core_fpdfapi_cmaps PRIVATE
    CNS1/B5pc-H_0.cpp
    CNS1/B5pc-V_0.cpp
    CNS1/CNS-EUC-H_0.cpp
    CNS1/CNS-EUC-V_0.cpp
    CNS1/ETen-B5-H_0.cpp
    CNS1/ETen-B5-V_0.cpp
    CNS1/ETenms-B5-H_0.cpp
    CNS1/ETenms-B5-V_0.cpp
    CNS1/HKscs-B5-H_5.cpp
    CNS1/HKscs-B5-V_5.cpp
    CNS1/UniCNS-UCS2-H_3.cpp
    CNS1/UniCNS-UCS2-V_3.cpp
    CNS1/UniCNS-UTF16-H_0.cpp
    GB1/GB-EUC-H_0.cpp
    GB1/GB-EUC-V_0.cpp
    GB1/GBK-EUC-H_2.cpp
    GB1/GBK-EUC-V_2.cpp
    GB1/GBK2K-H_5.cpp
    GB1/GBK2K-V_5.cpp
    GB1/GBKp-EUC-H_2.cpp
    GB1/GBKp-EUC-V_2.cpp
    GB1/GBpc-EUC-H_0.cpp
    GB1/GBpc-EUC-V_0.cpp
    GB1/UniGB-UCS2-H_4.cpp
    GB1/UniGB-UCS2-V_4.cpp
    Japan1/83pv-RKSJ-H_1.cpp
    Japan1/90ms-RKSJ-H_2.cpp
    Japan1/90ms-RKSJ-V_2.cpp
    Japan1/90msp-RKSJ-H_2.cpp
    Japan1/90msp-RKSJ-V_2.cpp
    Japan1/90pv-RKSJ-H_1.cpp
    Japan1/Add-RKSJ-H_1.cpp
    Japan1/Add-RKSJ-V_1.cpp
    Japan1/EUC-H_1.cpp
    Japan1/EUC-V_1.cpp
    Japan1/Ext-RKSJ-H_2.cpp
    Japan1/Ext-RKSJ-V_2.cpp
    Japan1/H_1.cpp
    Japan1/UniJIS-UCS2-HW-H_4.cpp
    Japan1/UniJIS-UCS2-HW-V_4.cpp
    Japan1/UniJIS-UCS2-H_4.cpp
    Japan1/UniJIS-UCS2-V_4.cpp
    Japan1/V_1.cpp
    Korea1/KSC-EUC-H_0.cpp
    Korea1/KSC-EUC-V_0.cpp
    Korea1/KSCms-UHC-HW-H_1.cpp
    Korea1/KSCms-UHC-HW-V_1.cpp
    Korea1/KSCms-UHC-H_1.cpp
    Korea1/KSCms-UHC-V_1.cpp
    Korea1/KSCpc-EUC-H_0.cpp
    Korea1/UniKS-UCS2-H_1.cpp
    Korea1/UniKS-UCS2-V_1.cpp
    Korea1/UniKS-UTF16-H_0.cpp
    fpdf_cmaps.cpp
)

target_include_directories(core_fpdfapi_cmaps PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fpdfapi_cmaps PUBLIC
    core_fxcrt
)

target_compile_options(core_fpdfapi_cmaps PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fpdfapi_cmaps PRIVATE ${PDFIUM_COMMON_DEFINES})

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fpdfapi_cmaps PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fpdfapi_cmaps PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

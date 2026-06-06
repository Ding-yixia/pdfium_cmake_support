# Helper macros for PDFium CMake build
# Copyright 2024 The PDFium Authors

# Add a pdfium_source_set target (analogous to GN source_set)
# Usage:
#   add_pdfium_source_set(target_name
#       SOURCES src1.cpp src2.cpp ...
#       [DEPS dep1 dep2 ...]
#       [PUBLIC_DEPS dep1 dep2 ...]
#       [PUBLIC_INCLUDES dir1 dir2 ...]
#       [DEFINES def1 def2 ...]
#       [PRIVATE]
#   )
function(add_pdfium_source_set target_name)
    cmake_parse_arguments(PARSE_ARGV 1 ARG "" "" "SOURCES;DEPS;PUBLIC_DEPS;PUBLIC_INCLUDES;DEFINES")

    add_library(${target_name} STATIC)
    target_sources(${target_name} PRIVATE ${ARG_SOURCES})

    target_include_directories(${target_name} PUBLIC
        ${PDFIUM_ROOT_DIR}
    )

    if(ARG_PUBLIC_INCLUDES)
        target_include_directories(${target_name} PUBLIC ${ARG_PUBLIC_INCLUDES})
    endif()

    target_compile_options(${target_name} PRIVATE ${PDFIUM_COMMON_CFLAGS})
    target_compile_definitions(${target_name} PRIVATE ${PDFIUM_COMMON_DEFINES} ${ARG_DEFINES})

    if(ARG_DEPS)
        target_link_libraries(${target_name} PRIVATE ${ARG_DEPS})
    endif()
    if(ARG_PUBLIC_DEPS)
        target_link_libraries(${target_name} PUBLIC ${ARG_PUBLIC_DEPS})
    endif()

    # Apply strict config flags
    if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        target_compile_options(${target_name} PRIVATE
            -Wcovered-switch-default
            -Wshorten-64-to-32
        )
    endif()

    set_target_properties(${target_name} PROPERTIES
        POSITION_INDEPENDENT_CODE ON
    )
endfunction()

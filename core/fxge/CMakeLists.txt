# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(core_fxge STATIC)

target_sources(core_fxge PRIVATE
    calculate_pitch.cpp
    cfx_charmap_resolver.cpp
    cfx_color.cpp
    cfx_cttgsubtable.cpp
    cfx_defaultrenderdevice.cpp
    cfx_drawutils.cpp
    cfx_face.cpp
    cfx_folderfontinfo.cpp
    cfx_font.cpp
    cfx_fontmapper.cpp
    cfx_fontmgr.cpp
    cfx_gemodule.cpp
    cfx_glyphbitmap.cpp
    cfx_glyphcache.cpp
    cfx_graphstate.cpp
    cfx_graphstatedata.cpp
    cfx_path.cpp
    cfx_renderdevice.cpp
    cfx_substfont.cpp
    dib/blend.cpp
    dib/cfx_bitmapstorer.cpp
    dib/cfx_cmyk_to_srgb.cpp
    dib/cfx_dibbase.cpp
    dib/cfx_dibitmap.cpp
    dib/cfx_imagestretcher.cpp
    dib/cfx_imagetransformer.cpp
    dib/cfx_scanlinecompositor.cpp
    dib/cstretchengine.cpp
    dib/fx_dib.cpp
    fontdata/chromefontdata/FoxitDingbats.cpp
    fontdata/chromefontdata/FoxitFixed.cpp
    fontdata/chromefontdata/FoxitFixedBold.cpp
    fontdata/chromefontdata/FoxitFixedBoldItalic.cpp
    fontdata/chromefontdata/FoxitFixedItalic.cpp
    fontdata/chromefontdata/FoxitSans.cpp
    fontdata/chromefontdata/FoxitSansBold.cpp
    fontdata/chromefontdata/FoxitSansBoldItalic.cpp
    fontdata/chromefontdata/FoxitSansItalic.cpp
    fontdata/chromefontdata/FoxitSansMM.cpp
    fontdata/chromefontdata/FoxitSerif.cpp
    fontdata/chromefontdata/FoxitSerifBold.cpp
    fontdata/chromefontdata/FoxitSerifBoldItalic.cpp
    fontdata/chromefontdata/FoxitSerifItalic.cpp
    fontdata/chromefontdata/FoxitSerifMM.cpp
    fontdata/chromefontdata/FoxitSymbol.cpp
    freetype/fx_freetype.cpp
    fx_font.cpp
    renderdevicedriver_iface.cpp
    text_char_pos.cpp
    text_glyph_pos.cpp
)

target_include_directories(core_fxge PUBLIC ${PDFIUM_ROOT_DIR})

target_link_libraries(core_fxge PUBLIC
    core_fxcrt
)

target_compile_options(core_fxge PRIVATE ${PDFIUM_COMMON_CFLAGS})
target_compile_definitions(core_fxge PRIVATE ${PDFIUM_COMMON_DEFINES})

if(PDF_USE_AGG)
    target_sources(core_fxge PRIVATE
        agg/cfx_agg_bitmapcomposer.cpp
        agg/cfx_agg_cliprgn.cpp
        agg/cfx_agg_devicedriver.cpp
        agg/cfx_agg_imagerenderer.cpp
    )
    target_link_libraries(core_fxge PRIVATE fx_agg)
endif()

if(WIN32)
    target_sources(core_fxge PRIVATE
        cfx_windowsrenderdevice.cpp
        win32/cfx_psfonttracker.cpp
        win32/cfx_psrenderer.cpp
        win32/cgdi_device_driver.cpp
        win32/cgdi_display_driver.cpp
        win32/cgdi_plus_ext.cpp
        win32/cgdi_printer_driver.cpp
        win32/cps_printer_driver.cpp
        win32/cpsoutput.cpp
        win32/ctext_only_printer_driver.cpp
        win32/cwin32_platform.cpp
    )
endif()

# Strict config
if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    target_compile_options(core_fxge PRIVATE
        -Wcovered-switch-default
        -Wshorten-64-to-32
    )
endif()

set_target_properties(core_fxge PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

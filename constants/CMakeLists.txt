# Copyright 2025 The PDFium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

add_library(constants INTERFACE)

target_include_directories(constants INTERFACE
    ${PDFIUM_ROOT_DIR}
)

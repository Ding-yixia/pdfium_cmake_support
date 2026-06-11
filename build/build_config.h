// Copyright 2014 The PDFium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// This file adds defines about the platform we're currently building on.
// It also adds defines about which compiler we're using.
//  _BUILD_CONFIG_H_ must be the first include in all compilation units.

#ifndef BUILD_BUILD_CONFIG_H_
#define BUILD_BUILD_CONFIG_H_

#include "build/buildflag.h"

// ---------------------------------------------------------------------------
// Platform identifiers
// ---------------------------------------------------------------------------

// Operating system:
//  IS_WIN / IS_ANDROID / IS_LINUX / IS_APPLE / IS_IOS / IS_MAC /
//  IS_CHROMEOS / IS_FUCHSIA / IS_BSD

#if defined(_WIN32) || defined(_WIN64)
#define OS_WIN 1
#define BUILDFLAG_INTERNAL_IS_WIN() (1)
#define BUILDFLAG_INTERNAL_IS_ANDROID() (0)
#define BUILDFLAG_INTERNAL_IS_LINUX() (0)
#define BUILDFLAG_INTERNAL_IS_CHROMEOS() (0)
#define BUILDFLAG_INTERNAL_IS_APPLE() (0)
#define BUILDFLAG_INTERNAL_IS_IOS() (0)
#define BUILDFLAG_INTERNAL_IS_MAC() (0)
#define BUILDFLAG_INTERNAL_IS_FUCHSIA() (0)
#define BUILDFLAG_INTERNAL_IS_BSD() (0)
#define BUILDFLAG_INTERNAL_IS_POSIX() (0)
#elif defined(__ANDROID__)
#define OS_ANDROID 1
#define BUILDFLAG_INTERNAL_IS_ANDROID() (1)
#define BUILDFLAG_INTERNAL_IS_WIN() (0)
#define BUILDFLAG_INTERNAL_IS_LINUX() (0)
#define BUILDFLAG_INTERNAL_IS_CHROMEOS() (0)
#define BUILDFLAG_INTERNAL_IS_APPLE() (0)
#define BUILDFLAG_INTERNAL_IS_IOS() (0)
#define BUILDFLAG_INTERNAL_IS_MAC() (0)
#define BUILDFLAG_INTERNAL_IS_FUCHSIA() (0)
#define BUILDFLAG_INTERNAL_IS_BSD() (0)
#define BUILDFLAG_INTERNAL_IS_POSIX() (1)
#elif defined(__APPLE__)
#define OS_APPLE 1
#include <TargetConditionals.h>
#if TARGET_OS_IOS
#define OS_IOS 1
#define BUILDFLAG_INTERNAL_IS_IOS() (1)
#define BUILDFLAG_INTERNAL_IS_MAC() (0)
#else
#define OS_MAC 1
#define BUILDFLAG_INTERNAL_IS_MAC() (1)
#define BUILDFLAG_INTERNAL_IS_IOS() (0)
#endif
#define BUILDFLAG_INTERNAL_IS_APPLE() (1)
#define BUILDFLAG_INTERNAL_IS_WIN() (0)
#define BUILDFLAG_INTERNAL_IS_ANDROID() (0)
#define BUILDFLAG_INTERNAL_IS_LINUX() (0)
#define BUILDFLAG_INTERNAL_IS_CHROMEOS() (0)
#define BUILDFLAG_INTERNAL_IS_FUCHSIA() (0)
#define BUILDFLAG_INTERNAL_IS_BSD() (0)
#define BUILDFLAG_INTERNAL_IS_POSIX() (1)
#elif defined(__linux__)
#define OS_LINUX 1
#define BUILDFLAG_INTERNAL_IS_LINUX() (1)
#define BUILDFLAG_INTERNAL_IS_CHROMEOS() (0)
#define BUILDFLAG_INTERNAL_IS_WIN() (0)
#define BUILDFLAG_INTERNAL_IS_ANDROID() (0)
#define BUILDFLAG_INTERNAL_IS_APPLE() (0)
#define BUILDFLAG_INTERNAL_IS_IOS() (0)
#define BUILDFLAG_INTERNAL_IS_MAC() (0)
#define BUILDFLAG_INTERNAL_IS_FUCHSIA() (0)
#define BUILDFLAG_INTERNAL_IS_BSD() (0)
#define BUILDFLAG_INTERNAL_IS_POSIX() (1)
#elif defined(__FreeBSD__) || defined(__OpenBSD__) || defined(__NetBSD__)
#define OS_BSD 1
#define BUILDFLAG_INTERNAL_IS_BSD() (1)
#define BUILDFLAG_INTERNAL_IS_WIN() (0)
#define BUILDFLAG_INTERNAL_IS_ANDROID() (0)
#define BUILDFLAG_INTERNAL_IS_LINUX() (0)
#define BUILDFLAG_INTERNAL_IS_CHROMEOS() (0)
#define BUILDFLAG_INTERNAL_IS_APPLE() (0)
#define BUILDFLAG_INTERNAL_IS_IOS() (0)
#define BUILDFLAG_INTERNAL_IS_MAC() (0)
#define BUILDFLAG_INTERNAL_IS_FUCHSIA() (0)
#define BUILDFLAG_INTERNAL_IS_POSIX() (1)
#else
#error Please add your OS to build/build_config.h
#endif

// ---------------------------------------------------------------------------
// Compiler identifiers
// ---------------------------------------------------------------------------

// COMPILER_GCC is defined if the compiler is GCC, Clang, or a compatible
// compiler (i.e. not MSVC).
#if defined(__clang__)
#define COMPILER_CLANG 1
#define COMPILER_GCC 1  // Clang is GCC-compatible.
#define COMPILER_MSVC 0
#elif defined(__GNUC__)
#define COMPILER_GCC 1
#define COMPILER_MSVC 0
#elif defined(_MSC_VER)
#define COMPILER_MSVC 1
#define COMPILER_GCC 0
#else
#error Please add your compiler to build/build_config.h
#endif

// ---------------------------------------------------------------------------
// Processor architecture identifiers
// ---------------------------------------------------------------------------

#if defined(_M_ARM64) || defined(__aarch64__)
#define ARCH_CPU_ARM64 1
#define ARCH_CPU_ARM_FAMILY 1
#define ARCH_CPU_64_BITS 1
#define ARCH_CPU_LITTLE_ENDIAN 1
#define ARCH_CPU_ARMEL 0
#define ARCH_CPU_X86_FAMILY 0
#define ARCH_CPU_X86_64 0
#define ARCH_CPU_32_BITS 0
#elif defined(_M_ARM) || defined(__arm__)
#define ARCH_CPU_ARMEL 1
#define ARCH_CPU_ARM_FAMILY 1
#define ARCH_CPU_32_BITS 1
#define ARCH_CPU_LITTLE_ENDIAN 1
#define ARCH_CPU_ARM64 0
#define ARCH_CPU_X86_FAMILY 0
#define ARCH_CPU_X86_64 0
#define ARCH_CPU_64_BITS 0
#elif defined(_M_X64) || defined(__x86_64__)
#define ARCH_CPU_X86_FAMILY 1
#define ARCH_CPU_X86_64 1
#define ARCH_CPU_64_BITS 1
#define ARCH_CPU_LITTLE_ENDIAN 1
#define ARCH_CPU_ARM64 0
#define ARCH_CPU_ARMEL 0
#define ARCH_CPU_32_BITS 0
#elif defined(_M_IX86) || defined(__i386__)
#define ARCH_CPU_X86_FAMILY 1
#define ARCH_CPU_X86 1
#define ARCH_CPU_32_BITS 1
#define ARCH_CPU_LITTLE_ENDIAN 1
#define ARCH_CPU_ARM64 0
#define ARCH_CPU_ARMEL 0
#define ARCH_CPU_X86_64 0
#define ARCH_CPU_64_BITS 0
#else
#error Please add your architecture to build/build_config.h
#endif

// Type detection for wchar_t.
#if defined(OS_WIN)
#define WCHAR_T_IS_16_BIT
#elif defined(OS_FUCHSIA)
#define WCHAR_T_IS_32_BIT
#elif defined(OS_POSIX) && defined(COMPILER_GCC) && defined(__WCHAR_MAX__) && \
    (__WCHAR_MAX__ == 0x7fffffff || __WCHAR_MAX__ == 0xffffffff)
#define WCHAR_T_IS_32_BIT
#elif defined(OS_POSIX) && defined(COMPILER_GCC) && defined(__WCHAR_MAX__) && \
    (__WCHAR_MAX__ == 0x7fff || __WCHAR_MAX__ == 0xffff)
#define WCHAR_T_IS_16_BIT
#else
#error Please add support for your compiler in build/build_config.h
#endif

#endif  // BUILD_BUILD_CONFIG_H_
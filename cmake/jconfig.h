/* jconfig.h for PDFium CMake build (libjpeg-turbo without SIMD) */
#define JPEG_LIB_VERSION 80
#define LIBJPEG_TURBO_VERSION 2.1.5
#define LIBJPEG_TURBO_VERSION_NUMBER 2001005
#define C_ARITH_CODING_SUPPORTED 1
#define D_ARITH_CODING_SUPPORTED 1
#define MEM_SRCDST_SUPPORTED 1
/* No SIMD support in CMake build */
/* #undef WITH_SIMD */
#ifndef BITS_IN_JSAMPLE
#define BITS_IN_JSAMPLE 8
#endif

#ifdef _WIN32
#undef RIGHT_SHIFT_IS_UNSIGNED
#ifndef __RPCNDR_H__
typedef unsigned char boolean;
#endif
#define HAVE_BOOLEAN
#if !(defined(_BASETSD_H_) || defined(_BASETSD_H))
typedef short INT16;
typedef signed int INT32;
#endif
#define XMD_H
#else
/* #undef RIGHT_SHIFT_IS_UNSIGNED */
#endif

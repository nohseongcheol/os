/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_LIMITS_H
#define _LIBC_LIMITS_H
/* This package's compiler ABI is i386 ILP32 with signed plain char. */
#define bits_per_byte 8
#define signed_char_minimum (-128)
#define signed_char_maximum 127
#define unsigned_char_maximum 255
#define char_minimum signed_char_minimum
#define char_maximum signed_char_maximum
#define short_integer_minimum (-32767-1)
#define short_integer_maximum 32767
#define unsigned_short_maximum 65535
#define integer_minimum (-2147483647-1)
#define integer_maximum 2147483647
#define unsigned_integer_maximum 4294967295U
#define long_integer_minimum (-2147483647L-1L)
#define long_integer_maximum 2147483647L
#define unsigned_long_maximum 4294967295UL
#define long_long_integer_minimum (-9223372036854775807LL-1LL)
#define long_long_integer_maximum 9223372036854775807LL
#define unsigned_long_long_maximum 18446744073709551615ULL
#endif

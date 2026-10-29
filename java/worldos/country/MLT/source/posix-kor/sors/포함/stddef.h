#ifndef JKOROS_STDDEF_H
#define JKOROS_STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
#define NULL ((void *)0)
#define offsetof(tip_ta_data, membru) __builtin_offsetof(tip_ta_data, membru)
#endif

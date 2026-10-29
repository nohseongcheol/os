#ifndef JKOROS_STDDEF_H
#define JKOROS_STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
#define NULL ((void *)0)
#define offsetof(duomenų_tipas, narys) __builtin_offsetof(duomenų_tipas, narys)
#endif

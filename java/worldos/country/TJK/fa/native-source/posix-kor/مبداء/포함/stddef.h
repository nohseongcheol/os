#ifndef JKOROS_STDDEF_H
#define JKOROS_STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
#define NULL ((void *)0)
#define offsetof(نوع_داده_ها, عضو) __builtin_offsetof(نوع_داده_ها, عضو)
#endif

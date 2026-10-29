#ifndef JKOROS_STDDEF_H
#define JKOROS_STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
#define NULL ((void *)0)
#define offsetof(tipus_de_dades, membre) __builtin_offsetof(tipus_de_dades, membre)
#endif

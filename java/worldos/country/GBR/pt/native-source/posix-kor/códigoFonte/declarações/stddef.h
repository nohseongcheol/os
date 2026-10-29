#ifndef JKOROS_STDDEF_H
#define JKOROS_STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
#define NULL ((void *)0)
#define offsetof(tipo_de_dados, membro) __builtin_offsetof(tipo_de_dados, membro)
#endif

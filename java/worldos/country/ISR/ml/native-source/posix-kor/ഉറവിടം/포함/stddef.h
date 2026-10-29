#ifndef JKOROS_STDDEF_H
#define JKOROS_STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
#define NULL ((void *)0)
#define offsetof(ഡാറ്റാ_തരം, അംഗം) __builtin_offsetof(ഡാറ്റാ_തരം, അംഗം)
#endif

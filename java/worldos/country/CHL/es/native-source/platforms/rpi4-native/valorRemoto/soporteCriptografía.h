#ifndef encabezadoCriptografíaNativo
#define encabezadoCriptografíaNativo
#include <stddef.h>
#include <stdint.h>
void *asignarMemoriaRemoto(size_t);
void liberarRemoto(void *);
void *reasignarRemoto(void *, size_t);
int aleatorioRemoto(unsigned char *, unsigned);
void resumenRemoto(const void *, size_t, unsigned char [32]);
#endif

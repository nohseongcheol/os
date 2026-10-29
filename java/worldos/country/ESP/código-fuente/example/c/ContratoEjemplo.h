#ifndef EncabezadoEjemploNativo
#define EncabezadoEjemploNativo
#include <ABIArchivo.h>
#include <ABIPantalla.h>
static int longitudTexto(const char *texto) { int longitud=0;while(texto[longitud])longitud++;return longitud; }
static int Salida(const char *texto) { int longitud=longitudTexto(texto);return escribirDatosArchivo(1,texto,longitud)==longitud?0:1; }
#endif

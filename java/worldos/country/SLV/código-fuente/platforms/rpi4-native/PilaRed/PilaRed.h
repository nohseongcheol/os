#ifndef encabezadoRedNativo
#define encabezadoRedNativo
#include <stdint.h>
#include <stddef.h>
void prepararRed(void);
void inspeccionarRed(void);
int crearExtremoConectorRed(int categoríaTipo);
int asociarRedCorta(int manejadorArchivo, uint32_t dirección, unsigned númeroPuerto);
int escucharRedCorta(int manejadorArchivo);
void direcciónConectorRedReutilizar(int manejadorArchivo);
int conectarRedCorta(int manejadorArchivo, uint32_t dirección, unsigned númeroPuerto);
int aceptarRedCorta(int manejadorArchivo);
int leerRedCorta(int manejadorArchivo, void *Datos, unsigned númeroElementosElementoLista);
int escribirRedCorta(int manejadorArchivo, const void *Datos, unsigned númeroElementosElementoLista);
int enviarDatagrama(int manejadorArchivo, const void *Datos, unsigned númeroElementosElementoLista, uint32_t dirección, unsigned númeroPuerto);
int recibirDatagrama(int manejadorArchivo, void *Datos, unsigned númeroElementosElementoLista);
unsigned númeroPuertoRed(int manejadorArchivo);
unsigned númeroPuertoParRed(int manejadorArchivo);
uint32_t direcciónParRedRedCorta(int manejadorArchivo);
void cerrarRed(int manejadorArchivo);
int controlTransferenciaArchivo(int acción);
void inspeccionarTransferenciaArchivo(void);
uint32_t leerEstadoRed(unsigned valorEntradaElemento, unsigned número);
int configurarRed(unsigned acción, uint32_t dirección, uint32_t valorMáscara, uint32_t valorPasarela);
int iniciarPruebaRespuestaRetorno(uint32_t dirección, unsigned valorOrden);
int leerPruebaRespuestaRetorno(unsigned valorEntradaElemento);
#endif

#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t tipoResultadoEntradaSalida;
typedef size_t tipoNúmeroElementosByte;
typedef int64_t tipoDesfaseArchivo;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
tipoResultadoEntradaSalida pk_read(int fd, void *buffer, size_t count);
tipoResultadoEntradaSalida pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
tipoDesfaseArchivo pk_lseek(int fd, tipoDesfaseArchivo offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, tipoDesfaseArchivo size);
int pk_fsync(int fd);
int pk_size(int fd);
int abrirArchivo(const char *ruta, int modoMétodo, ...);
tipoResultadoEntradaSalida leerDatosArchivo(int Archivo, void *Datos, size_t númeroElementosElementoLista);
tipoResultadoEntradaSalida escribirDatosArchivo(int Archivo, const void *Datos, size_t númeroElementosElementoLista);
int cerrarArchivo(int Archivo);
tipoDesfaseArchivo posicionarArchivo(int Archivo, tipoDesfaseArchivo valorDistancia, int raízProyecto);
int eliminarNombreEntradaElementoArchivo(const char *ruta);
int establecerLongitudArchivo(int Archivo, tipoDesfaseArchivo tamaño);
int almacenamientoArchivoConfirmar(int Archivo);
int tamañoArchivo(int Archivo);
#ifdef __cplusplus
}
#endif
#define númeroError (*pk_errno_location())
#define leerValorSolamente 0
#define escribirValorSolamente 1
#define EscribirLeer 2
#define AusenteSiCrear 0x40
#define crearArchivoNuevo 0xc0
#define ContenidoTruncar 0x200
#define añadirFinalFinEnPosición 0x400
#define PrincipioDesde 0
#define raízActual 1
#define origenFin 2
#endif

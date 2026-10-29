#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define abrirArchivo open
#define crearArchivo creat
#define leerDatosArchivo read
#define escribirDatosArchivo write
#define cerrarArchivo close
#define posicionarArchivo lseek
#define descriptorArchivoDuplicado dup
#define enPosiciónDescriptorArchivoDuplicado dup2
#define eliminarNombreEntradaElementoArchivo unlink
#define establecerLongitudArchivo ftruncate
#define almacenamientoArchivoConfirmar fsync
#define leerEstadoArchivo fstat
#define descriptorArchivoControl fcntl
#define leerValorSolamente O_RDONLY
#define escribirValorSolamente O_WRONLY
#define EscribirLeer O_RDWR
#define AusenteSiCrear O_CREAT
#define crearArchivoNuevo (O_CREAT | O_EXCL)
#define ContenidoTruncar O_TRUNC
#define añadirFinalFinEnPosición O_APPEND
#define esperarNoOperadorHacer O_NONBLOCK
#define PrincipioDesde SEEK_SET
#define raízActual SEEK_CUR
#define origenFin SEEK_END
#define estadoArchivo stat
typedef size_t tipoNúmeroElementosByte;
typedef ssize_t tipoResultadoEntradaSalida;
typedef off_t tipoDesfaseArchivo;
#endif

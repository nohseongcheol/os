// 동일 español 헤더를 사용하는 별도 EL0 biblioteca. valorNúcleo 직접 호출판과 혼합 valorVedado.
#include "ABIArchivo.h"
#include "invocar.h"
#include "ABIRed.h"
static int códigoError;
int *pk_errno_location(void) { return &códigoError; }
static intptr_t comprobado(intptr_t resultado) { if (resultado < 0) { códigoError = -resultado; return -1; } return resultado; }
int pk_open(const char *path, int flags, ...) { return comprobado(invocarUsuario(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
tipoResultadoEntradaSalida pk_read(int fd, void *p, size_t n) { return comprobado(invocarUsuario(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
tipoResultadoEntradaSalida pk_write(int fd, const void *p, size_t n) { return comprobado(invocarUsuario(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return comprobado(invocarUsuario(4, fd, 0, 0, 0, 0, 0)); }
tipoDesfaseArchivo pk_lseek(int fd, tipoDesfaseArchivo offset, int origin) { return comprobado(invocarUsuario(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return comprobado(invocarUsuario(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, tipoDesfaseArchivo size) { return comprobado(invocarUsuario(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return comprobado(invocarUsuario(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return comprobado(invocarUsuario(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return comprobado(invocarUsuario(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return comprobado(invocarUsuario(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return comprobado(invocarUsuario(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return comprobado(invocarUsuario(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return comprobado(invocarUsuario(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return comprobado(invocarUsuario(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return comprobado(invocarUsuario(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return comprobado(invocarUsuario(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* español 공개 함수의 datosEfectivo EL0 implementación. 구조체는 SVC에서 copiarValor·검증한다. */
int crearExtremo(int familiaDirección,int modoComunicación,int protocoloTransferencia) {
    return comprobado(invocarUsuario(32,familiaDirección,modoComunicación,protocoloTransferencia,0,0,0));
}
int asociarDirección(int extremo,const struct DirecciónConectorRed *dirección,tipoLongitudDirecciónConectorRed longitud) {
    return comprobado(invocarUsuario(33,extremo,(uintptr_t)dirección,longitud,0,0,0));
}
intptr_t enviarDatosDatagrama(int extremo,const void *Datos,size_t númeroElementosElementoLista,int valorSelección,const struct DirecciónConectorRed *dirección,tipoLongitudDirecciónConectorRed longitud) {
    return comprobado(invocarUsuario(34,extremo,(uintptr_t)Datos,númeroElementosElementoLista,valorSelección,(uintptr_t)dirección,longitud));
}
intptr_t recibirDatosDatagrama(int extremo,void *Datos,size_t númeroElementosElementoLista,int valorSelección,struct DirecciónConectorRed *dirección,tipoLongitudDirecciónConectorRed *longitud) {
    return comprobado(invocarUsuario(35,extremo,(uintptr_t)Datos,númeroElementosElementoLista,valorSelección,(uintptr_t)dirección,(uintptr_t)longitud));
}
int leerDirecciónConectorRed(int extremo,struct DirecciónConectorRed *dirección,tipoLongitudDirecciónConectorRed *longitud) {
    return comprobado(invocarUsuario(36,extremo,(uintptr_t)dirección,(uintptr_t)longitud,0,0,0));
}
int conectarRed(int extremo,const struct DirecciónConectorRed *dirección,tipoLongitudDirecciónConectorRed longitud) {
    return comprobado(invocarUsuario(37,extremo,(uintptr_t)dirección,longitud,0,0,0));
}
int esperarConexiónRedPara(int extremo,int númeroElementosEsperaEnCurso) {
    return comprobado(invocarUsuario(38,extremo,númeroElementosEsperaEnCurso,0,0,0,0));
}
int aceptarConexiónRed(int extremo,struct DirecciónConectorRed *dirección,tipoLongitudDirecciónConectorRed *longitud) {
    return comprobado(invocarUsuario(39,extremo,(uintptr_t)dirección,(uintptr_t)longitud,0,0,0));
}

/* Archivo 함수도 독립된 español Función 심볼로 제공한다. */
int abrirArchivo(const char *ruta,int modoMétodo,...) { return comprobado(invocarUsuario(3,(uintptr_t)ruta,modoMétodo,0,0,0,0)); }
tipoResultadoEntradaSalida leerDatosArchivo(int Archivo,void *Datos,size_t númeroElementosElementoLista) { return comprobado(invocarUsuario(2,Archivo,(uintptr_t)Datos,númeroElementosElementoLista,0,0,0)); }
tipoResultadoEntradaSalida escribirDatosArchivo(int Archivo,const void *Datos,size_t númeroElementosElementoLista) { return comprobado(invocarUsuario(1,Archivo,(uintptr_t)Datos,númeroElementosElementoLista,0,0,0)); }
int cerrarArchivo(int Archivo) { return comprobado(invocarUsuario(4,Archivo,0,0,0,0,0)); }
tipoDesfaseArchivo posicionarArchivo(int Archivo,tipoDesfaseArchivo valorDistancia,int raízProyecto) { return comprobado(invocarUsuario(5,Archivo,valorDistancia,raízProyecto,0,0,0)); }
int eliminarNombreEntradaElementoArchivo(const char *ruta) { return comprobado(invocarUsuario(11,(uintptr_t)ruta,0,0,0,0,0)); }
int establecerLongitudArchivo(int Archivo,tipoDesfaseArchivo tamaño) { return comprobado(invocarUsuario(10,Archivo,tamaño,0,0,0,0)); }
int almacenamientoArchivoConfirmar(int Archivo) { return comprobado(invocarUsuario(12,Archivo,0,0,0,0,0)); }
int tamañoArchivo(int Archivo) { return comprobado(invocarUsuario(9,Archivo,0,0,0,0,0)); }

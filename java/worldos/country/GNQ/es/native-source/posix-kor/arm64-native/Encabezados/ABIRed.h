#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "ABIArchivo.h"
/* 표준 ABI는 기존 archivoCódigoEjecutable·valorExterno 코드와 연결할 때만 사용한다. */
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
#define IPPROTO_TCP 6
#define INADDR_LOOPBACK 0x7f000001u
typedef uint32_t pk_socklen_t;
struct pk_sockaddr { uint16_t sa_family; unsigned char sa_data[14]; };
struct pk_in_addr { uint32_t s_addr; };
struct pk_sockaddr_in { uint16_t sin_family, sin_port; struct pk_in_addr sin_addr; unsigned char sin_zero[8]; };

/* español 자료형은 valorMacro 별칭이 아닌 독립된 구조체다.
 * dirección(住所)는 도착할 곳, 갈래는 dirección valorSistemaOperación, datagrama(電文)은 valorFrontera 있는 Comunicación 자료다. */
enum constanteRed {
    FamiliaInternet = 2, RedFlujo = 1, ConectorRedDatagrama = 2,
    protocoloTransporteFlujo = 6, ProtocoloDatagrama = 17,
    direcciónBucleRetorno = 0x7f000001u, direccionesConexiónTodos = 0, ErrorOtraVezIntentar = 11
};
typedef uint32_t tipoLongitudDirecciónConectorRed;
struct DirecciónConectorRed { uint16_t familiaDirección; unsigned char datosDirección[14]; };
struct valorDirecciónInternet { uint32_t valorDirección; };
struct DirecciónConectorRedInternet {
    uint16_t familiaDirección;
    uint16_t númeroPuerto;
    struct valorDirecciónInternet DirecciónInternet;
    unsigned char valorMargen[8];
};
typedef struct DirecciónConectorRed tipoDirecciónConectorRed;
typedef struct DirecciónConectorRedInternet tipoDirecciónConectorRedInternet;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char comprobarTamañoDirecciónConectorRedInternet[(sizeof(struct DirecciónConectorRedInternet)==16)?1:-1];
typedef char comprobarDisposiciónDirecciónConectorRedInternet[(offsetof(struct DirecciónConectorRedInternet,DirecciónInternet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int crearExtremo(int familiaDirección, int modoComunicación, int protocoloTransferencia);
int asociarDirección(int extremo, const struct DirecciónConectorRed *dirección, tipoLongitudDirecciónConectorRed longitud);
intptr_t enviarDatosDatagrama(int extremo, const void *Datos, size_t númeroElementosElementoLista, int valorSelección, const struct DirecciónConectorRed *dirección, tipoLongitudDirecciónConectorRed longitud);
intptr_t recibirDatosDatagrama(int extremo, void *Datos, size_t númeroElementosElementoLista, int valorSelección, struct DirecciónConectorRed *dirección, tipoLongitudDirecciónConectorRed *longitud);
int leerDirecciónConectorRed(int extremo, struct DirecciónConectorRed *dirección, tipoLongitudDirecciónConectorRed *longitud);
int conectarRed(int extremo, const struct DirecciónConectorRed *dirección, tipoLongitudDirecciónConectorRed longitud);
int esperarConexiónRedPara(int extremo, int númeroElementosEsperaEnCurso);
int aceptarConexiónRed(int extremo, struct DirecciónConectorRed *dirección, tipoLongitudDirecciónConectorRed *longitud);

int pk_connect(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
int pk_listen(int fd, int backlog);
int pk_accept(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_socket(int domain, int type, int protocol);
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
#ifdef __cplusplus
}
#endif
static inline uint16_t cortoRed(uint16_t valor) { return (uint16_t)((valor >> 8) | (valor << 8)); }
static inline uint32_t enteroValorRed(uint32_t valor) { return ((valor & 255u) << 24) | ((valor & 0xff00u) << 8) | ((valor >> 8) & 0xff00u) | (valor >> 24); }
static inline uint16_t cortoOrdenDispositivo(uint16_t valor) { return cortoRed(valor); }
static inline uint32_t enteroValorOrdenDispositivo(uint32_t valor) { return enteroValorRed(valor); }
static inline uint16_t pk_htons(uint16_t x) { return cortoRed(x); }
static inline uint32_t pk_htonl(uint32_t x) { return enteroValorRed(x); }
#endif

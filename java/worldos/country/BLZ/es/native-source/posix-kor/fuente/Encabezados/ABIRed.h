#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define crearExtremo socket
#define asociarDirección bind
#define enviarDatosDatagrama sendto
#define recibirDatosDatagrama recvfrom
#define leerDirecciónConectorRed getsockname
#define cambiarAjustesRed setsockopt
#define analizarDirecciónRed inet_pton
#define direcciónRedFormato inet_ntop
#define cortoRed htons
#define enteroValorRed htonl
#define cortoOrdenDispositivo ntohs
#define enteroValorOrdenDispositivo ntohl
#endif

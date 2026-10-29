#include <ABIArchivo.h>
#include <ABIRed.h>
#include <string.h>
#include <stdio.h>

#define verificar(condición) do { if (!(condición)) { puts("POSIX UDP CHECK FAILED: " #condición); return 1; } } while (0)
int main(int númeroElementosArgumentos, char **listaArgumento) {
    verificar(númeroElementosArgumentos == 2);
    int númeroPuerto = 0;
    for (int entradaElementoRanura = 0; listaArgumento[1][entradaElementoRanura]; entradaElementoRanura++) {
        verificar(listaArgumento[1][entradaElementoRanura] >= '0' && listaArgumento[1][entradaElementoRanura] <= '9');
        númeroPuerto = númeroPuerto * 10 + listaArgumento[1][entradaElementoRanura] - '0';
        verificar(númeroPuerto <= 65535);
    }
    int valorExtremo = crearExtremo(AF_INET, SOCK_DGRAM, 0);
    verificar(valorExtremo == 3);
    struct sockaddr_in ámbitoLocal = {0}, valorParRed = {0}, direcciónRecibido = {0};
    ámbitoLocal.sin_family = AF_INET;
    socklen_t longitud = sizeof ámbitoLocal;
    verificar(leerDirecciónConectorRed(valorExtremo, (struct sockaddr *)&ámbitoLocal, &longitud) == 0 && ámbitoLocal.sin_port == 0);
    verificar(asociarDirección(valorExtremo, (struct sockaddr *)&ámbitoLocal, sizeof ámbitoLocal) == 0);
    verificar(leerDirecciónConectorRed(valorExtremo, (struct sockaddr *)&ámbitoLocal, &longitud) == 0 && ntohs(ámbitoLocal.sin_port) >= 49152);
    verificar(asociarDirección(valorExtremo, (struct sockaddr *)&ámbitoLocal, sizeof ámbitoLocal) == -1 && errno == EINVAL);
    int ordinalSegundo = socket(AF_INET, SOCK_DGRAM, 0);
    verificar(bind(ordinalSegundo, (struct sockaddr *)&ámbitoLocal, sizeof ámbitoLocal) == -1 && errno == EADDRINUSE);
    verificar(close(ordinalSegundo) == 0);
    ordinalSegundo = dup(valorExtremo);
    verificar(close(valorExtremo) == 0); valorExtremo = ordinalSegundo;
    valorParRed.sin_family = AF_INET; valorParRed.sin_port = cortoRed(númeroPuerto);
    verificar(analizarDirecciónRed(AF_INET, "10.0.2.2", &valorParRed.sin_addr) == 1);
    struct timeval esperarValor = {0, 200000};
    verificar(cambiarAjustesRed(valorExtremo, SOL_SOCKET, SO_RCVTIMEO, &esperarValor, sizeof esperarValor) == 0);
    char Datos[32];
    verificar(recibirDatosDatagrama(valorExtremo, Datos, sizeof Datos, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(enviarDatosDatagrama(valorExtremo, "posix-udp", 9, 0, (struct sockaddr *)&valorParRed, sizeof valorParRed) == 9);
    longitud = sizeof direcciónRecibido;
    verificar(recvfrom(valorExtremo, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verificar(recibirDatosDatagrama(valorExtremo, Datos, sizeof Datos, 0, (struct sockaddr *)&direcciónRecibido, &longitud) == 9);
    verificar(memcmp(Datos, "posix-udp", 9) == 0 && longitud == 16);
    verificar(direcciónRecibido.sin_port == valorParRed.sin_port && direcciónRecibido.sin_addr.s_addr == valorParRed.sin_addr.s_addr);
    verificar(sendto(valorExtremo, "truncate", 8, 0, (struct sockaddr *)&valorParRed, sizeof valorParRed) == 8);
    verificar(recvfrom(valorExtremo, Datos, 3, 0, NULL, NULL) == 3 && memcmp(Datos, "tru", 3) == 0);
    verificar(recvfrom(valorExtremo, Datos, sizeof Datos, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(sendto(valorExtremo, NULL, 0, 0, (struct sockaddr *)&valorParRed, sizeof valorParRed) == 0);
    verificar(recvfrom(valorExtremo, NULL, 0, 0, NULL, NULL) == 0);
    verificar(recvfrom(valorExtremo, Datos, sizeof Datos, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(close(valorExtremo) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verificar(condición) do { if (!(condición)) { puts("POSIX UDP CHECK FAILED: " #condición); return 1; } } while (0)
int main(int 인수개수, char **argumento_Lista) {
    verificar(인수개수 == 2);
    int número_do_porto = 0;
    for (int 칸 = 0; argumento_Lista[1][칸]; 칸++) {
        verificar(argumento_Lista[1][칸] >= '0' && argumento_Lista[1][칸] <= '9');
        número_do_porto = número_do_porto * 10 + argumento_Lista[1][칸] - '0';
        verificar(número_do_porto <= 65535);
    }
    int extremo_VALOR = crear_extremo(AF_INET, SOCK_DGRAM, 0);
    verificar(extremo_VALOR == 3);
    struct sockaddr_in local_Ámbito = {0}, punto_VALOR = {0}, RECIBIDO_ENDEREZO = {0};
    local_Ámbito.sin_family = AF_INET;
    socklen_t duración_VALOR = sizeof local_Ámbito;
    verificar(통신주소읽기(extremo_VALOR, (struct sockaddr *)&local_Ámbito, &duración_VALOR) == 0 && local_Ámbito.sin_port == 0);
    verificar(ligar_ENDEREZO(extremo_VALOR, (struct sockaddr *)&local_Ámbito, sizeof local_Ámbito) == 0);
    verificar(통신주소읽기(extremo_VALOR, (struct sockaddr *)&local_Ámbito, &duración_VALOR) == 0 && ntohs(local_Ámbito.sin_port) >= 49152);
    verificar(ligar_ENDEREZO(extremo_VALOR, (struct sockaddr *)&local_Ámbito, sizeof local_Ámbito) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verificar(bind(둘째, (struct sockaddr *)&local_Ámbito, sizeof local_Ámbito) == -1 && errno == EADDRINUSE);
    verificar(close(둘째) == 0);
    둘째 = dup(extremo_VALOR);
    verificar(close(extremo_VALOR) == 0); extremo_VALOR = 둘째;
    punto_VALOR.sin_family = AF_INET; punto_VALOR.sin_port = 망차례짧은수(número_do_porto);
    verificar(analizar_Rede_ENDEREZO(AF_INET, "10.0.2.2", &punto_VALOR.sin_addr) == 1);
    struct timeval agarda_VALOR = {0, 200000};
    verificar(modificar_Rede_Configuración(extremo_VALOR, SOL_SOCKET, SO_RCVTIMEO, &agarda_VALOR, sizeof agarda_VALOR) == 0);
    char datos[32];
    verificar(자료전문받기(extremo_VALOR, datos, sizeof datos, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(자료전문보내기(extremo_VALOR, "posix-udp", 9, 0, (struct sockaddr *)&punto_VALOR, sizeof punto_VALOR) == 9);
    duración_VALOR = sizeof RECIBIDO_ENDEREZO;
    verificar(recvfrom(extremo_VALOR, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verificar(자료전문받기(extremo_VALOR, datos, sizeof datos, 0, (struct sockaddr *)&RECIBIDO_ENDEREZO, &duración_VALOR) == 9);
    verificar(memcmp(datos, "posix-udp", 9) == 0 && duración_VALOR == 16);
    verificar(RECIBIDO_ENDEREZO.sin_port == punto_VALOR.sin_port && RECIBIDO_ENDEREZO.sin_addr.s_addr == punto_VALOR.sin_addr.s_addr);
    verificar(sendto(extremo_VALOR, "truncate", 8, 0, (struct sockaddr *)&punto_VALOR, sizeof punto_VALOR) == 8);
    verificar(recvfrom(extremo_VALOR, datos, 3, 0, NULL, NULL) == 3 && memcmp(datos, "tru", 3) == 0);
    verificar(recvfrom(extremo_VALOR, datos, sizeof datos, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(sendto(extremo_VALOR, NULL, 0, 0, (struct sockaddr *)&punto_VALOR, sizeof punto_VALOR) == 0);
    verificar(recvfrom(extremo_VALOR, NULL, 0, 0, NULL, NULL) == 0);
    verificar(recvfrom(extremo_VALOR, datos, sizeof datos, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(close(extremo_VALOR) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

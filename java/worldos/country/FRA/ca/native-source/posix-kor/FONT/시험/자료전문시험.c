#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verificar(condició) do { if (!(condició)) { puts("POSIX UDP CHECK FAILED: " #condició); return 1; } } while (0)
int main(int 인수개수, char **arg_Llista) {
    verificar(인수개수 == 2);
    int número_de_port = 0;
    for (int 칸 = 0; arg_Llista[1][칸]; 칸++) {
        verificar(arg_Llista[1][칸] >= '0' && arg_Llista[1][칸] <= '9');
        número_de_port = número_de_port * 10 + arg_Llista[1][칸] - '0';
        verificar(número_de_port <= 65535);
    }
    int extrem_VALOR = Crear_extrem(AF_INET, SOCK_DGRAM, 0);
    verificar(extrem_VALOR == 3);
    struct sockaddr_in local_Àmbit = {0}, homòleg_VALOR = {0}, CANTIDAD_RECIBIDA_ADREÇA = {0};
    local_Àmbit.sin_family = AF_INET;
    socklen_t durada_VALOR = sizeof local_Àmbit;
    verificar(통신주소읽기(extrem_VALOR, (struct sockaddr *)&local_Àmbit, &durada_VALOR) == 0 && local_Àmbit.sin_port == 0);
    verificar(enllaçar_ADREÇA(extrem_VALOR, (struct sockaddr *)&local_Àmbit, sizeof local_Àmbit) == 0);
    verificar(통신주소읽기(extrem_VALOR, (struct sockaddr *)&local_Àmbit, &durada_VALOR) == 0 && ntohs(local_Àmbit.sin_port) >= 49152);
    verificar(enllaçar_ADREÇA(extrem_VALOR, (struct sockaddr *)&local_Àmbit, sizeof local_Àmbit) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verificar(bind(둘째, (struct sockaddr *)&local_Àmbit, sizeof local_Àmbit) == -1 && errno == EADDRINUSE);
    verificar(close(둘째) == 0);
    둘째 = dup(extrem_VALOR);
    verificar(close(extrem_VALOR) == 0); extrem_VALOR = 둘째;
    homòleg_VALOR.sin_family = AF_INET; homòleg_VALOR.sin_port = 망차례짧은수(número_de_port);
    verificar(analitzar_xarxa_ADREÇA(AF_INET, "10.0.2.2", &homòleg_VALOR.sin_addr) == 1);
    struct timeval Espera_VALOR = {0, 200000};
    verificar(canviar_xarxa_Configuració(extrem_VALOR, SOL_SOCKET, SO_RCVTIMEO, &Espera_VALOR, sizeof Espera_VALOR) == 0);
    char dades[32];
    verificar(자료전문받기(extrem_VALOR, dades, sizeof dades, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(자료전문보내기(extrem_VALOR, "posix-udp", 9, 0, (struct sockaddr *)&homòleg_VALOR, sizeof homòleg_VALOR) == 9);
    durada_VALOR = sizeof CANTIDAD_RECIBIDA_ADREÇA;
    verificar(recvfrom(extrem_VALOR, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verificar(자료전문받기(extrem_VALOR, dades, sizeof dades, 0, (struct sockaddr *)&CANTIDAD_RECIBIDA_ADREÇA, &durada_VALOR) == 9);
    verificar(memcmp(dades, "posix-udp", 9) == 0 && durada_VALOR == 16);
    verificar(CANTIDAD_RECIBIDA_ADREÇA.sin_port == homòleg_VALOR.sin_port && CANTIDAD_RECIBIDA_ADREÇA.sin_addr.s_addr == homòleg_VALOR.sin_addr.s_addr);
    verificar(sendto(extrem_VALOR, "truncate", 8, 0, (struct sockaddr *)&homòleg_VALOR, sizeof homòleg_VALOR) == 8);
    verificar(recvfrom(extrem_VALOR, dades, 3, 0, NULL, NULL) == 3 && memcmp(dades, "tru", 3) == 0);
    verificar(recvfrom(extrem_VALOR, dades, sizeof dades, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(sendto(extrem_VALOR, NULL, 0, 0, (struct sockaddr *)&homòleg_VALOR, sizeof homòleg_VALOR) == 0);
    verificar(recvfrom(extrem_VALOR, NULL, 0, 0, NULL, NULL) == 0);
    verificar(recvfrom(extrem_VALOR, dades, sizeof dades, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verificar(close(extrem_VALOR) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

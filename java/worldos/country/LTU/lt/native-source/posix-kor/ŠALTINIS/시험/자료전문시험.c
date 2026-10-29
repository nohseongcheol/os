#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define patvirtinti(sąlyga) do { if (!(sąlyga)) { puts("POSIX UDP CHECK FAILED: " #sąlyga); return 1; } } while (0)
int main(int 인수개수, char **argumentas_Sąrašas) {
    patvirtinti(인수개수 == 2);
    int prievado_numeris = 0;
    for (int 칸 = 0; argumentas_Sąrašas[1][칸]; 칸++) {
        patvirtinti(argumentas_Sąrašas[1][칸] >= '0' && argumentas_Sąrašas[1][칸] <= '9');
        prievado_numeris = prievado_numeris * 10 + argumentas_Sąrašas[1][칸] - '0';
        patvirtinti(prievado_numeris <= 65535);
    }
    int dalyvis_VALUE = kurti_dalyvis(AF_INET, SOCK_DGRAM, 0);
    patvirtinti(dalyvis_VALUE == 3);
    struct sockaddr_in vietinis_Aprėptis = {0}, lygiavertis_mazgas_VALUE = {0}, RECEIVED_ADDRESS = {0};
    vietinis_Aprėptis.sin_family = AF_INET;
    socklen_t 길이 = sizeof vietinis_Aprėptis;
    patvirtinti(통신주소읽기(dalyvis_VALUE, (struct sockaddr *)&vietinis_Aprėptis, &길이) == 0 && vietinis_Aprėptis.sin_port == 0);
    patvirtinti(BIND_ADDRESS(dalyvis_VALUE, (struct sockaddr *)&vietinis_Aprėptis, sizeof vietinis_Aprėptis) == 0);
    patvirtinti(통신주소읽기(dalyvis_VALUE, (struct sockaddr *)&vietinis_Aprėptis, &길이) == 0 && ntohs(vietinis_Aprėptis.sin_port) >= 49152);
    patvirtinti(BIND_ADDRESS(dalyvis_VALUE, (struct sockaddr *)&vietinis_Aprėptis, sizeof vietinis_Aprėptis) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    patvirtinti(bind(둘째, (struct sockaddr *)&vietinis_Aprėptis, sizeof vietinis_Aprėptis) == -1 && errno == EADDRINUSE);
    patvirtinti(close(둘째) == 0);
    둘째 = dup(dalyvis_VALUE);
    patvirtinti(close(dalyvis_VALUE) == 0); dalyvis_VALUE = 둘째;
    lygiavertis_mazgas_VALUE.sin_family = AF_INET; lygiavertis_mazgas_VALUE.sin_port = 망차례짧은수(prievado_numeris);
    patvirtinti(analizuoti_sintaksę_tinklo_identifikatorius(AF_INET, "10.0.2.2", &lygiavertis_mazgas_VALUE.sin_addr) == 1);
    struct timeval Palauk_VALUE = {0, 200000};
    patvirtinti(keisti_tinklas_Parametrai(dalyvis_VALUE, SOL_SOCKET, SO_RCVTIMEO, &Palauk_VALUE, sizeof Palauk_VALUE) == 0);
    char duomenys[32];
    patvirtinti(gauti_paketų_kelio_schema_duomenys(dalyvis_VALUE, duomenys, sizeof duomenys, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    patvirtinti(siųsti_paketų_kelio_schema_duomenys(dalyvis_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&lygiavertis_mazgas_VALUE, sizeof lygiavertis_mazgas_VALUE) == 9);
    길이 = sizeof RECEIVED_ADDRESS;
    patvirtinti(recvfrom(dalyvis_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    patvirtinti(gauti_paketų_kelio_schema_duomenys(dalyvis_VALUE, duomenys, sizeof duomenys, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &길이) == 9);
    patvirtinti(memcmp(duomenys, "posix-udp", 9) == 0 && 길이 == 16);
    patvirtinti(RECEIVED_ADDRESS.sin_port == lygiavertis_mazgas_VALUE.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == lygiavertis_mazgas_VALUE.sin_addr.s_addr);
    patvirtinti(sendto(dalyvis_VALUE, "truncate", 8, 0, (struct sockaddr *)&lygiavertis_mazgas_VALUE, sizeof lygiavertis_mazgas_VALUE) == 8);
    patvirtinti(recvfrom(dalyvis_VALUE, duomenys, 3, 0, NULL, NULL) == 3 && memcmp(duomenys, "tru", 3) == 0);
    patvirtinti(recvfrom(dalyvis_VALUE, duomenys, sizeof duomenys, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    patvirtinti(sendto(dalyvis_VALUE, NULL, 0, 0, (struct sockaddr *)&lygiavertis_mazgas_VALUE, sizeof lygiavertis_mazgas_VALUE) == 0);
    patvirtinti(recvfrom(dalyvis_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    patvirtinti(recvfrom(dalyvis_VALUE, duomenys, sizeof duomenys, 0, NULL, NULL) == -1 && errno == EAGAIN);
    patvirtinti(close(dalyvis_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

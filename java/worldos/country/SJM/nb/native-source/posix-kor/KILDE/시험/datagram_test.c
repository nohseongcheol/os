#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define bekrefte(vilkår) do { if (!(vilkår)) { puts("POSIX UDP CHECK FAILED: " #vilkår); return 1; } } while (0)
int main(int 인수개수, char **argument_Liste) {
    bekrefte(인수개수 == 2);
    int portnummer = 0;
    for (int åpning_oppføring = 0; argument_Liste[1][åpning_oppføring]; åpning_oppføring++) {
        bekrefte(argument_Liste[1][åpning_oppføring] >= '0' && argument_Liste[1][åpning_oppføring] <= '9');
        portnummer = portnummer * 10 + argument_Liste[1][åpning_oppføring] - '0';
        bekrefte(portnummer <= 65535);
    }
    int deltaker_VERDI = åpne_deltaker(AF_INET, SOCK_DGRAM, 0);
    bekrefte(deltaker_VERDI == 3);
    struct sockaddr_in lokal_Omfang = {0}, node_VERDI_6a3b6fa7 = {0}, MOTTATT_AVKAST_e_post = {0};
    lokal_Omfang.sin_family = AF_INET;
    socklen_t lengde_VERDI = sizeof lokal_Omfang;
    bekrefte(통신주소읽기(deltaker_VERDI, (struct sockaddr *)&lokal_Omfang, &lengde_VERDI) == 0 && lokal_Omfang.sin_port == 0);
    bekrefte(BIND_e_post(deltaker_VERDI, (struct sockaddr *)&lokal_Omfang, sizeof lokal_Omfang) == 0);
    bekrefte(통신주소읽기(deltaker_VERDI, (struct sockaddr *)&lokal_Omfang, &lengde_VERDI) == 0 && ntohs(lokal_Omfang.sin_port) >= 49152);
    bekrefte(BIND_e_post(deltaker_VERDI, (struct sockaddr *)&lokal_Omfang, sizeof lokal_Omfang) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    bekrefte(bind(둘째, (struct sockaddr *)&lokal_Omfang, sizeof lokal_Omfang) == -1 && errno == EADDRINUSE);
    bekrefte(close(둘째) == 0);
    둘째 = dup(deltaker_VERDI);
    bekrefte(close(deltaker_VERDI) == 0); deltaker_VERDI = 둘째;
    node_VERDI_6a3b6fa7.sin_family = AF_INET; node_VERDI_6a3b6fa7.sin_port = 망차례짧은수(portnummer);
    bekrefte(dele_opp_nettverks_ID(AF_INET, "10.0.2.2", &node_VERDI_6a3b6fa7.sin_addr) == 1);
    struct timeval vent_VERDI = {0, 200000};
    bekrefte(endre_nettverk_Innstillinger(deltaker_VERDI, SOL_SOCKET, SO_RCVTIMEO, &vent_VERDI, sizeof vent_VERDI) == 0);
    char data[32];
    bekrefte(motta_datagram_data(deltaker_VERDI, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    bekrefte(sende_datagram_data(deltaker_VERDI, "posix-udp", 9, 0, (struct sockaddr *)&node_VERDI_6a3b6fa7, sizeof node_VERDI_6a3b6fa7) == 9);
    lengde_VERDI = sizeof MOTTATT_AVKAST_e_post;
    bekrefte(recvfrom(deltaker_VERDI, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    bekrefte(motta_datagram_data(deltaker_VERDI, data, sizeof data, 0, (struct sockaddr *)&MOTTATT_AVKAST_e_post, &lengde_VERDI) == 9);
    bekrefte(memcmp(data, "posix-udp", 9) == 0 && lengde_VERDI == 16);
    bekrefte(MOTTATT_AVKAST_e_post.sin_port == node_VERDI_6a3b6fa7.sin_port && MOTTATT_AVKAST_e_post.sin_addr.s_addr == node_VERDI_6a3b6fa7.sin_addr.s_addr);
    bekrefte(sendto(deltaker_VERDI, "truncate", 8, 0, (struct sockaddr *)&node_VERDI_6a3b6fa7, sizeof node_VERDI_6a3b6fa7) == 8);
    bekrefte(recvfrom(deltaker_VERDI, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    bekrefte(recvfrom(deltaker_VERDI, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    bekrefte(sendto(deltaker_VERDI, NULL, 0, 0, (struct sockaddr *)&node_VERDI_6a3b6fa7, sizeof node_VERDI_6a3b6fa7) == 0);
    bekrefte(recvfrom(deltaker_VERDI, NULL, 0, 0, NULL, NULL) == 0);
    bekrefte(recvfrom(deltaker_VERDI, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    bekrefte(close(deltaker_VERDI) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

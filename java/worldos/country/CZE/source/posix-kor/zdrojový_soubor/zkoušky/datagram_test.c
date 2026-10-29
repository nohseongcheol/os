#include <Soubor_ABI.h>
#include <síť_ABI.h>
#include <string.h>
#include <stdio.h>

#define ověřit(podmínka) do { if (!(podmínka)) { puts("POSIX UDP CHECK FAILED: " #podmínka); return 1; } } while (0)
int main(int 인수개수, char **argument_Seznam) {
    ověřit(인수개수 == 2);
    int číslo_portu = 0;
    for (int přihrádka_položka = 0; argument_Seznam[1][přihrádka_položka]; přihrádka_položka++) {
        ověřit(argument_Seznam[1][přihrádka_položka] >= '0' && argument_Seznam[1][přihrádka_položka] <= '9');
        číslo_portu = číslo_portu * 10 + argument_Seznam[1][přihrádka_položka] - '0';
        ověřit(číslo_portu <= 65535);
    }
    int účastník_HODNOTA = Create_účastník(AF_INET, SOCK_DGRAM, 0);
    ověřit(účastník_HODNOTA == 3);
    struct sockaddr_in místní_obor = {0}, partner_HODNOTA = {0}, RECEIVED_ODKAZ = {0};
    místní_obor.sin_family = AF_INET;
    socklen_t délka_HODNOTA = sizeof místní_obor;
    ověřit(통신주소읽기(účastník_HODNOTA, (struct sockaddr *)&místní_obor, &délka_HODNOTA) == 0 && místní_obor.sin_port == 0);
    ověřit(vázat_ODKAZ(účastník_HODNOTA, (struct sockaddr *)&místní_obor, sizeof místní_obor) == 0);
    ověřit(통신주소읽기(účastník_HODNOTA, (struct sockaddr *)&místní_obor, &délka_HODNOTA) == 0 && ntohs(místní_obor.sin_port) >= 49152);
    ověřit(vázat_ODKAZ(účastník_HODNOTA, (struct sockaddr *)&místní_obor, sizeof místní_obor) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ověřit(bind(둘째, (struct sockaddr *)&místní_obor, sizeof místní_obor) == -1 && errno == EADDRINUSE);
    ověřit(close(둘째) == 0);
    둘째 = dup(účastník_HODNOTA);
    ověřit(close(účastník_HODNOTA) == 0); účastník_HODNOTA = 둘째;
    partner_HODNOTA.sin_family = AF_INET; partner_HODNOTA.sin_port = 망차례짧은수(číslo_portu);
    ověřit(parsovat_ID_sítě(AF_INET, "10.0.2.2", &partner_HODNOTA.sin_addr) == 1);
    struct timeval počkej_HODNOTA = {0, 200000};
    ověřit(změnit_síť_Nastavení(účastník_HODNOTA, SOL_SOCKET, SO_RCVTIMEO, &počkej_HODNOTA, sizeof počkej_HODNOTA) == 0);
    char data[32];
    ověřit(dostat_datagram_data(účastník_HODNOTA, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ověřit(poslat_datagram_data(účastník_HODNOTA, "posix-udp", 9, 0, (struct sockaddr *)&partner_HODNOTA, sizeof partner_HODNOTA) == 9);
    délka_HODNOTA = sizeof RECEIVED_ODKAZ;
    ověřit(recvfrom(účastník_HODNOTA, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ověřit(dostat_datagram_data(účastník_HODNOTA, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_ODKAZ, &délka_HODNOTA) == 9);
    ověřit(memcmp(data, "posix-udp", 9) == 0 && délka_HODNOTA == 16);
    ověřit(RECEIVED_ODKAZ.sin_port == partner_HODNOTA.sin_port && RECEIVED_ODKAZ.sin_addr.s_addr == partner_HODNOTA.sin_addr.s_addr);
    ověřit(sendto(účastník_HODNOTA, "truncate", 8, 0, (struct sockaddr *)&partner_HODNOTA, sizeof partner_HODNOTA) == 8);
    ověřit(recvfrom(účastník_HODNOTA, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    ověřit(recvfrom(účastník_HODNOTA, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ověřit(sendto(účastník_HODNOTA, NULL, 0, 0, (struct sockaddr *)&partner_HODNOTA, sizeof partner_HODNOTA) == 0);
    ověřit(recvfrom(účastník_HODNOTA, NULL, 0, 0, NULL, NULL) == 0);
    ověřit(recvfrom(účastník_HODNOTA, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ověřit(close(účastník_HODNOTA) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

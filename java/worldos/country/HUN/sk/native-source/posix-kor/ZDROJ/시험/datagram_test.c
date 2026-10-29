#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define overiť(podmienka) do { if (!(podmienka)) { puts("POSIX UDP CHECK FAILED: " #podmienka); return 1; } } while (0)
int main(int 인수개수, char **argument_Zoznam) {
    overiť(인수개수 == 2);
    int číslo_portu = 0;
    for (int 칸 = 0; argument_Zoznam[1][칸]; 칸++) {
        overiť(argument_Zoznam[1][칸] >= '0' && argument_Zoznam[1][칸] <= '9');
        číslo_portu = číslo_portu * 10 + argument_Zoznam[1][칸] - '0';
        overiť(číslo_portu <= 65535);
    }
    int účastník_VALUE = Create_účastník(AF_INET, SOCK_DGRAM, 0);
    overiť(účastník_VALUE == 3);
    struct sockaddr_in miestny_Rozsah = {0}, partnerský_uzol_VALUE = {0}, RECEIVED_adresa = {0};
    miestny_Rozsah.sin_family = AF_INET;
    socklen_t dĺžka_VALUE = sizeof miestny_Rozsah;
    overiť(통신주소읽기(účastník_VALUE, (struct sockaddr *)&miestny_Rozsah, &dĺžka_VALUE) == 0 && miestny_Rozsah.sin_port == 0);
    overiť(BIND_adresa(účastník_VALUE, (struct sockaddr *)&miestny_Rozsah, sizeof miestny_Rozsah) == 0);
    overiť(통신주소읽기(účastník_VALUE, (struct sockaddr *)&miestny_Rozsah, &dĺžka_VALUE) == 0 && ntohs(miestny_Rozsah.sin_port) >= 49152);
    overiť(BIND_adresa(účastník_VALUE, (struct sockaddr *)&miestny_Rozsah, sizeof miestny_Rozsah) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    overiť(bind(둘째, (struct sockaddr *)&miestny_Rozsah, sizeof miestny_Rozsah) == -1 && errno == EADDRINUSE);
    overiť(close(둘째) == 0);
    둘째 = dup(účastník_VALUE);
    overiť(close(účastník_VALUE) == 0); účastník_VALUE = 둘째;
    partnerský_uzol_VALUE.sin_family = AF_INET; partnerský_uzol_VALUE.sin_port = 망차례짧은수(číslo_portu);
    overiť(analyzovať_sieťová_identifikácia(AF_INET, "10.0.2.2", &partnerský_uzol_VALUE.sin_addr) == 1);
    struct timeval počkaj_VALUE = {0, 200000};
    overiť(zmeniť_sieť_Nastavenia(účastník_VALUE, SOL_SOCKET, SO_RCVTIMEO, &počkaj_VALUE, sizeof počkaj_VALUE) == 0);
    char údaje[32];
    overiť(dostať_datagram_údaje(účastník_VALUE, údaje, sizeof údaje, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    overiť(odoslať_datagram_údaje(účastník_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&partnerský_uzol_VALUE, sizeof partnerský_uzol_VALUE) == 9);
    dĺžka_VALUE = sizeof RECEIVED_adresa;
    overiť(recvfrom(účastník_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    overiť(dostať_datagram_údaje(účastník_VALUE, údaje, sizeof údaje, 0, (struct sockaddr *)&RECEIVED_adresa, &dĺžka_VALUE) == 9);
    overiť(memcmp(údaje, "posix-udp", 9) == 0 && dĺžka_VALUE == 16);
    overiť(RECEIVED_adresa.sin_port == partnerský_uzol_VALUE.sin_port && RECEIVED_adresa.sin_addr.s_addr == partnerský_uzol_VALUE.sin_addr.s_addr);
    overiť(sendto(účastník_VALUE, "truncate", 8, 0, (struct sockaddr *)&partnerský_uzol_VALUE, sizeof partnerský_uzol_VALUE) == 8);
    overiť(recvfrom(účastník_VALUE, údaje, 3, 0, NULL, NULL) == 3 && memcmp(údaje, "tru", 3) == 0);
    overiť(recvfrom(účastník_VALUE, údaje, sizeof údaje, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    overiť(sendto(účastník_VALUE, NULL, 0, 0, (struct sockaddr *)&partnerský_uzol_VALUE, sizeof partnerský_uzol_VALUE) == 0);
    overiť(recvfrom(účastník_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    overiť(recvfrom(účastník_VALUE, údaje, sizeof údaje, 0, NULL, NULL) == -1 && errno == EAGAIN);
    overiť(close(účastník_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define provjeriti(uvjet) do { if (!(uvjet)) { puts("POSIX UDP CHECK FAILED: " #uvjet); return 1; } } while (0)
int main(int 인수개수, char **argument_Popis) {
    provjeriti(인수개수 == 2);
    int broj_priključka = 0;
    for (int 칸 = 0; argument_Popis[1][칸]; 칸++) {
        provjeriti(argument_Popis[1][칸] >= '0' && argument_Popis[1][칸] <= '9');
        broj_priključka = broj_priključka * 10 + argument_Popis[1][칸] - '0';
        provjeriti(broj_priključka <= 65535);
    }
    int sudionik_VALUE = Create_sudionik(AF_INET, SOCK_DGRAM, 0);
    provjeriti(sudionik_VALUE == 3);
    struct sockaddr_in lokalno_doseg = {0}, ravnopravan_član_VALUE = {0}, RECEIVED_adresa = {0};
    lokalno_doseg.sin_family = AF_INET;
    socklen_t 길이 = sizeof lokalno_doseg;
    provjeriti(통신주소읽기(sudionik_VALUE, (struct sockaddr *)&lokalno_doseg, &길이) == 0 && lokalno_doseg.sin_port == 0);
    provjeriti(BIND_adresa(sudionik_VALUE, (struct sockaddr *)&lokalno_doseg, sizeof lokalno_doseg) == 0);
    provjeriti(통신주소읽기(sudionik_VALUE, (struct sockaddr *)&lokalno_doseg, &길이) == 0 && ntohs(lokalno_doseg.sin_port) >= 49152);
    provjeriti(BIND_adresa(sudionik_VALUE, (struct sockaddr *)&lokalno_doseg, sizeof lokalno_doseg) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    provjeriti(bind(둘째, (struct sockaddr *)&lokalno_doseg, sizeof lokalno_doseg) == -1 && errno == EADDRINUSE);
    provjeriti(close(둘째) == 0);
    둘째 = dup(sudionik_VALUE);
    provjeriti(close(sudionik_VALUE) == 0); sudionik_VALUE = 둘째;
    ravnopravan_član_VALUE.sin_family = AF_INET; ravnopravan_član_VALUE.sin_port = 망차례짧은수(broj_priključka);
    provjeriti(rastavljati_mrežni_ID(AF_INET, "10.0.2.2", &ravnopravan_član_VALUE.sin_addr) == 1);
    struct timeval čekaj_VALUE = {0, 200000};
    provjeriti(promijeniti_mreža_Postavke(sudionik_VALUE, SOL_SOCKET, SO_RCVTIMEO, &čekaj_VALUE, sizeof čekaj_VALUE) == 0);
    char podaci[32];
    provjeriti(primiti_datogram_podaci(sudionik_VALUE, podaci, sizeof podaci, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    provjeriti(slati_datogram_podaci(sudionik_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&ravnopravan_član_VALUE, sizeof ravnopravan_član_VALUE) == 9);
    길이 = sizeof RECEIVED_adresa;
    provjeriti(recvfrom(sudionik_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    provjeriti(primiti_datogram_podaci(sudionik_VALUE, podaci, sizeof podaci, 0, (struct sockaddr *)&RECEIVED_adresa, &길이) == 9);
    provjeriti(memcmp(podaci, "posix-udp", 9) == 0 && 길이 == 16);
    provjeriti(RECEIVED_adresa.sin_port == ravnopravan_član_VALUE.sin_port && RECEIVED_adresa.sin_addr.s_addr == ravnopravan_član_VALUE.sin_addr.s_addr);
    provjeriti(sendto(sudionik_VALUE, "truncate", 8, 0, (struct sockaddr *)&ravnopravan_član_VALUE, sizeof ravnopravan_član_VALUE) == 8);
    provjeriti(recvfrom(sudionik_VALUE, podaci, 3, 0, NULL, NULL) == 3 && memcmp(podaci, "tru", 3) == 0);
    provjeriti(recvfrom(sudionik_VALUE, podaci, sizeof podaci, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    provjeriti(sendto(sudionik_VALUE, NULL, 0, 0, (struct sockaddr *)&ravnopravan_član_VALUE, sizeof ravnopravan_član_VALUE) == 0);
    provjeriti(recvfrom(sudionik_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    provjeriti(recvfrom(sudionik_VALUE, podaci, sizeof podaci, 0, NULL, NULL) == -1 && errno == EAGAIN);
    provjeriti(close(sudionik_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

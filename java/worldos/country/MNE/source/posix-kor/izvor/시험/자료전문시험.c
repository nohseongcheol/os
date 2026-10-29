#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define verifikovati(stanje) do { if (!(stanje)) { puts("POSIX UDP CHECK FAILED: " #stanje); return 1; } } while (0)
int main(int 인수개수, char **argument_Lista) {
    verifikovati(인수개수 == 2);
    int broj_porta = 0;
    for (int 칸 = 0; argument_Lista[1][칸]; 칸++) {
        verifikovati(argument_Lista[1][칸] >= '0' && argument_Lista[1][칸] <= '9');
        broj_porta = broj_porta * 10 + argument_Lista[1][칸] - '0';
        verifikovati(broj_porta <= 65535);
    }
    int učesnik_VALUE = Create_učesnik(AF_INET, SOCK_DGRAM, 0);
    verifikovati(učesnik_VALUE == 3);
    struct sockaddr_in lokalni_skup = {0}, ravnopravni_uređaj_VALUE = {0}, RECEIVED_adresa = {0};
    lokalni_skup.sin_family = AF_INET;
    socklen_t 길이 = sizeof lokalni_skup;
    verifikovati(통신주소읽기(učesnik_VALUE, (struct sockaddr *)&lokalni_skup, &길이) == 0 && lokalni_skup.sin_port == 0);
    verifikovati(povezati_adresa(učesnik_VALUE, (struct sockaddr *)&lokalni_skup, sizeof lokalni_skup) == 0);
    verifikovati(통신주소읽기(učesnik_VALUE, (struct sockaddr *)&lokalni_skup, &길이) == 0 && ntohs(lokalni_skup.sin_port) >= 49152);
    verifikovati(povezati_adresa(učesnik_VALUE, (struct sockaddr *)&lokalni_skup, sizeof lokalni_skup) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    verifikovati(bind(둘째, (struct sockaddr *)&lokalni_skup, sizeof lokalni_skup) == -1 && errno == EADDRINUSE);
    verifikovati(close(둘째) == 0);
    둘째 = dup(učesnik_VALUE);
    verifikovati(close(učesnik_VALUE) == 0); učesnik_VALUE = 둘째;
    ravnopravni_uređaj_VALUE.sin_family = AF_INET; ravnopravni_uređaj_VALUE.sin_port = 망차례짧은수(broj_porta);
    verifikovati(raščlaniti_ID_mreže(AF_INET, "10.0.2.2", &ravnopravni_uređaj_VALUE.sin_addr) == 1);
    struct timeval čekaj_VALUE = {0, 200000};
    verifikovati(promeniti_Mreža_Postavke(učesnik_VALUE, SOL_SOCKET, SO_RCVTIMEO, &čekaj_VALUE, sizeof čekaj_VALUE) == 0);
    char podaci[32];
    verifikovati(primiti_datagram_podaci(učesnik_VALUE, podaci, sizeof podaci, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifikovati(poslati_datagram_podaci(učesnik_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&ravnopravni_uređaj_VALUE, sizeof ravnopravni_uređaj_VALUE) == 9);
    길이 = sizeof RECEIVED_adresa;
    verifikovati(recvfrom(učesnik_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verifikovati(primiti_datagram_podaci(učesnik_VALUE, podaci, sizeof podaci, 0, (struct sockaddr *)&RECEIVED_adresa, &길이) == 9);
    verifikovati(memcmp(podaci, "posix-udp", 9) == 0 && 길이 == 16);
    verifikovati(RECEIVED_adresa.sin_port == ravnopravni_uređaj_VALUE.sin_port && RECEIVED_adresa.sin_addr.s_addr == ravnopravni_uređaj_VALUE.sin_addr.s_addr);
    verifikovati(sendto(učesnik_VALUE, "truncate", 8, 0, (struct sockaddr *)&ravnopravni_uređaj_VALUE, sizeof ravnopravni_uređaj_VALUE) == 8);
    verifikovati(recvfrom(učesnik_VALUE, podaci, 3, 0, NULL, NULL) == 3 && memcmp(podaci, "tru", 3) == 0);
    verifikovati(recvfrom(učesnik_VALUE, podaci, sizeof podaci, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verifikovati(sendto(učesnik_VALUE, NULL, 0, 0, (struct sockaddr *)&ravnopravni_uređaj_VALUE, sizeof ravnopravni_uređaj_VALUE) == 0);
    verifikovati(recvfrom(učesnik_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    verifikovati(recvfrom(učesnik_VALUE, podaci, sizeof podaci, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verifikovati(close(učesnik_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

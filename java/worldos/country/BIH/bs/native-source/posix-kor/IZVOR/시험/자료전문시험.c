#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define potvrditi(uvjet) do { if (!(uvjet)) { puts("POSIX UDP CHECK FAILED: " #uvjet); return 1; } } while (0)
int main(int 인수개수, char **argument_spisak) {
    potvrditi(인수개수 == 2);
    int broj_priključka = 0;
    for (int prostor_za_unos_unos = 0; argument_spisak[1][prostor_za_unos_unos]; prostor_za_unos_unos++) {
        potvrditi(argument_spisak[1][prostor_za_unos_unos] >= '0' && argument_spisak[1][prostor_za_unos_unos] <= '9');
        broj_priključka = broj_priključka * 10 + argument_spisak[1][prostor_za_unos_unos] - '0';
        potvrditi(broj_priključka <= 65535);
    }
    int završna_tačka_VALUE = Create_završna_tačka(AF_INET, SOCK_DGRAM, 0);
    potvrditi(završna_tačka_VALUE == 3);
    struct sockaddr_in lokalni_opseg = {0}, peer_VALUE = {0}, RECEIVED_adresa = {0};
    lokalni_opseg.sin_family = AF_INET;
    socklen_t dužina_VALUE = sizeof lokalni_opseg;
    potvrditi(통신주소읽기(završna_tačka_VALUE, (struct sockaddr *)&lokalni_opseg, &dužina_VALUE) == 0 && lokalni_opseg.sin_port == 0);
    potvrditi(BIND_adresa(završna_tačka_VALUE, (struct sockaddr *)&lokalni_opseg, sizeof lokalni_opseg) == 0);
    potvrditi(통신주소읽기(završna_tačka_VALUE, (struct sockaddr *)&lokalni_opseg, &dužina_VALUE) == 0 && ntohs(lokalni_opseg.sin_port) >= 49152);
    potvrditi(BIND_adresa(završna_tačka_VALUE, (struct sockaddr *)&lokalni_opseg, sizeof lokalni_opseg) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    potvrditi(bind(둘째, (struct sockaddr *)&lokalni_opseg, sizeof lokalni_opseg) == -1 && errno == EADDRINUSE);
    potvrditi(close(둘째) == 0);
    둘째 = dup(završna_tačka_VALUE);
    potvrditi(close(završna_tačka_VALUE) == 0); završna_tačka_VALUE = 둘째;
    peer_VALUE.sin_family = AF_INET; peer_VALUE.sin_port = 망차례짧은수(broj_priključka);
    potvrditi(raščlanjivati_Mreža_adresa(AF_INET, "10.0.2.2", &peer_VALUE.sin_addr) == 1);
    struct timeval čekaj_VALUE = {0, 200000};
    potvrditi(promijeniti_Mreža_Postavke(završna_tačka_VALUE, SOL_SOCKET, SO_RCVTIMEO, &čekaj_VALUE, sizeof čekaj_VALUE) == 0);
    char podaci[32];
    potvrditi(자료전문받기(završna_tačka_VALUE, podaci, sizeof podaci, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    potvrditi(자료전문보내기(završna_tačka_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 9);
    dužina_VALUE = sizeof RECEIVED_adresa;
    potvrditi(recvfrom(završna_tačka_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    potvrditi(자료전문받기(završna_tačka_VALUE, podaci, sizeof podaci, 0, (struct sockaddr *)&RECEIVED_adresa, &dužina_VALUE) == 9);
    potvrditi(memcmp(podaci, "posix-udp", 9) == 0 && dužina_VALUE == 16);
    potvrditi(RECEIVED_adresa.sin_port == peer_VALUE.sin_port && RECEIVED_adresa.sin_addr.s_addr == peer_VALUE.sin_addr.s_addr);
    potvrditi(sendto(završna_tačka_VALUE, "truncate", 8, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 8);
    potvrditi(recvfrom(završna_tačka_VALUE, podaci, 3, 0, NULL, NULL) == 3 && memcmp(podaci, "tru", 3) == 0);
    potvrditi(recvfrom(završna_tačka_VALUE, podaci, sizeof podaci, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    potvrditi(sendto(završna_tačka_VALUE, NULL, 0, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 0);
    potvrditi(recvfrom(završna_tačka_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    potvrditi(recvfrom(završna_tačka_VALUE, podaci, sizeof podaci, 0, NULL, NULL) == -1 && errno == EAGAIN);
    potvrditi(close(završna_tačka_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

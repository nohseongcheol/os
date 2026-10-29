#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define tarkistaa(ehto) do { if (!(ehto)) { puts("POSIX UDP CHECK FAILED: " #ehto); return 1; } } while (0)
int main(int 인수개수, char **argumentti_luettelo) {
    tarkistaa(인수개수 == 2);
    int portin_numero = 0;
    for (int paikka_merkintä = 0; argumentti_luettelo[1][paikka_merkintä]; paikka_merkintä++) {
        tarkistaa(argumentti_luettelo[1][paikka_merkintä] >= '0' && argumentti_luettelo[1][paikka_merkintä] <= '9');
        portin_numero = portin_numero * 10 + argumentti_luettelo[1][paikka_merkintä] - '0';
        tarkistaa(portin_numero <= 65535);
    }
    int päätepiste_ARVO = Luo_päätepiste(AF_INET, SOCK_DGRAM, 0);
    tarkistaa(päätepiste_ARVO == 3);
    struct sockaddr_in paikallinen_laajuus = {0}, vertaissolmu_ARVO = {0}, SAATU_HINTA_OSOITE = {0};
    paikallinen_laajuus.sin_family = AF_INET;
    socklen_t kesto_ARVO = sizeof paikallinen_laajuus;
    tarkistaa(lukea_vastake_OSOITE(päätepiste_ARVO, (struct sockaddr *)&paikallinen_laajuus, &kesto_ARVO) == 0 && paikallinen_laajuus.sin_port == 0);
    tarkistaa(BIND_OSOITE(päätepiste_ARVO, (struct sockaddr *)&paikallinen_laajuus, sizeof paikallinen_laajuus) == 0);
    tarkistaa(lukea_vastake_OSOITE(päätepiste_ARVO, (struct sockaddr *)&paikallinen_laajuus, &kesto_ARVO) == 0 && ntohs(paikallinen_laajuus.sin_port) >= 49152);
    tarkistaa(BIND_OSOITE(päätepiste_ARVO, (struct sockaddr *)&paikallinen_laajuus, sizeof paikallinen_laajuus) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    tarkistaa(bind(둘째, (struct sockaddr *)&paikallinen_laajuus, sizeof paikallinen_laajuus) == -1 && errno == EADDRINUSE);
    tarkistaa(close(둘째) == 0);
    둘째 = dup(päätepiste_ARVO);
    tarkistaa(close(päätepiste_ARVO) == 0); päätepiste_ARVO = 둘째;
    vertaissolmu_ARVO.sin_family = AF_INET; vertaissolmu_ARVO.sin_port = 망차례짧은수(portin_numero);
    tarkistaa(jäsentää_verkkotunnus(AF_INET, "10.0.2.2", &vertaissolmu_ARVO.sin_addr) == 1);
    struct timeval odottaa_ARVO = {0, 200000};
    tarkistaa(muuttaa_verkko_Asetukset(päätepiste_ARVO, SOL_SOCKET, SO_RCVTIMEO, &odottaa_ARVO, sizeof odottaa_ARVO) == 0);
    char data[32];
    tarkistaa(saada_datagrammi_data(päätepiste_ARVO, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tarkistaa(lähettää_datagrammi_data(päätepiste_ARVO, "posix-udp", 9, 0, (struct sockaddr *)&vertaissolmu_ARVO, sizeof vertaissolmu_ARVO) == 9);
    kesto_ARVO = sizeof SAATU_HINTA_OSOITE;
    tarkistaa(recvfrom(päätepiste_ARVO, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    tarkistaa(saada_datagrammi_data(päätepiste_ARVO, data, sizeof data, 0, (struct sockaddr *)&SAATU_HINTA_OSOITE, &kesto_ARVO) == 9);
    tarkistaa(memcmp(data, "posix-udp", 9) == 0 && kesto_ARVO == 16);
    tarkistaa(SAATU_HINTA_OSOITE.sin_port == vertaissolmu_ARVO.sin_port && SAATU_HINTA_OSOITE.sin_addr.s_addr == vertaissolmu_ARVO.sin_addr.s_addr);
    tarkistaa(sendto(päätepiste_ARVO, "truncate", 8, 0, (struct sockaddr *)&vertaissolmu_ARVO, sizeof vertaissolmu_ARVO) == 8);
    tarkistaa(recvfrom(päätepiste_ARVO, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    tarkistaa(recvfrom(päätepiste_ARVO, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tarkistaa(sendto(päätepiste_ARVO, NULL, 0, 0, (struct sockaddr *)&vertaissolmu_ARVO, sizeof vertaissolmu_ARVO) == 0);
    tarkistaa(recvfrom(päätepiste_ARVO, NULL, 0, 0, NULL, NULL) == 0);
    tarkistaa(recvfrom(päätepiste_ARVO, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    tarkistaa(close(päätepiste_ARVO) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define kinnitama(tingimus) do { if (!(tingimus)) { puts("POSIX UDP CHECK FAILED: " #tingimus); return 1; } } while (0)
int main(int 인수개수, char **argument_Loend) {
    kinnitama(인수개수 == 2);
    int pordinumber = 0;
    for (int 칸 = 0; argument_Loend[1][칸]; 칸++) {
        kinnitama(argument_Loend[1][칸] >= '0' && argument_Loend[1][칸] <= '9');
        pordinumber = pordinumber * 10 + argument_Loend[1][칸] - '0';
        kinnitama(pordinumber <= 65535);
    }
    int osaleja_VALUE = avama_osaleja(AF_INET, SOCK_DGRAM, 0);
    kinnitama(osaleja_VALUE == 3);
    struct sockaddr_in kohalik_skoop = {0}, partner_VALUE = {0}, RECEIVED_ADDRESS = {0};
    kohalik_skoop.sin_family = AF_INET;
    socklen_t 길이 = sizeof kohalik_skoop;
    kinnitama(통신주소읽기(osaleja_VALUE, (struct sockaddr *)&kohalik_skoop, &길이) == 0 && kohalik_skoop.sin_port == 0);
    kinnitama(BIND_ADDRESS(osaleja_VALUE, (struct sockaddr *)&kohalik_skoop, sizeof kohalik_skoop) == 0);
    kinnitama(통신주소읽기(osaleja_VALUE, (struct sockaddr *)&kohalik_skoop, &길이) == 0 && ntohs(kohalik_skoop.sin_port) >= 49152);
    kinnitama(BIND_ADDRESS(osaleja_VALUE, (struct sockaddr *)&kohalik_skoop, sizeof kohalik_skoop) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    kinnitama(bind(둘째, (struct sockaddr *)&kohalik_skoop, sizeof kohalik_skoop) == -1 && errno == EADDRINUSE);
    kinnitama(close(둘째) == 0);
    둘째 = dup(osaleja_VALUE);
    kinnitama(close(osaleja_VALUE) == 0); osaleja_VALUE = 둘째;
    partner_VALUE.sin_family = AF_INET; partner_VALUE.sin_port = 망차례짧은수(pordinumber);
    kinnitama(sõeluma_võrgu_ID(AF_INET, "10.0.2.2", &partner_VALUE.sin_addr) == 1);
    struct timeval Oota_VALUE = {0, 200000};
    kinnitama(muutma_võrk_Sätted(osaleja_VALUE, SOL_SOCKET, SO_RCVTIMEO, &Oota_VALUE, sizeof Oota_VALUE) == 0);
    char andmed[32];
    kinnitama(saama_datagramm_andmed(osaleja_VALUE, andmed, sizeof andmed, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    kinnitama(saatma_datagramm_andmed(osaleja_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&partner_VALUE, sizeof partner_VALUE) == 9);
    길이 = sizeof RECEIVED_ADDRESS;
    kinnitama(recvfrom(osaleja_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    kinnitama(saama_datagramm_andmed(osaleja_VALUE, andmed, sizeof andmed, 0, (struct sockaddr *)&RECEIVED_ADDRESS, &길이) == 9);
    kinnitama(memcmp(andmed, "posix-udp", 9) == 0 && 길이 == 16);
    kinnitama(RECEIVED_ADDRESS.sin_port == partner_VALUE.sin_port && RECEIVED_ADDRESS.sin_addr.s_addr == partner_VALUE.sin_addr.s_addr);
    kinnitama(sendto(osaleja_VALUE, "truncate", 8, 0, (struct sockaddr *)&partner_VALUE, sizeof partner_VALUE) == 8);
    kinnitama(recvfrom(osaleja_VALUE, andmed, 3, 0, NULL, NULL) == 3 && memcmp(andmed, "tru", 3) == 0);
    kinnitama(recvfrom(osaleja_VALUE, andmed, sizeof andmed, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    kinnitama(sendto(osaleja_VALUE, NULL, 0, 0, (struct sockaddr *)&partner_VALUE, sizeof partner_VALUE) == 0);
    kinnitama(recvfrom(osaleja_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    kinnitama(recvfrom(osaleja_VALUE, andmed, sizeof andmed, 0, NULL, NULL) == -1 && errno == EAGAIN);
    kinnitama(close(osaleja_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

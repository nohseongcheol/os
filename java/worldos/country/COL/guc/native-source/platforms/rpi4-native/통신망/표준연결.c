#include "string.h"
size_t strlen(const char *kaleena_atijaaya) { const char *자료위치 = kaleena_atijaaya; while (*자료위치) 자료위치++; return 자료위치 - kaleena_atijaaya; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *jalamüinjatü_atijaaya, const void *kaleena_atijaaya, size_t 개수) { unsigned char *가로좌표 = jalamüinjatü_atijaaya; const unsigned char *세로좌표 = kaleena_atijaaya; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; 가로좌표[개수] = 세로좌표[개수]; } } return jalamüinjatü_atijaaya; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *둘째값++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *kaleena_atijaaya, char **끝위치, int apa_ajanaa_ajutuu) {
    const char *시작위치 = kaleena_atijaaya; unsigned long ajutuu = 0; int atijitaalüjiaa_ajutuu = 1, 하나라도 = 0;
    while (*kaleena_atijaaya == ' ' || (*kaleena_atijaaya >= 9 && *kaleena_atijaaya <= 13)) kaleena_atijaaya++;
    if (*kaleena_atijaaya == '-' || *kaleena_atijaaya == '+') { if (*kaleena_atijaaya == '-') atijitaalüjiaa_ajutuu = -1; kaleena_atijaaya++; }
    if (apa_ajanaa_ajutuu == 0) apa_ajanaa_ajutuu = 10;
    while (*kaleena_atijaaya >= '0' && *kaleena_atijaaya <= '9' && *kaleena_atijaaya - '0' < apa_ajanaa_ajutuu) {
        unsigned 숫자 = *kaleena_atijaaya++ - '0'; 하나라도 = 1;
        if (ajutuu > (0x7ffffffffffffffful - 숫자) / (unsigned)apa_ajanaa_ajutuu) ajutuu = 0x7ffffffffffffffful;
        else ajutuu = ajutuu * apa_ajanaa_ajutuu + 숫자;
    }
    if (끝위치) *끝위치 = (char *)(하나라도 ? kaleena_atijaaya : 시작위치); return atijitaalüjiaa_ajutuu > 0 ? (long)ajutuu : -(long)ajutuu;
}
int atoi(const char *kaleena_atijaaya) { return (int)strtol(kaleena_atijaaya, 0, 10); }

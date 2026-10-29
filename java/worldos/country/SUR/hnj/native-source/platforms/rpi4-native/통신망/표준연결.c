#include "string.h"
size_t strlen(const char *문자열값) { const char *자료위치 = 문자열값; while (*자료위치) 자료위치++; return 자료위치 - 문자열값; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *목적자료, const void *문자열값, size_t 개수) { unsigned char *가로좌표 = 목적자료; const unsigned char *세로좌표 = 문자열값; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; 가로좌표[개수] = 세로좌표[개수]; } } return 목적자료; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *둘째값++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *문자열값, char **끝위치, int 바탕) {
    const char *시작위치 = 문자열값; unsigned long 값 = 0; int 부호 = 1, 하나라도 = 0;
    while (*문자열값 == ' ' || (*문자열값 >= 9 && *문자열값 <= 13)) 문자열값++;
    if (*문자열값 == '-' || *문자열값 == '+') { if (*문자열값 == '-') 부호 = -1; 문자열값++; }
    if (바탕 == 0) 바탕 = 10;
    while (*문자열값 >= '0' && *문자열값 <= '9' && *문자열값 - '0' < 바탕) {
        unsigned 숫자 = *문자열값++ - '0'; 하나라도 = 1;
        if (값 > (0x7ffffffffffffffful - 숫자) / (unsigned)바탕) 값 = 0x7ffffffffffffffful;
        else 값 = 값 * 바탕 + 숫자;
    }
    if (끝위치) *끝위치 = (char *)(하나라도 ? 문자열값 : 시작위치); return 부호 > 0 ? (long)값 : -(long)값;
}
int atoi(const char *문자열값) { return (int)strtol(문자열값, 0, 10); }

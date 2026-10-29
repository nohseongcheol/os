#include "string.h"
size_t strlen(const char *стринг_подаци) { const char *자료위치 = стринг_подаци; while (*자료위치) 자료위치++; return 자료위치 - стринг_подаци; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *одредиште_подаци, const void *стринг_подаци, size_t 개수) { unsigned char *가로좌표 = одредиште_подаци; const unsigned char *세로좌표 = стринг_подаци; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; 가로좌표[개수] = 세로좌표[개수]; } } return одредиште_подаци; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *둘째값++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *стринг_подаци, char **끝위치, int позадина_вриједност) {
    const char *시작위치 = стринг_подаци; unsigned long вриједност = 0; int кодирање_вриједност = 1, 하나라도 = 0;
    while (*стринг_подаци == ' ' || (*стринг_подаци >= 9 && *стринг_подаци <= 13)) стринг_подаци++;
    if (*стринг_подаци == '-' || *стринг_подаци == '+') { if (*стринг_подаци == '-') кодирање_вриједност = -1; стринг_подаци++; }
    if (позадина_вриједност == 0) позадина_вриједност = 10;
    while (*стринг_подаци >= '0' && *стринг_подаци <= '9' && *стринг_подаци - '0' < позадина_вриједност) {
        unsigned 숫자 = *стринг_подаци++ - '0'; 하나라도 = 1;
        if (вриједност > (0x7ffffffffffffffful - 숫자) / (unsigned)позадина_вриједност) вриједност = 0x7ffffffffffffffful;
        else вриједност = вриједност * позадина_вриједност + 숫자;
    }
    if (끝위치) *끝위치 = (char *)(하나라도 ? стринг_подаци : 시작위치); return кодирање_вриједност > 0 ? (long)вриједност : -(long)вриједност;
}
int atoi(const char *стринг_подаци) { return (int)strtol(стринг_подаци, 0, 10); }

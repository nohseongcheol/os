#include "string.h"
size_t strlen(const char *مزى_اومتوک) { const char *자료위치 = مزى_اومتوک; while (*자료위치) 자료위치++; return 자료위치 - مزى_اومتوک; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *موخه_اومتوک, const void *مزى_اومتوک, size_t 개수) { unsigned char *가로좌표 = موخه_اومتوک; const unsigned char *세로좌표 = مزى_اومتوک; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; 가로좌표[개수] = 세로좌표[개수]; } } return موخه_اومتوک; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *둘째값++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *مزى_اومتوک, char **끝위치, int شاليد_ارزښت) {
    const char *시작위치 = مزى_اومتوک; unsigned long ارزښت = 0; int کوډييزونه_ارزښت = 1, 하나라도 = 0;
    while (*مزى_اومتوک == ' ' || (*مزى_اومتوک >= 9 && *مزى_اومتوک <= 13)) مزى_اومتوک++;
    if (*مزى_اومتوک == '-' || *مزى_اومتوک == '+') { if (*مزى_اومتوک == '-') کوډييزونه_ارزښت = -1; مزى_اومتوک++; }
    if (شاليد_ارزښت == 0) شاليد_ارزښت = 10;
    while (*مزى_اومتوک >= '0' && *مزى_اومتوک <= '9' && *مزى_اومتوک - '0' < شاليد_ارزښت) {
        unsigned 숫자 = *مزى_اومتوک++ - '0'; 하나라도 = 1;
        if (ارزښت > (0x7ffffffffffffffful - 숫자) / (unsigned)شاليد_ارزښت) ارزښت = 0x7ffffffffffffffful;
        else ارزښت = ارزښت * شاليد_ارزښت + 숫자;
    }
    if (끝위치) *끝위치 = (char *)(하나라도 ? مزى_اومتوک : 시작위치); return کوډييزونه_ارزښت > 0 ? (long)ارزښت : -(long)ارزښت;
}
int atoi(const char *مزى_اومتوک) { return (int)strtol(مزى_اومتوک, 0, 10); }

#include "string.h"
size_t strlen(const char *رست_دەیتا) { const char *자료위치 = رست_دەیتا; while (*자료위치) 자료위치++; return 자료위치 - رست_دەیتا; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *پۆوتانی_x = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*پۆوتانی_x != *세로좌표) return (int)*پۆوتانی_x - *세로좌표; پۆوتانی_x++; 세로좌표++; } return 0; }
void *memmove(void *جێمەبەست_دەیتا, const void *رست_دەیتا, size_t 개수) { unsigned char *پۆوتانی_x = جێمەبەست_دەیتا; const unsigned char *세로좌표 = رست_دەیتا; if (پۆوتانی_x < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) پۆوتانی_x[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; پۆوتانی_x[개수] = 세로좌표[개수]; } } return جێمەبەست_دەیتا; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char پۆوتانی_x = *첫째값++, 세로좌표 = *둘째값++; if (پۆوتانی_x != 세로좌표) return (int)پۆوتانی_x-세로좌표; if (!پۆوتانی_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *رست_دەیتا, char **دوایی_کردن_ئۆفسێت, int بن_زمینه_نرخ) {
    const char *دەستپێك_ئۆفسێت = رست_دەیتا; unsigned long نرخ = 0; int نهێنبەندی_نرخ = 1, 하나라도 = 0;
    while (*رست_دەیتا == ' ' || (*رست_دەیتا >= 9 && *رست_دەیتا <= 13)) رست_دەیتا++;
    if (*رست_دەیتا == '-' || *رست_دەیتا == '+') { if (*رست_دەیتا == '-') نهێنبەندی_نرخ = -1; رست_دەیتا++; }
    if (بن_زمینه_نرخ == 0) بن_زمینه_نرخ = 10;
    while (*رست_دەیتا >= '0' && *رست_دەیتا <= '9' && *رست_دەیتا - '0' < بن_زمینه_نرخ) {
        unsigned ڕه_نووس_نرخ = *رست_دەیتا++ - '0'; 하나라도 = 1;
        if (نرخ > (0x7ffffffffffffffful - ڕه_نووس_نرخ) / (unsigned)بن_زمینه_نرخ) نرخ = 0x7ffffffffffffffful;
        else نرخ = نرخ * بن_زمینه_نرخ + ڕه_نووس_نرخ;
    }
    if (دوایی_کردن_ئۆفسێت) *دوایی_کردن_ئۆفسێت = (char *)(하나라도 ? رست_دەیتا : دەستپێك_ئۆفسێت); return نهێنبەندی_نرخ > 0 ? (long)نرخ : -(long)نرخ;
}
int atoi(const char *رست_دەیتا) { return (int)strtol(رست_دەیتا, 0, 10); }

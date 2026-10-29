#include "string.h"
size_t strlen(const char *سلک_کوائف) { const char *کوائف_پوزیشن_ٹھیک_کریں = سلک_کوائف; while (*کوائف_پوزیشن_ٹھیک_کریں) کوائف_پوزیشن_ٹھیک_کریں++; return کوائف_پوزیشن_ٹھیک_کریں - سلک_کوائف; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *ایکس_مربوط = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*ایکس_مربوط != *세로좌표) return (int)*ایکس_مربوط - *세로좌표; ایکس_مربوط++; 세로좌표++; } return 0; }
void *memmove(void *منزل_مقصود_کوائف, const void *سلک_کوائف, size_t 개수) { unsigned char *ایکس_مربوط = منزل_مقصود_کوائف; const unsigned char *세로좌표 = سلک_کوائف; if (ایکس_مربوط < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) ایکس_مربوط[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; ایکس_مربوط[개수] = 세로좌표[개수]; } } return منزل_مقصود_کوائف; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char ایکس_مربوط = *첫째값++, 세로좌표 = *둘째값++; if (ایکس_مربوط != 세로좌표) return (int)ایکس_مربوط-세로좌표; if (!ایکس_مربوط) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *سلک_کوائف, char **اختتام_آفسٹ, int پس_منظر_قدر) {
    const char *ابتدا_آفسٹ = سلک_کوائف; unsigned long قدر = 0; int ضابطہ_بندی_قدر = 1, 하나라도 = 0;
    while (*سلک_کوائف == ' ' || (*سلک_کوائف >= 9 && *سلک_کوائف <= 13)) سلک_کوائف++;
    if (*سلک_کوائف == '-' || *سلک_کوائف == '+') { if (*سلک_کوائف == '-') ضابطہ_بندی_قدر = -1; سلک_کوائف++; }
    if (پس_منظر_قدر == 0) پس_منظر_قدر = 10;
    while (*سلک_کوائف >= '0' && *سلک_کوائف <= '9' && *سلک_کوائف - '0' < پس_منظر_قدر) {
        unsigned عدد_قدر = *سلک_کوائف++ - '0'; 하나라도 = 1;
        if (قدر > (0x7ffffffffffffffful - عدد_قدر) / (unsigned)پس_منظر_قدر) قدر = 0x7ffffffffffffffful;
        else قدر = قدر * پس_منظر_قدر + عدد_قدر;
    }
    if (اختتام_آفسٹ) *اختتام_آفسٹ = (char *)(하나라도 ? سلک_کوائف : ابتدا_آفسٹ); return ضابطہ_بندی_قدر > 0 ? (long)قدر : -(long)قدر;
}
int atoi(const char *سلک_کوائف) { return (int)strtol(سلک_کوائف, 0, 10); }

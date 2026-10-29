#include "string.h"
size_t strlen(const char *dữLiệuChuỗi) { const char *vịTríDữLiệu = dữLiệuChuỗi; while (*vịTríDữLiệu) vịTríDữLiệu++; return vịTríDữLiệu - dữLiệuChuỗi; }
int memcmp(const void *giáTrịĐầuTiên, const void *giáTrịThứHai, size_t sốLượngPhầnMục) { const unsigned char *tọaĐộX = giáTrịĐầuTiên, *tọaĐộY = giáTrịThứHai; while (sốLượngPhầnMục--) { if (*tọaĐộX != *tọaĐộY) return (int)*tọaĐộX - *tọaĐộY; tọaĐộX++; tọaĐộY++; } return 0; }
void *memmove(void *dữLiệuĐích, const void *dữLiệuChuỗi, size_t sốLượngPhầnMục) { unsigned char *tọaĐộX = dữLiệuĐích; const unsigned char *tọaĐộY = dữLiệuChuỗi; if (tọaĐộX < tọaĐộY) { for (size_t chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) tọaĐộX[chỉSốThứBậc] = tọaĐộY[chỉSốThứBậc]; } else { while (sốLượngPhầnMục) { sốLượngPhầnMục--; tọaĐộX[sốLượngPhầnMục] = tọaĐộY[sốLượngPhầnMục]; } } return dữLiệuĐích; }
int strncmp(const char *giáTrịĐầuTiên, const char *giáTrịThứHai, size_t sốLượngPhầnMục) { while (sốLượngPhầnMục--) { unsigned char tọaĐộX = *giáTrịĐầuTiên++, tọaĐộY = *giáTrịThứHai++; if (tọaĐộX != tọaĐộY) return (int)tọaĐộX-tọaĐộY; if (!tọaĐộX) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *dữLiệuChuỗi, char **độLệchKếtThúc, int giáTrịNền) {
    const char *bắtChạyĐộLệch = dữLiệuChuỗi; unsigned long giáTrị = 0; int giáTrịBảngMã = 1, giáTrịBấtKỳ = 0;
    while (*dữLiệuChuỗi == ' ' || (*dữLiệuChuỗi >= 9 && *dữLiệuChuỗi <= 13)) dữLiệuChuỗi++;
    if (*dữLiệuChuỗi == '-' || *dữLiệuChuỗi == '+') { if (*dữLiệuChuỗi == '-') giáTrịBảngMã = -1; dữLiệuChuỗi++; }
    if (giáTrịNền == 0) giáTrịNền = 10;
    while (*dữLiệuChuỗi >= '0' && *dữLiệuChuỗi <= '9' && *dữLiệuChuỗi - '0' < giáTrịNền) {
        unsigned giáTrịChữSố = *dữLiệuChuỗi++ - '0'; giáTrịBấtKỳ = 1;
        if (giáTrị > (0x7ffffffffffffffful - giáTrịChữSố) / (unsigned)giáTrịNền) giáTrị = 0x7ffffffffffffffful;
        else giáTrị = giáTrị * giáTrịNền + giáTrịChữSố;
    }
    if (độLệchKếtThúc) *độLệchKếtThúc = (char *)(giáTrịBấtKỳ ? dữLiệuChuỗi : bắtChạyĐộLệch); return giáTrịBảngMã > 0 ? (long)giáTrị : -(long)giáTrị;
}
int atoi(const char *dữLiệuChuỗi) { return (int)strtol(dữLiệuChuỗi, 0, 10); }

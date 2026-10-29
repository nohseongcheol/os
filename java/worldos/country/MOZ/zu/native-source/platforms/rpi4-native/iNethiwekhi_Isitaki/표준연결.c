#include "string.h"
size_t strlen(const char *uchunge_imininingwane) { const char *자료위치 = uchunge_imininingwane; while (*자료위치) 자료위치++; return 자료위치 - uchunge_imininingwane; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *okuxhumanisa_u_x = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*okuxhumanisa_u_x != *세로좌표) return (int)*okuxhumanisa_u_x - *세로좌표; okuxhumanisa_u_x++; 세로좌표++; } return 0; }
void *memmove(void *isikhumulo_imininingwane, const void *uchunge_imininingwane, size_t 개수) { unsigned char *okuxhumanisa_u_x = isikhumulo_imininingwane; const unsigned char *세로좌표 = uchunge_imininingwane; if (okuxhumanisa_u_x < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) okuxhumanisa_u_x[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; okuxhumanisa_u_x[개수] = 세로좌표[개수]; } } return isikhumulo_imininingwane; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char okuxhumanisa_u_x = *첫째값++, 세로좌표 = *둘째값++; if (okuxhumanisa_u_x != 세로좌표) return (int)okuxhumanisa_u_x-세로좌표; if (!okuxhumanisa_u_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *uchunge_imininingwane, char **yekisa_I_ofisethi, int ngemuva_inani) {
    const char *qala_I_ofisethi = uchunge_imininingwane; unsigned long inani = 0; int ukubhala_ngokufihla_inani = 1, 하나라도 = 0;
    while (*uchunge_imininingwane == ' ' || (*uchunge_imininingwane >= 9 && *uchunge_imininingwane <= 13)) uchunge_imininingwane++;
    if (*uchunge_imininingwane == '-' || *uchunge_imininingwane == '+') { if (*uchunge_imininingwane == '-') ukubhala_ngokufihla_inani = -1; uchunge_imininingwane++; }
    if (ngemuva_inani == 0) ngemuva_inani = 10;
    while (*uchunge_imininingwane >= '0' && *uchunge_imininingwane <= '9' && *uchunge_imininingwane - '0' < ngemuva_inani) {
        unsigned idijithi_inani = *uchunge_imininingwane++ - '0'; 하나라도 = 1;
        if (inani > (0x7ffffffffffffffful - idijithi_inani) / (unsigned)ngemuva_inani) inani = 0x7ffffffffffffffful;
        else inani = inani * ngemuva_inani + idijithi_inani;
    }
    if (yekisa_I_ofisethi) *yekisa_I_ofisethi = (char *)(하나라도 ? uchunge_imininingwane : qala_I_ofisethi); return ukubhala_ngokufihla_inani > 0 ? (long)inani : -(long)inani;
}
int atoi(const char *uchunge_imininingwane) { return (int)strtol(uchunge_imininingwane, 0, 10); }

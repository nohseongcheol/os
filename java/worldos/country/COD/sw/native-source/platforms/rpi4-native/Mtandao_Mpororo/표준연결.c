#include "string.h"
size_t strlen(const char *tungo_data) { const char *자료위치 = tungo_data; while (*자료위치) 자료위치++; return 자료위치 - tungo_data; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *jira_x = 첫째값, *Kitufe_cha_Y_kiratibu = 둘째값; while (개수--) { if (*jira_x != *Kitufe_cha_Y_kiratibu) return (int)*jira_x - *Kitufe_cha_Y_kiratibu; jira_x++; Kitufe_cha_Y_kiratibu++; } return 0; }
void *memmove(void *fikio_data, const void *tungo_data, size_t 개수) { unsigned char *jira_x = fikio_data; const unsigned char *Kitufe_cha_Y_kiratibu = tungo_data; if (jira_x < Kitufe_cha_Y_kiratibu) { for (size_t 순번 = 0; 순번 < 개수; 순번++) jira_x[순번] = Kitufe_cha_Y_kiratibu[순번]; } else { while (개수) { 개수--; jira_x[개수] = Kitufe_cha_Y_kiratibu[개수]; } } return fikio_data; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char jira_x = *첫째값++, Kitufe_cha_Y_kiratibu = *둘째값++; if (jira_x != Kitufe_cha_Y_kiratibu) return (int)jira_x-Kitufe_cha_Y_kiratibu; if (!jira_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *tungo_data, char **tamatia_Chipua, int nyuma_thamani) {
    const char *Anza_Chipua = tungo_data; unsigned long thamani = 0; int usimbaji_thamani = 1, 하나라도 = 0;
    while (*tungo_data == ' ' || (*tungo_data >= 9 && *tungo_data <= 13)) tungo_data++;
    if (*tungo_data == '-' || *tungo_data == '+') { if (*tungo_data == '-') usimbaji_thamani = -1; tungo_data++; }
    if (nyuma_thamani == 0) nyuma_thamani = 10;
    while (*tungo_data >= '0' && *tungo_data <= '9' && *tungo_data - '0' < nyuma_thamani) {
        unsigned dijiti_thamani = *tungo_data++ - '0'; 하나라도 = 1;
        if (thamani > (0x7ffffffffffffffful - dijiti_thamani) / (unsigned)nyuma_thamani) thamani = 0x7ffffffffffffffful;
        else thamani = thamani * nyuma_thamani + dijiti_thamani;
    }
    if (tamatia_Chipua) *tamatia_Chipua = (char *)(하나라도 ? tungo_data : Anza_Chipua); return usimbaji_thamani > 0 ? (long)thamani : -(long)thamani;
}
int atoi(const char *tungo_data) { return (int)strtol(tungo_data, 0, 10); }

#include "string.h"
size_t strlen(const char *streng_data) { const char *data_plassere = streng_data; while (*data_plassere) data_plassere++; return data_plassere - streng_data; }
int memcmp(const void *첫째값, const void *SEKUND_VERDI, size_t vare_ANTALL) { const unsigned char *x_koordinat = 첫째값, *Y_koordinat = SEKUND_VERDI; while (vare_ANTALL--) { if (*x_koordinat != *Y_koordinat) return (int)*x_koordinat - *Y_koordinat; x_koordinat++; Y_koordinat++; } return 0; }
void *memmove(void *mål_data, const void *streng_data, size_t vare_ANTALL) { unsigned char *x_koordinat = mål_data; const unsigned char *Y_koordinat = streng_data; if (x_koordinat < Y_koordinat) { for (size_t 순번 = 0; 순번 < vare_ANTALL; 순번++) x_koordinat[순번] = Y_koordinat[순번]; } else { while (vare_ANTALL) { vare_ANTALL--; x_koordinat[vare_ANTALL] = Y_koordinat[vare_ANTALL]; } } return mål_data; }
int strncmp(const char *첫째값, const char *SEKUND_VERDI, size_t vare_ANTALL) { while (vare_ANTALL--) { unsigned char x_koordinat = *첫째값++, Y_koordinat = *SEKUND_VERDI++; if (x_koordinat != Y_koordinat) return (int)x_koordinat-Y_koordinat; if (!x_koordinat) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *streng_data, char **avslutte_en_samtale_FORSKYVNING, int bakgrunn_VERDI) {
    const char *START_FORSKYVNING = streng_data; unsigned long VERDI = 0; int koding_VERDI = 1, 하나라도 = 0;
    while (*streng_data == ' ' || (*streng_data >= 9 && *streng_data <= 13)) streng_data++;
    if (*streng_data == '-' || *streng_data == '+') { if (*streng_data == '-') koding_VERDI = -1; streng_data++; }
    if (bakgrunn_VERDI == 0) bakgrunn_VERDI = 10;
    while (*streng_data >= '0' && *streng_data <= '9' && *streng_data - '0' < bakgrunn_VERDI) {
        unsigned siffer_VERDI = *streng_data++ - '0'; 하나라도 = 1;
        if (VERDI > (0x7ffffffffffffffful - siffer_VERDI) / (unsigned)bakgrunn_VERDI) VERDI = 0x7ffffffffffffffful;
        else VERDI = VERDI * bakgrunn_VERDI + siffer_VERDI;
    }
    if (avslutte_en_samtale_FORSKYVNING) *avslutte_en_samtale_FORSKYVNING = (char *)(하나라도 ? streng_data : START_FORSKYVNING); return koding_VERDI > 0 ? (long)VERDI : -(long)VERDI;
}
int atoi(const char *streng_data) { return (int)strtol(streng_data, 0, 10); }

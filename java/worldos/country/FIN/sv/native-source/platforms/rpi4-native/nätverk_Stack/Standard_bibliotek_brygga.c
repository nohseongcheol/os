#include "string.h"
size_t strlen(const char *sträng_data) { const char *data_placera = sträng_data; while (*data_placera) data_placera++; return data_placera - sträng_data; }
int memcmp(const void *첫째값, const void *SEKUND_värde, size_t objekt_ANTAL) { const unsigned char *x_koordinat = 첫째값, *Y_koordinat = SEKUND_värde; while (objekt_ANTAL--) { if (*x_koordinat != *Y_koordinat) return (int)*x_koordinat - *Y_koordinat; x_koordinat++; Y_koordinat++; } return 0; }
void *memmove(void *mål_data, const void *sträng_data, size_t objekt_ANTAL) { unsigned char *x_koordinat = mål_data; const unsigned char *Y_koordinat = sträng_data; if (x_koordinat < Y_koordinat) { for (size_t 순번 = 0; 순번 < objekt_ANTAL; 순번++) x_koordinat[순번] = Y_koordinat[순번]; } else { while (objekt_ANTAL) { objekt_ANTAL--; x_koordinat[objekt_ANTAL] = Y_koordinat[objekt_ANTAL]; } } return mål_data; }
int strncmp(const char *첫째값, const char *SEKUND_värde, size_t objekt_ANTAL) { while (objekt_ANTAL--) { unsigned char x_koordinat = *첫째값++, Y_koordinat = *SEKUND_värde++; if (x_koordinat != Y_koordinat) return (int)x_koordinat-Y_koordinat; if (!x_koordinat) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *sträng_data, char **avsluta_FÖRSKJUTNING, int Bakgrund_värde) {
    const char *START_FÖRSKJUTNING = sträng_data; unsigned long värde = 0; int kodning_värde = 1, 하나라도 = 0;
    while (*sträng_data == ' ' || (*sträng_data >= 9 && *sträng_data <= 13)) sträng_data++;
    if (*sträng_data == '-' || *sträng_data == '+') { if (*sträng_data == '-') kodning_värde = -1; sträng_data++; }
    if (Bakgrund_värde == 0) Bakgrund_värde = 10;
    while (*sträng_data >= '0' && *sträng_data <= '9' && *sträng_data - '0' < Bakgrund_värde) {
        unsigned siffra_värde = *sträng_data++ - '0'; 하나라도 = 1;
        if (värde > (0x7ffffffffffffffful - siffra_värde) / (unsigned)Bakgrund_värde) värde = 0x7ffffffffffffffful;
        else värde = värde * Bakgrund_värde + siffra_värde;
    }
    if (avsluta_FÖRSKJUTNING) *avsluta_FÖRSKJUTNING = (char *)(하나라도 ? sträng_data : START_FÖRSKJUTNING); return kodning_värde > 0 ? (long)värde : -(long)värde;
}
int atoi(const char *sträng_data) { return (int)strtol(sträng_data, 0, 10); }

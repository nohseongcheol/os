#include "string.h"
size_t strlen(const char *virkne_dati) { const char *dati_amats = virkne_dati; while (*dati_amats) dati_amats++; return dati_amats - virkne_dati; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t krājums_COUNT) { const unsigned char *x_koordināta = 첫째값, *세로좌표 = SECOND_VALUE; while (krājums_COUNT--) { if (*x_koordināta != *세로좌표) return (int)*x_koordināta - *세로좌표; x_koordināta++; 세로좌표++; } return 0; }
void *memmove(void *mērķis_dati, const void *virkne_dati, size_t krājums_COUNT) { unsigned char *x_koordināta = mērķis_dati; const unsigned char *세로좌표 = virkne_dati; if (x_koordināta < 세로좌표) { for (size_t 순번 = 0; 순번 < krājums_COUNT; 순번++) x_koordināta[순번] = 세로좌표[순번]; } else { while (krājums_COUNT) { krājums_COUNT--; x_koordināta[krājums_COUNT] = 세로좌표[krājums_COUNT]; } } return mērķis_dati; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t krājums_COUNT) { while (krājums_COUNT--) { unsigned char x_koordināta = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (x_koordināta != 세로좌표) return (int)x_koordināta-세로좌표; if (!x_koordināta) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *virkne_dati, char **beigt_zvanu_Nobīde, int Fons_VALUE) {
    const char *Sākt_Nobīde = virkne_dati; unsigned long VALUE = 0; int kodēšana_VALUE = 1, 하나라도 = 0;
    while (*virkne_dati == ' ' || (*virkne_dati >= 9 && *virkne_dati <= 13)) virkne_dati++;
    if (*virkne_dati == '-' || *virkne_dati == '+') { if (*virkne_dati == '-') kodēšana_VALUE = -1; virkne_dati++; }
    if (Fons_VALUE == 0) Fons_VALUE = 10;
    while (*virkne_dati >= '0' && *virkne_dati <= '9' && *virkne_dati - '0' < Fons_VALUE) {
        unsigned cipars_VALUE = *virkne_dati++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - cipars_VALUE) / (unsigned)Fons_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * Fons_VALUE + cipars_VALUE;
    }
    if (beigt_zvanu_Nobīde) *beigt_zvanu_Nobīde = (char *)(하나라도 ? virkne_dati : Sākt_Nobīde); return kodēšana_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *virkne_dati) { return (int)strtol(virkne_dati, 0, 10); }

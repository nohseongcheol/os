#include "string.h"
size_t strlen(const char *tekenreeks_gegevens) { const char *gegevens_functie = tekenreeks_gegevens; while (*gegevens_functie) gegevens_functie++; return gegevens_functie - tekenreeks_gegevens; }
int memcmp(const void *첫째값, const void *SECONDE_WAARDE, size_t item_AANTAL) { const unsigned char *x_coördinaat = 첫째값, *Y_coördinaat = SECONDE_WAARDE; while (item_AANTAL--) { if (*x_coördinaat != *Y_coördinaat) return (int)*x_coördinaat - *Y_coördinaat; x_coördinaat++; Y_coördinaat++; } return 0; }
void *memmove(void *doel_gegevens, const void *tekenreeks_gegevens, size_t item_AANTAL) { unsigned char *x_coördinaat = doel_gegevens; const unsigned char *Y_coördinaat = tekenreeks_gegevens; if (x_coördinaat < Y_coördinaat) { for (size_t 순번 = 0; 순번 < item_AANTAL; 순번++) x_coördinaat[순번] = Y_coördinaat[순번]; } else { while (item_AANTAL) { item_AANTAL--; x_coördinaat[item_AANTAL] = Y_coördinaat[item_AANTAL]; } } return doel_gegevens; }
int strncmp(const char *첫째값, const char *SECONDE_WAARDE, size_t item_AANTAL) { while (item_AANTAL--) { unsigned char x_coördinaat = *첫째값++, Y_coördinaat = *SECONDE_WAARDE++; if (x_coördinaat != Y_coördinaat) return (int)x_coördinaat-Y_coördinaat; if (!x_coördinaat) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *tekenreeks_gegevens, char **beëindigen_VERSCHUIVING, int Achtergrond_WAARDE) {
    const char *START_VERSCHUIVING = tekenreeks_gegevens; unsigned long WAARDE = 0; int Encoding_WAARDE = 1, 하나라도 = 0;
    while (*tekenreeks_gegevens == ' ' || (*tekenreeks_gegevens >= 9 && *tekenreeks_gegevens <= 13)) tekenreeks_gegevens++;
    if (*tekenreeks_gegevens == '-' || *tekenreeks_gegevens == '+') { if (*tekenreeks_gegevens == '-') Encoding_WAARDE = -1; tekenreeks_gegevens++; }
    if (Achtergrond_WAARDE == 0) Achtergrond_WAARDE = 10;
    while (*tekenreeks_gegevens >= '0' && *tekenreeks_gegevens <= '9' && *tekenreeks_gegevens - '0' < Achtergrond_WAARDE) {
        unsigned cijfer_WAARDE = *tekenreeks_gegevens++ - '0'; 하나라도 = 1;
        if (WAARDE > (0x7ffffffffffffffful - cijfer_WAARDE) / (unsigned)Achtergrond_WAARDE) WAARDE = 0x7ffffffffffffffful;
        else WAARDE = WAARDE * Achtergrond_WAARDE + cijfer_WAARDE;
    }
    if (beëindigen_VERSCHUIVING) *beëindigen_VERSCHUIVING = (char *)(하나라도 ? tekenreeks_gegevens : START_VERSCHUIVING); return Encoding_WAARDE > 0 ? (long)WAARDE : -(long)WAARDE;
}
int atoi(const char *tekenreeks_gegevens) { return (int)strtol(tekenreeks_gegevens, 0, 10); }

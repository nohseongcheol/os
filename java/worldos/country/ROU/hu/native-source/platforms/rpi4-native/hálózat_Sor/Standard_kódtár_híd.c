#include "string.h"
size_t strlen(const char *sztring_adat) { const char *adat_pozíció = sztring_adat; while (*adat_pozíció) adat_pozíció++; return adat_pozíció - sztring_adat; }
int memcmp(const void *첫째값, const void *MPERC_ÉRTÉK, size_t cikk_DARAB) { const unsigned char *x_koordináta = 첫째값, *Y_koordináta = MPERC_ÉRTÉK; while (cikk_DARAB--) { if (*x_koordináta != *Y_koordináta) return (int)*x_koordináta - *Y_koordináta; x_koordináta++; Y_koordináta++; } return 0; }
void *memmove(void *cél_adat, const void *sztring_adat, size_t cikk_DARAB) { unsigned char *x_koordináta = cél_adat; const unsigned char *Y_koordináta = sztring_adat; if (x_koordináta < Y_koordináta) { for (size_t 순번 = 0; 순번 < cikk_DARAB; 순번++) x_koordináta[순번] = Y_koordináta[순번]; } else { while (cikk_DARAB) { cikk_DARAB--; x_koordináta[cikk_DARAB] = Y_koordináta[cikk_DARAB]; } } return cél_adat; }
int strncmp(const char *첫째값, const char *MPERC_ÉRTÉK, size_t cikk_DARAB) { while (cikk_DARAB--) { unsigned char x_koordináta = *첫째값++, Y_koordináta = *MPERC_ÉRTÉK++; if (x_koordináta != Y_koordináta) return (int)x_koordináta-Y_koordináta; if (!x_koordináta) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *sztring_adat, char **megszüntet_Ofszet, int Háttér_ÉRTÉK) {
    const char *START_Ofszet = sztring_adat; unsigned long ÉRTÉK = 0; int kódolás_ÉRTÉK = 1, 하나라도 = 0;
    while (*sztring_adat == ' ' || (*sztring_adat >= 9 && *sztring_adat <= 13)) sztring_adat++;
    if (*sztring_adat == '-' || *sztring_adat == '+') { if (*sztring_adat == '-') kódolás_ÉRTÉK = -1; sztring_adat++; }
    if (Háttér_ÉRTÉK == 0) Háttér_ÉRTÉK = 10;
    while (*sztring_adat >= '0' && *sztring_adat <= '9' && *sztring_adat - '0' < Háttér_ÉRTÉK) {
        unsigned számjegy_ÉRTÉK = *sztring_adat++ - '0'; 하나라도 = 1;
        if (ÉRTÉK > (0x7ffffffffffffffful - számjegy_ÉRTÉK) / (unsigned)Háttér_ÉRTÉK) ÉRTÉK = 0x7ffffffffffffffful;
        else ÉRTÉK = ÉRTÉK * Háttér_ÉRTÉK + számjegy_ÉRTÉK;
    }
    if (megszüntet_Ofszet) *megszüntet_Ofszet = (char *)(하나라도 ? sztring_adat : START_Ofszet); return kódolás_ÉRTÉK > 0 ? (long)ÉRTÉK : -(long)ÉRTÉK;
}
int atoi(const char *sztring_adat) { return (int)strtol(sztring_adat, 0, 10); }

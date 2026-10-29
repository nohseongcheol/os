#include "string.h"
size_t strlen(const char *ciąg_dane) { const char *dane_stanowisko = ciąg_dane; while (*dane_stanowisko) dane_stanowisko++; return dane_stanowisko - ciąg_dane; }
int memcmp(const void *첫째값, const void *SEKUNDA_WARTOŚĆ, size_t towar_ILE_LICZB) { const unsigned char *współrzędna_X = 첫째값, *Y_współrzędna = SEKUNDA_WARTOŚĆ; while (towar_ILE_LICZB--) { if (*współrzędna_X != *Y_współrzędna) return (int)*współrzędna_X - *Y_współrzędna; współrzędna_X++; Y_współrzędna++; } return 0; }
void *memmove(void *cel_dane, const void *ciąg_dane, size_t towar_ILE_LICZB) { unsigned char *współrzędna_X = cel_dane; const unsigned char *Y_współrzędna = ciąg_dane; if (współrzędna_X < Y_współrzędna) { for (size_t 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) współrzędna_X[순번] = Y_współrzędna[순번]; } else { while (towar_ILE_LICZB) { towar_ILE_LICZB--; współrzędna_X[towar_ILE_LICZB] = Y_współrzędna[towar_ILE_LICZB]; } } return cel_dane; }
int strncmp(const char *첫째값, const char *SEKUNDA_WARTOŚĆ, size_t towar_ILE_LICZB) { while (towar_ILE_LICZB--) { unsigned char współrzędna_X = *첫째값++, Y_współrzędna = *SEKUNDA_WARTOŚĆ++; if (współrzędna_X != Y_współrzędna) return (int)współrzędna_X-Y_współrzędna; if (!współrzędna_X) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *ciąg_dane, char **Koniec_przesunąć, int Tło_WARTOŚĆ) {
    const char *START_przesunąć = ciąg_dane; unsigned long WARTOŚĆ = 0; int Encoding_WARTOŚĆ = 1, 하나라도 = 0;
    while (*ciąg_dane == ' ' || (*ciąg_dane >= 9 && *ciąg_dane <= 13)) ciąg_dane++;
    if (*ciąg_dane == '-' || *ciąg_dane == '+') { if (*ciąg_dane == '-') Encoding_WARTOŚĆ = -1; ciąg_dane++; }
    if (Tło_WARTOŚĆ == 0) Tło_WARTOŚĆ = 10;
    while (*ciąg_dane >= '0' && *ciąg_dane <= '9' && *ciąg_dane - '0' < Tło_WARTOŚĆ) {
        unsigned cyfra_WARTOŚĆ = *ciąg_dane++ - '0'; 하나라도 = 1;
        if (WARTOŚĆ > (0x7ffffffffffffffful - cyfra_WARTOŚĆ) / (unsigned)Tło_WARTOŚĆ) WARTOŚĆ = 0x7ffffffffffffffful;
        else WARTOŚĆ = WARTOŚĆ * Tło_WARTOŚĆ + cyfra_WARTOŚĆ;
    }
    if (Koniec_przesunąć) *Koniec_przesunąć = (char *)(하나라도 ? ciąg_dane : START_przesunąć); return Encoding_WARTOŚĆ > 0 ? (long)WARTOŚĆ : -(long)WARTOŚĆ;
}
int atoi(const char *ciąg_dane) { return (int)strtol(ciąg_dane, 0, 10); }

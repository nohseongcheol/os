#include "string.h"
size_t strlen(const char *kate_datuak) { const char *datuak_kargu = kate_datuak; while (*datuak_kargu) datuak_kargu++; return datuak_kargu - kate_datuak; }
int memcmp(const void *첫째값, const void *SEGUNDOA_balio, size_t elementu_ZENBATU) { const unsigned char *X_koordenatu = 첫째값, *Y_koordenatu = SEGUNDOA_balio; while (elementu_ZENBATU--) { if (*X_koordenatu != *Y_koordenatu) return (int)*X_koordenatu - *Y_koordenatu; X_koordenatu++; Y_koordenatu++; } return 0; }
void *memmove(void *helburu_datuak, const void *kate_datuak, size_t elementu_ZENBATU) { unsigned char *X_koordenatu = helburu_datuak; const unsigned char *Y_koordenatu = kate_datuak; if (X_koordenatu < Y_koordenatu) { for (size_t 순번 = 0; 순번 < elementu_ZENBATU; 순번++) X_koordenatu[순번] = Y_koordenatu[순번]; } else { while (elementu_ZENBATU) { elementu_ZENBATU--; X_koordenatu[elementu_ZENBATU] = Y_koordenatu[elementu_ZENBATU]; } } return helburu_datuak; }
int strncmp(const char *첫째값, const char *SEGUNDOA_balio, size_t elementu_ZENBATU) { while (elementu_ZENBATU--) { unsigned char X_koordenatu = *첫째값++, Y_koordenatu = *SEGUNDOA_balio++; if (X_koordenatu != Y_koordenatu) return (int)X_koordenatu-Y_koordenatu; if (!X_koordenatu) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *kate_datuak, char **amaitu_Geruzak, int horma_paper_balio) {
    const char *HASI_Geruzak = kate_datuak; unsigned long balio = 0; int kodeketa_balio = 1, 하나라도 = 0;
    while (*kate_datuak == ' ' || (*kate_datuak >= 9 && *kate_datuak <= 13)) kate_datuak++;
    if (*kate_datuak == '-' || *kate_datuak == '+') { if (*kate_datuak == '-') kodeketa_balio = -1; kate_datuak++; }
    if (horma_paper_balio == 0) horma_paper_balio = 10;
    while (*kate_datuak >= '0' && *kate_datuak <= '9' && *kate_datuak - '0' < horma_paper_balio) {
        unsigned digitu_balio = *kate_datuak++ - '0'; 하나라도 = 1;
        if (balio > (0x7ffffffffffffffful - digitu_balio) / (unsigned)horma_paper_balio) balio = 0x7ffffffffffffffful;
        else balio = balio * horma_paper_balio + digitu_balio;
    }
    if (amaitu_Geruzak) *amaitu_Geruzak = (char *)(하나라도 ? kate_datuak : HASI_Geruzak); return kodeketa_balio > 0 ? (long)balio : -(long)balio;
}
int atoi(const char *kate_datuak) { return (int)strtol(kate_datuak, 0, 10); }

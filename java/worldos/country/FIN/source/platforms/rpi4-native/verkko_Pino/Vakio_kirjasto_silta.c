#include "string.h"
size_t strlen(const char *merkkijono_data) { const char *data_toimi = merkkijono_data; while (*data_toimi) data_toimi++; return data_toimi - merkkijono_data; }
int memcmp(const void *첫째값, const void *SEKUNNIT_ARVO, size_t kohde_LASKE) { const unsigned char *x_koordinaatti = 첫째값, *Y_koordinaatti = SEKUNNIT_ARVO; while (kohde_LASKE--) { if (*x_koordinaatti != *Y_koordinaatti) return (int)*x_koordinaatti - *Y_koordinaatti; x_koordinaatti++; Y_koordinaatti++; } return 0; }
void *memmove(void *kohde_data, const void *merkkijono_data, size_t kohde_LASKE) { unsigned char *x_koordinaatti = kohde_data; const unsigned char *Y_koordinaatti = merkkijono_data; if (x_koordinaatti < Y_koordinaatti) { for (size_t 순번 = 0; 순번 < kohde_LASKE; 순번++) x_koordinaatti[순번] = Y_koordinaatti[순번]; } else { while (kohde_LASKE) { kohde_LASKE--; x_koordinaatti[kohde_LASKE] = Y_koordinaatti[kohde_LASKE]; } } return kohde_data; }
int strncmp(const char *첫째값, const char *SEKUNNIT_ARVO, size_t kohde_LASKE) { while (kohde_LASKE--) { unsigned char x_koordinaatti = *첫째값++, Y_koordinaatti = *SEKUNNIT_ARVO++; if (x_koordinaatti != Y_koordinaatti) return (int)x_koordinaatti-Y_koordinaatti; if (!x_koordinaatti) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *merkkijono_data, char **lopettaa_puhelu_SIIRTYMÄ, int Tausta_ARVO) {
    const char *alku_SIIRTYMÄ = merkkijono_data; unsigned long ARVO = 0; int koodaus_ARVO = 1, 하나라도 = 0;
    while (*merkkijono_data == ' ' || (*merkkijono_data >= 9 && *merkkijono_data <= 13)) merkkijono_data++;
    if (*merkkijono_data == '-' || *merkkijono_data == '+') { if (*merkkijono_data == '-') koodaus_ARVO = -1; merkkijono_data++; }
    if (Tausta_ARVO == 0) Tausta_ARVO = 10;
    while (*merkkijono_data >= '0' && *merkkijono_data <= '9' && *merkkijono_data - '0' < Tausta_ARVO) {
        unsigned numero_ARVO = *merkkijono_data++ - '0'; 하나라도 = 1;
        if (ARVO > (0x7ffffffffffffffful - numero_ARVO) / (unsigned)Tausta_ARVO) ARVO = 0x7ffffffffffffffful;
        else ARVO = ARVO * Tausta_ARVO + numero_ARVO;
    }
    if (lopettaa_puhelu_SIIRTYMÄ) *lopettaa_puhelu_SIIRTYMÄ = (char *)(하나라도 ? merkkijono_data : alku_SIIRTYMÄ); return koodaus_ARVO > 0 ? (long)ARVO : -(long)ARVO;
}
int atoi(const char *merkkijono_data) { return (int)strtol(merkkijono_data, 0, 10); }

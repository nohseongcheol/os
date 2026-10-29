#include "string.h"
size_t strlen(const char *Zare_Tarin_bayani) { const char *자료위치 = Zare_Tarin_bayani; while (*자료위치) 자료위치++; return 자료위치 - Zare_Tarin_bayani; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *gamayyar_x = 첫째값, *Maɓallin_Y_Mai_tsarawa = 둘째값; while (개수--) { if (*gamayyar_x != *Maɓallin_Y_Mai_tsarawa) return (int)*gamayyar_x - *Maɓallin_Y_Mai_tsarawa; gamayyar_x++; Maɓallin_Y_Mai_tsarawa++; } return 0; }
void *memmove(void *Zangon_ƙarshe_Tarin_bayani, const void *Zare_Tarin_bayani, size_t 개수) { unsigned char *gamayyar_x = Zangon_ƙarshe_Tarin_bayani; const unsigned char *Maɓallin_Y_Mai_tsarawa = Zare_Tarin_bayani; if (gamayyar_x < Maɓallin_Y_Mai_tsarawa) { for (size_t 순번 = 0; 순번 < 개수; 순번++) gamayyar_x[순번] = Maɓallin_Y_Mai_tsarawa[순번]; } else { while (개수) { 개수--; gamayyar_x[개수] = Maɓallin_Y_Mai_tsarawa[개수]; } } return Zangon_ƙarshe_Tarin_bayani; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char gamayyar_x = *첫째값++, Maɓallin_Y_Mai_tsarawa = *둘째값++; if (gamayyar_x != Maɓallin_Y_Mai_tsarawa) return (int)gamayyar_x-Maɓallin_Y_Mai_tsarawa; if (!gamayyar_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *Zare_Tarin_bayani, char **Ƙarshe_Sassautawa, int Bi_bango_Daraja) {
    const char *Fara_Sassautawa = Zare_Tarin_bayani; unsigned long Daraja = 0; int Juyar_da_bayanai_zuwa_lamba_Daraja = 1, 하나라도 = 0;
    while (*Zare_Tarin_bayani == ' ' || (*Zare_Tarin_bayani >= 9 && *Zare_Tarin_bayani <= 13)) Zare_Tarin_bayani++;
    if (*Zare_Tarin_bayani == '-' || *Zare_Tarin_bayani == '+') { if (*Zare_Tarin_bayani == '-') Juyar_da_bayanai_zuwa_lamba_Daraja = -1; Zare_Tarin_bayani++; }
    if (Bi_bango_Daraja == 0) Bi_bango_Daraja = 10;
    while (*Zare_Tarin_bayani >= '0' && *Zare_Tarin_bayani <= '9' && *Zare_Tarin_bayani - '0' < Bi_bango_Daraja) {
        unsigned lamba_Daraja = *Zare_Tarin_bayani++ - '0'; 하나라도 = 1;
        if (Daraja > (0x7ffffffffffffffful - lamba_Daraja) / (unsigned)Bi_bango_Daraja) Daraja = 0x7ffffffffffffffful;
        else Daraja = Daraja * Bi_bango_Daraja + lamba_Daraja;
    }
    if (Ƙarshe_Sassautawa) *Ƙarshe_Sassautawa = (char *)(하나라도 ? Zare_Tarin_bayani : Fara_Sassautawa); return Juyar_da_bayanai_zuwa_lamba_Daraja > 0 ? (long)Daraja : -(long)Daraja;
}
int atoi(const char *Zare_Tarin_bayani) { return (int)strtol(Zare_Tarin_bayani, 0, 10); }

#include "string.h"
size_t strlen(const char *տող_տվյալ) { const char *տվյալ_դիրք = տող_տվյալ; while (*տվյալ_դիրք) տվյալ_դիրք++; return տվյալ_դիրք - տող_տվյալ; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *x_կոորդինատ = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*x_կոորդինատ != *세로좌표) return (int)*x_կոորդինատ - *세로좌표; x_կոորդինատ++; 세로좌표++; } return 0; }
void *memmove(void *նպատակակետ_տվյալ, const void *տող_տվյալ, size_t 개수) { unsigned char *x_կոորդինատ = նպատակակետ_տվյալ; const unsigned char *세로좌표 = տող_տվյալ; if (x_կոորդինատ < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) x_կոորդինատ[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; x_կոորդինատ[개수] = 세로좌표[개수]; } } return նպատակակետ_տվյալ; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char x_կոորդինատ = *첫째값++, 세로좌표 = *둘째값++; if (x_կոորդինատ != 세로좌표) return (int)x_կոորդինատ-세로좌표; if (!x_կոորդինատ) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *տող_տվյալ, char **վերջացնել_Տեղաշարժում, int խորք_արժեք) {
    const char *Մեկնարկ_Տեղաշարժում = տող_տվյալ; unsigned long արժեք = 0; int կոդավորում_արժեք = 1, 하나라도 = 0;
    while (*տող_տվյալ == ' ' || (*տող_տվյալ >= 9 && *տող_տվյալ <= 13)) տող_տվյալ++;
    if (*տող_տվյալ == '-' || *տող_տվյալ == '+') { if (*տող_տվյալ == '-') կոդավորում_արժեք = -1; տող_տվյալ++; }
    if (խորք_արժեք == 0) խորք_արժեք = 10;
    while (*տող_տվյալ >= '0' && *տող_տվյալ <= '9' && *տող_տվյալ - '0' < խորք_արժեք) {
        unsigned թվանշան_արժեք = *տող_տվյալ++ - '0'; 하나라도 = 1;
        if (արժեք > (0x7ffffffffffffffful - թվանշան_արժեք) / (unsigned)խորք_արժեք) արժեք = 0x7ffffffffffffffful;
        else արժեք = արժեք * խորք_արժեք + թվանշան_արժեք;
    }
    if (վերջացնել_Տեղաշարժում) *վերջացնել_Տեղաշարժում = (char *)(하나라도 ? տող_տվյալ : Մեկնարկ_Տեղաշարժում); return կոդավորում_արժեք > 0 ? (long)արժեք : -(long)արժեք;
}
int atoi(const char *տող_տվյալ) { return (int)strtol(տող_տվյալ, 0, 10); }

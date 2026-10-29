#include "string.h"
size_t strlen(const char *molokoloko_data) { const char *자료위치 = molokoloko_data; while (*자료위치) 자료위치++; return 자료위치 - molokoloko_data; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *kamano_ya_x = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*kamano_ya_x != *세로좌표) return (int)*kamano_ya_x - *세로좌표; kamano_ya_x++; 세로좌표++; } return 0; }
void *memmove(void *boyo_data, const void *molokoloko_data, size_t 개수) { unsigned char *kamano_ya_x = boyo_data; const unsigned char *세로좌표 = molokoloko_data; if (kamano_ya_x < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) kamano_ya_x[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; kamano_ya_x[개수] = 세로좌표[개수]; } } return boyo_data; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char kamano_ya_x = *첫째값++, 세로좌표 = *둘째값++; if (kamano_ya_x != 세로좌표) return (int)kamano_ya_x-세로좌표; if (!kamano_ya_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *molokoloko_data, char **fetša_E_Šetšego, int Bokamorago_boleng) {
    const char *Thomišo_E_Šetšego = molokoloko_data; unsigned long boleng = 0; int go_enkhouta_boleng = 1, 하나라도 = 0;
    while (*molokoloko_data == ' ' || (*molokoloko_data >= 9 && *molokoloko_data <= 13)) molokoloko_data++;
    if (*molokoloko_data == '-' || *molokoloko_data == '+') { if (*molokoloko_data == '-') go_enkhouta_boleng = -1; molokoloko_data++; }
    if (Bokamorago_boleng == 0) Bokamorago_boleng = 10;
    while (*molokoloko_data >= '0' && *molokoloko_data <= '9' && *molokoloko_data - '0' < Bokamorago_boleng) {
        unsigned 숫자 = *molokoloko_data++ - '0'; 하나라도 = 1;
        if (boleng > (0x7ffffffffffffffful - 숫자) / (unsigned)Bokamorago_boleng) boleng = 0x7ffffffffffffffful;
        else boleng = boleng * Bokamorago_boleng + 숫자;
    }
    if (fetša_E_Šetšego) *fetša_E_Šetšego = (char *)(하나라도 ? molokoloko_data : Thomišo_E_Šetšego); return go_enkhouta_boleng > 0 ? (long)boleng : -(long)boleng;
}
int atoi(const char *molokoloko_data) { return (int)strtol(molokoloko_data, 0, 10); }

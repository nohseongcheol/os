#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *molokoloko_boleng) { size_t botelele_boleng = 0; while (molokoloko_boleng[botelele_boleng]) botelele_boleng++; return botelele_boleng; }
int strcmp(const char *앞, const char *Morago_boleng) {
    while (*앞 && *앞 == *Morago_boleng) { 앞++; Morago_boleng++; }
    return (unsigned char)*앞 - (unsigned char)*Morago_boleng;
}
int memcmp(const void *앞, const void *Morago_boleng, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Morago_boleng;
    for (size_t sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 바이트수; sekgobana_go_tsenya_tshedimošo++) if (가[sekgobana_go_tsenya_tshedimošo] != 나[sekgobana_go_tsenya_tshedimošo]) return 가[sekgobana_go_tsenya_tshedimošo] - 나[sekgobana_go_tsenya_tshedimošo];
    return 0;
}
void *memcpy(void *boyo_boleng, const void *원본, size_t 바이트수) {
    unsigned char *가 = boyo_boleng; const unsigned char *나 = 원본;
    for (size_t sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 바이트수; sekgobana_go_tsenya_tshedimošo++) 가[sekgobana_go_tsenya_tshedimošo] = 나[sekgobana_go_tsenya_tshedimošo];
    return boyo_boleng;
}
void *memset(void *boyo_boleng, int boleng, size_t 바이트수) {
    unsigned char *data = boyo_boleng;
    for (size_t sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 바이트수; sekgobana_go_tsenya_tshedimošo++) data[sekgobana_go_tsenya_tshedimošo] = boleng;
    return boyo_boleng;
}
int putchar(int 문자) { unsigned char boleng = 문자; return write(1, &boleng, 1) == 1 ? boleng : EOF; }
int puts(const char *molokoloko_boleng) {
    size_t botelele_boleng = strlen(molokoloko_boleng), 위치 = 0;
    while (위치 < botelele_boleng) { ssize_t 결과 = write(1, molokoloko_boleng + 위치, botelele_boleng - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

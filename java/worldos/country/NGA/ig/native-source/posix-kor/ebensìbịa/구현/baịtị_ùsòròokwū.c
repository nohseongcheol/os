#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ùsòròokwū_valuu) { size_t ogologo_valuu = 0; while (ùsòròokwū_valuu[ogologo_valuu]) ogologo_valuu++; return ogologo_valuu; }
int strcmp(const char *앞, const char *Àzụ_valuu) {
    while (*앞 && *앞 == *Àzụ_valuu) { 앞++; Àzụ_valuu++; }
    return (unsigned char)*앞 - (unsigned char)*Àzụ_valuu;
}
int memcmp(const void *앞, const void *Àzụ_valuu, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Àzụ_valuu;
    for (size_t oghere_ndebà = 0; oghere_ndebà < 바이트수; oghere_ndebà++) if (가[oghere_ndebà] != 나[oghere_ndebà]) return 가[oghere_ndebà] - 나[oghere_ndebà];
    return 0;
}
void *memcpy(void *ebemwèga_valuu, const void *원본, size_t 바이트수) {
    unsigned char *가 = ebemwèga_valuu; const unsigned char *나 = 원본;
    for (size_t oghere_ndebà = 0; oghere_ndebà < 바이트수; oghere_ndebà++) 가[oghere_ndebà] = 나[oghere_ndebà];
    return ebemwèga_valuu;
}
void *memset(void *ebemwèga_valuu, int valuu, size_t 바이트수) {
    unsigned char *datà = ebemwèga_valuu;
    for (size_t oghere_ndebà = 0; oghere_ndebà < 바이트수; oghere_ndebà++) datà[oghere_ndebà] = valuu;
    return ebemwèga_valuu;
}
int putchar(int 문자) { unsigned char valuu = 문자; return write(1, &valuu, 1) == 1 ? valuu : EOF; }
int puts(const char *ùsòròokwū_valuu) {
    size_t ogologo_valuu = strlen(ùsòròokwū_valuu), 위치 = 0;
    while (위치 < ogologo_valuu) { ssize_t 결과 = write(1, ùsòròokwū_valuu + 위치, ogologo_valuu - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

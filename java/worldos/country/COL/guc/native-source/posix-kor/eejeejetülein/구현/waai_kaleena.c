#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *kaleena_ajutuu) { size_t akaliaa_ajutuu = 0; while (kaleena_ajutuu[akaliaa_ajutuu]) akaliaa_ajutuu++; return akaliaa_ajutuu; }
int strcmp(const char *앞, const char *뒤) {
    while (*앞 && *앞 == *뒤) { 앞++; 뒤++; }
    return (unsigned char)*앞 - (unsigned char)*뒤;
}
int memcmp(const void *앞, const void *뒤, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = 뒤;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *jalamüinjatü_ajutuu, const void *원본, size_t 바이트수) {
    unsigned char *가 = jalamüinjatü_ajutuu; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return jalamüinjatü_ajutuu;
}
void *memset(void *jalamüinjatü_ajutuu, int ajutuu, size_t 바이트수) {
    unsigned char *atijaaya = jalamüinjatü_ajutuu;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) atijaaya[칸] = ajutuu;
    return jalamüinjatü_ajutuu;
}
int putchar(int 문자) { unsigned char ajutuu = 문자; return write(1, &ajutuu, 1) == 1 ? ajutuu : EOF; }
int puts(const char *kaleena_ajutuu) {
    size_t akaliaa_ajutuu = strlen(kaleena_ajutuu), 위치 = 0;
    while (위치 < akaliaa_ajutuu) { ssize_t 결과 = write(1, kaleena_ajutuu + 위치, akaliaa_ajutuu - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

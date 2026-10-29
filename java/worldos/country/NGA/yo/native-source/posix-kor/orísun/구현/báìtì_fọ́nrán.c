#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *fọ́nrán_iye) { size_t gígùn_iye = 0; while (fọ́nrán_iye[gígùn_iye]) gígùn_iye++; return gígùn_iye; }
int strcmp(const char *앞, const char *Padà_sẹ́yìn_iye) {
    while (*앞 && *앞 == *Padà_sẹ́yìn_iye) { 앞++; Padà_sẹ́yìn_iye++; }
    return (unsigned char)*앞 - (unsigned char)*Padà_sẹ́yìn_iye;
}
int memcmp(const void *앞, const void *Padà_sẹ́yìn_iye, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Padà_sẹ́yìn_iye;
    for (size_t ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 바이트수; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (가[ààyè_ìfàyọkàsí_ìgbéwọlé] != 나[ààyè_ìfàyọkàsí_ìgbéwọlé]) return 가[ààyè_ìfàyọkàsí_ìgbéwọlé] - 나[ààyè_ìfàyọkàsí_ìgbéwọlé];
    return 0;
}
void *memcpy(void *èbúté_iye, const void *원본, size_t 바이트수) {
    unsigned char *가 = èbúté_iye; const unsigned char *나 = 원본;
    for (size_t ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 바이트수; ààyè_ìfàyọkàsí_ìgbéwọlé++) 가[ààyè_ìfàyọkàsí_ìgbéwọlé] = 나[ààyè_ìfàyọkàsí_ìgbéwọlé];
    return èbúté_iye;
}
void *memset(void *èbúté_iye, int iye, size_t 바이트수) {
    unsigned char *détà = èbúté_iye;
    for (size_t ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 바이트수; ààyè_ìfàyọkàsí_ìgbéwọlé++) détà[ààyè_ìfàyọkàsí_ìgbéwọlé] = iye;
    return èbúté_iye;
}
int putchar(int 문자) { unsigned char iye = 문자; return write(1, &iye, 1) == 1 ? iye : EOF; }
int puts(const char *fọ́nrán_iye) {
    size_t gígùn_iye = strlen(fọ́nrán_iye), 위치 = 0;
    while (위치 < gígùn_iye) { ssize_t 결과 = write(1, fọ́nrán_iye + 위치, gígùn_iye - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

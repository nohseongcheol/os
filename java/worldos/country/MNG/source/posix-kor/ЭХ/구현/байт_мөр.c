#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *мөр_утга_6ca8363c) { size_t урт_утга = 0; while (мөр_утга_6ca8363c[урт_утга]) урт_утга++; return урт_утга; }
int strcmp(const char *앞, const char *Буцах_утга) {
    while (*앞 && *앞 == *Буцах_утга) { 앞++; Буцах_утга++; }
    return (unsigned char)*앞 - (unsigned char)*Буцах_утга;
}
int memcmp(const void *앞, const void *Буцах_утга, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Буцах_утга;
    for (size_t зай_оролт = 0; зай_оролт < 바이트수; зай_оролт++) if (가[зай_оролт] != 나[зай_оролт]) return 가[зай_оролт] - 나[зай_оролт];
    return 0;
}
void *memcpy(void *товлосон_газар_утга, const void *원본, size_t 바이트수) {
    unsigned char *가 = товлосон_газар_утга; const unsigned char *나 = 원본;
    for (size_t зай_оролт = 0; зай_оролт < 바이트수; зай_оролт++) 가[зай_оролт] = 나[зай_оролт];
    return товлосон_газар_утга;
}
void *memset(void *товлосон_газар_утга, int утга, size_t 바이트수) {
    unsigned char *өгөгдөл = товлосон_газар_утга;
    for (size_t зай_оролт = 0; зай_оролт < 바이트수; зай_оролт++) өгөгдөл[зай_оролт] = утга;
    return товлосон_газар_утга;
}
int putchar(int 문자) { unsigned char утга = 문자; return write(1, &утга, 1) == 1 ? утга : EOF; }
int puts(const char *мөр_утга_6ca8363c) {
    size_t урт_утга = strlen(мөр_утга_6ca8363c), 위치 = 0;
    while (위치 < урт_утга) { ssize_t 결과 = write(1, мөр_утга_6ca8363c + 위치, урт_утга - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

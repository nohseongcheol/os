#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *સ્ટ્રિંગ_મૂલ્ય) { size_t લંબાઈ_મૂલ્ય = 0; while (સ્ટ્રિંગ_મૂલ્ય[લંબાઈ_મૂલ્ય]) લંબાઈ_મૂલ્ય++; return લંબાઈ_મૂલ્ય; }
int strcmp(const char *앞, const char *બેક_મૂલ્ય) {
    while (*앞 && *앞 == *બેક_મૂલ્ય) { 앞++; બેક_મૂલ્ય++; }
    return (unsigned char)*앞 - (unsigned char)*બેક_મૂલ્ય;
}
int memcmp(const void *앞, const void *બેક_મૂલ્ય, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = બેક_મૂલ્ય;
    for (size_t સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < 바이트수; સ્લૉટ_પ્રવેશ++) if (가[સ્લૉટ_પ્રવેશ] != 나[સ્લૉટ_પ્રવેશ]) return 가[સ્લૉટ_પ્રવેશ] - 나[સ્લૉટ_પ્રવેશ];
    return 0;
}
void *memcpy(void *ગંતવ્ય_મૂલ્ય, const void *원본, size_t 바이트수) {
    unsigned char *가 = ગંતવ્ય_મૂલ્ય; const unsigned char *나 = 원본;
    for (size_t સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < 바이트수; સ્લૉટ_પ્રવેશ++) 가[સ્લૉટ_પ્રવેશ] = 나[સ્લૉટ_પ્રવેશ];
    return ગંતવ્ય_મૂલ્ય;
}
void *memset(void *ગંતવ્ય_મૂલ્ય, int મૂલ્ય, size_t 바이트수) {
    unsigned char *ડેટા = ગંતવ્ય_મૂલ્ય;
    for (size_t સ્લૉટ_પ્રવેશ = 0; સ્લૉટ_પ્રવેશ < 바이트수; સ્લૉટ_પ્રવેશ++) ડેટા[સ્લૉટ_પ્રવેશ] = મૂલ્ય;
    return ગંતવ્ય_મૂલ્ય;
}
int putchar(int 문자) { unsigned char મૂલ્ય = 문자; return write(1, &મૂલ્ય, 1) == 1 ? મૂલ્ય : EOF; }
int puts(const char *સ્ટ્રિંગ_મૂલ્ય) {
    size_t લંબાઈ_મૂલ્ય = strlen(સ્ટ્રિંગ_મૂલ્ય), સ્થાન = 0;
    while (સ્થાન < લંબાઈ_મૂલ્ય) { ssize_t પરિમાણ = write(1, સ્ટ્રિંગ_મૂલ્ય + સ્થાન, લંબાઈ_મૂલ્ય - સ્થાન); if (પરિમાણ <= 0) return EOF; સ્થાન += પરિમાણ; }
    return putchar('\n') == EOF ? EOF : 0;
}

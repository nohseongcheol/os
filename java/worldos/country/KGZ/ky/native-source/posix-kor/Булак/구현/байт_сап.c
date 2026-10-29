#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *сап_маани) { size_t узундук_маани = 0; while (сап_маани[узундук_маани]) узундук_маани++; return узундук_маани; }
int strcmp(const char *앞, const char *Артка_маани) {
    while (*앞 && *앞 == *Артка_маани) { 앞++; Артка_маани++; }
    return (unsigned char)*앞 - (unsigned char)*Артка_маани;
}
int memcmp(const void *앞, const void *Артка_маани, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Артка_маани;
    for (size_t оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < 바이트수; оюкча_киргизме_жазуу++) if (가[оюкча_киргизме_жазуу] != 나[оюкча_киргизме_жазуу]) return 가[оюкча_киргизме_жазуу] - 나[оюкча_киргизме_жазуу];
    return 0;
}
void *memcpy(void *көздөө_жайы_маани, const void *원본, size_t 바이트수) {
    unsigned char *가 = көздөө_жайы_маани; const unsigned char *나 = 원본;
    for (size_t оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < 바이트수; оюкча_киргизме_жазуу++) 가[оюкча_киргизме_жазуу] = 나[оюкча_киргизме_жазуу];
    return көздөө_жайы_маани;
}
void *memset(void *көздөө_жайы_маани, int маани, size_t 바이트수) {
    unsigned char *берилмелер = көздөө_жайы_маани;
    for (size_t оюкча_киргизме_жазуу = 0; оюкча_киргизме_жазуу < 바이트수; оюкча_киргизме_жазуу++) берилмелер[оюкча_киргизме_жазуу] = маани;
    return көздөө_жайы_маани;
}
int putchar(int 문자) { unsigned char маани = 문자; return write(1, &маани, 1) == 1 ? маани : EOF; }
int puts(const char *сап_маани) {
    size_t узундук_маани = strlen(сап_маани), Турган_жери = 0;
    while (Турган_жери < узундук_маани) { ssize_t 결과 = write(1, сап_маани + Турган_жери, узундук_маани - Турган_жери); if (결과 <= 0) return EOF; Турган_жери += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

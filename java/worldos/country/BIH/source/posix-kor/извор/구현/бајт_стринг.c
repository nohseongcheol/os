#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *стринг_вриједност) { size_t дужина_вриједност = 0; while (стринг_вриједност[дужина_вриједност]) дужина_вриједност++; return дужина_вриједност; }
int strcmp(const char *앞, const char *Назад_вриједност) {
    while (*앞 && *앞 == *Назад_вриједност) { 앞++; Назад_вриједност++; }
    return (unsigned char)*앞 - (unsigned char)*Назад_вриједност;
}
int memcmp(const void *앞, const void *Назад_вриједност, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Назад_вриједност;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *одредиште_вриједност, const void *원본, size_t 바이트수) {
    unsigned char *가 = одредиште_вриједност; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return одредиште_вриједност;
}
void *memset(void *одредиште_вриједност, int вриједност, size_t 바이트수) {
    unsigned char *подаци = одредиште_вриједност;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) подаци[칸] = вриједност;
    return одредиште_вриједност;
}
int putchar(int 문자) { unsigned char вриједност = 문자; return write(1, &вриједност, 1) == 1 ? вриједност : EOF; }
int puts(const char *стринг_вриједност) {
    size_t дужина_вриједност = strlen(стринг_вриједност), 위치 = 0;
    while (위치 < дужина_вриједност) { ssize_t 결과 = write(1, стринг_вриједност + 위치, дужина_вриједност - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

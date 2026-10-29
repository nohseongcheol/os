#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *문자열) { size_t 길이 = 0; while (문자열[길이]) 길이++; return 길이; }
int strcmp(const char *앞, const char *뒤) {
    while (*앞 && *앞 == *뒤) { 앞++; 뒤++; }
    return (unsigned char)*앞 - (unsigned char)*뒤;
}
int memcmp(const void *앞, const void *뒤, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = 뒤;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *목적, const void *원본, size_t 바이트수) {
    unsigned char *가 = 목적; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return 목적;
}
void *memset(void *목적, int 값, size_t 바이트수) {
    unsigned char *자료 = 목적;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 자료[칸] = 값;
    return 목적;
}
int putchar(int 문자) { unsigned char 값 = 문자; return write(1, &값, 1) == 1 ? 값 : EOF; }
int puts(const char *문자열) {
    size_t 길이 = strlen(문자열), Положај = 0;
    while (Положај < 길이) { ssize_t ИСХОД = write(1, 문자열 + Положај, 길이 - Положај); if (ИСХОД <= 0) return EOF; Положај += ИСХОД; }
    return putchar('\n') == EOF ? EOF : 0;
}

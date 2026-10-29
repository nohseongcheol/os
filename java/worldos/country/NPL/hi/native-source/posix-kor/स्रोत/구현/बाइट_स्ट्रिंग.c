#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *स्ट्रिंग_मान) { size_t 길이 = 0; while (स्ट्रिंग_मान[길이]) 길이++; return 길이; }
int strcmp(const char *सामने_मान, const char *वापस_मान) {
    while (*सामने_मान && *सामने_मान == *वापस_मान) { सामने_मान++; वापस_मान++; }
    return (unsigned char)*सामने_मान - (unsigned char)*वापस_मान;
}
int memcmp(const void *सामने_मान, const void *वापस_मान, size_t 바이트수) {
    const unsigned char *가 = सामने_मान, *나 = वापस_मान;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *गंतव्य_मान, const void *원본, size_t 바이트수) {
    unsigned char *가 = गंतव्य_मान; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return गंतव्य_मान;
}
void *memset(void *गंतव्य_मान, int मान, size_t 바이트수) {
    unsigned char *आँकड़े = गंतव्य_मान;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) आँकड़े[칸] = मान;
    return गंतव्य_मान;
}
int putchar(int 문자) { unsigned char मान = 문자; return write(1, &मान, 1) == 1 ? मान : EOF; }
int puts(const char *स्ट्रिंग_मान) {
    size_t 길이 = strlen(स्ट्रिंग_मान), स्थान = 0;
    while (स्थान < 길이) { ssize_t परिणाम = write(1, स्ट्रिंग_मान + स्थान, 길이 - स्थान); if (परिणाम <= 0) return EOF; स्थान += परिणाम; }
    return putchar('\n') == EOF ? EOF : 0;
}

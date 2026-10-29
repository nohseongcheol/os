#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *низ_стойност) { size_t 길이 = 0; while (низ_стойност[길이]) 길이++; return 길이; }
int strcmp(const char *предна_стойност, const char *НАЗАД_стойност) {
    while (*предна_стойност && *предна_стойност == *НАЗАД_стойност) { предна_стойност++; НАЗАД_стойност++; }
    return (unsigned char)*предна_стойност - (unsigned char)*НАЗАД_стойност;
}
int memcmp(const void *предна_стойност, const void *НАЗАД_стойност, size_t 바이트수) {
    const unsigned char *가 = предна_стойност, *나 = НАЗАД_стойност;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *местоназначение_стойност, const void *원본, size_t 바이트수) {
    unsigned char *가 = местоназначение_стойност; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return местоназначение_стойност;
}
void *memset(void *местоназначение_стойност, int стойност, size_t 바이트수) {
    unsigned char *данни = местоназначение_стойност;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) данни[칸] = стойност;
    return местоназначение_стойност;
}
int putchar(int 문자) { unsigned char стойност = 문자; return write(1, &стойност, 1) == 1 ? стойност : EOF; }
int puts(const char *низ_стойност) {
    size_t 길이 = strlen(низ_стойност), Позиция = 0;
    while (Позиция < 길이) { ssize_t РЕЗУЛТАТ = write(1, низ_стойност + Позиция, 길이 - Позиция); if (РЕЗУЛТАТ <= 0) return EOF; Позиция += РЕЗУЛТАТ; }
    return putchar('\n') == EOF ? EOF : 0;
}

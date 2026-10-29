#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *строка_ЗНАЧЕН) { size_t длина_ЗНАЧЕН = 0; while (строка_ЗНАЧЕН[длина_ЗНАЧЕН]) длина_ЗНАЧЕН++; return длина_ЗНАЧЕН; }
int strcmp(const char *лицевая_камера_ЗНАЧЕН, const char *BACK_ЗНАЧЕН) {
    while (*лицевая_камера_ЗНАЧЕН && *лицевая_камера_ЗНАЧЕН == *BACK_ЗНАЧЕН) { лицевая_камера_ЗНАЧЕН++; BACK_ЗНАЧЕН++; }
    return (unsigned char)*лицевая_камера_ЗНАЧЕН - (unsigned char)*BACK_ЗНАЧЕН;
}
int memcmp(const void *лицевая_камера_ЗНАЧЕН, const void *BACK_ЗНАЧЕН, size_t байт_СЧЁТ) {
    const unsigned char *가 = лицевая_камера_ЗНАЧЕН, *СЕКУНДЫ_операнд = BACK_ЗНАЧЕН;
    for (size_t слот_ввод = 0; слот_ввод < байт_СЧЁТ; слот_ввод++) if (가[слот_ввод] != СЕКУНДЫ_операнд[слот_ввод]) return 가[слот_ввод] - СЕКУНДЫ_операнд[слот_ввод];
    return 0;
}
void *memcpy(void *цель_ЗНАЧЕН, const void *원본, size_t байт_СЧЁТ) {
    unsigned char *가 = цель_ЗНАЧЕН; const unsigned char *СЕКУНДЫ_операнд = 원본;
    for (size_t слот_ввод = 0; слот_ввод < байт_СЧЁТ; слот_ввод++) 가[слот_ввод] = СЕКУНДЫ_операнд[слот_ввод];
    return цель_ЗНАЧЕН;
}
void *memset(void *цель_ЗНАЧЕН, int ЗНАЧЕН, size_t байт_СЧЁТ) {
    unsigned char *данные = цель_ЗНАЧЕН;
    for (size_t слот_ввод = 0; слот_ввод < байт_СЧЁТ; слот_ввод++) данные[слот_ввод] = ЗНАЧЕН;
    return цель_ЗНАЧЕН;
}
int putchar(int 문자) { unsigned char ЗНАЧЕН = 문자; return write(1, &ЗНАЧЕН, 1) == 1 ? ЗНАЧЕН : EOF; }
int puts(const char *строка_ЗНАЧЕН) {
    size_t длина_ЗНАЧЕН = strlen(строка_ЗНАЧЕН), позиция = 0;
    while (позиция < длина_ЗНАЧЕН) { ssize_t результат = write(1, строка_ЗНАЧЕН + позиция, длина_ЗНАЧЕН - позиция); if (результат <= 0) return EOF; позиция += результат; }
    return putchar('\n') == EOF ? EOF : 0;
}

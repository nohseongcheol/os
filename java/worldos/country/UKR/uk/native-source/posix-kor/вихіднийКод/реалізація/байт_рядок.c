#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *рядок_значення) { size_t 길이 = 0; while (рядок_значення[길이]) 길이++; return 길이; }
int strcmp(const char *фронтальна_камера_значення, const char *НАЗАД_значення) {
    while (*фронтальна_камера_значення && *фронтальна_камера_значення == *НАЗАД_значення) { фронтальна_камера_значення++; НАЗАД_значення++; }
    return (unsigned char)*фронтальна_камера_значення - (unsigned char)*НАЗАД_значення;
}
int memcmp(const void *фронтальна_камера_значення, const void *НАЗАД_значення, size_t 바이트수) {
    const unsigned char *가 = фронтальна_камера_значення, *나 = НАЗАД_значення;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *місце_значення, const void *원본, size_t 바이트수) {
    unsigned char *가 = місце_значення; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return місце_значення;
}
void *memset(void *місце_значення, int значення, size_t 바이트수) {
    unsigned char *дані = місце_значення;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) дані[칸] = значення;
    return місце_значення;
}
int putchar(int 문자) { unsigned char значення = 문자; return write(1, &значення, 1) == 1 ? значення : EOF; }
int puts(const char *рядок_значення) {
    size_t 길이 = strlen(рядок_значення), позиція = 0;
    while (позиція < 길이) { ssize_t результат = write(1, рядок_значення + позиція, 길이 - позиція); if (результат <= 0) return EOF; позиція += результат; }
    return putchar('\n') == EOF ? EOF : 0;
}

#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *տող_արժեք_6ca8363c) { size_t տեւողություն_արժեք = 0; while (տող_արժեք_6ca8363c[տեւողություն_արժեք]) տեւողություն_արժեք++; return տեւողություն_արժեք; }
int strcmp(const char *앞, const char *Հետ_արժեք) {
    while (*앞 && *앞 == *Հետ_արժեք) { 앞++; Հետ_արժեք++; }
    return (unsigned char)*앞 - (unsigned char)*Հետ_արժեք;
}
int memcmp(const void *앞, const void *Հետ_արժեք, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Հետ_արժեք;
    for (size_t փորակ_մուտքագրում = 0; փորակ_մուտքագրում < 바이트수; փորակ_մուտքագրում++) if (가[փորակ_մուտքագրում] != 나[փորակ_մուտքագրում]) return 가[փորակ_մուտքագրում] - 나[փորակ_մուտքագրում];
    return 0;
}
void *memcpy(void *նպատակակետ_արժեք, const void *원본, size_t 바이트수) {
    unsigned char *가 = նպատակակետ_արժեք; const unsigned char *나 = 원본;
    for (size_t փորակ_մուտքագրում = 0; փորակ_մուտքագրում < 바이트수; փորակ_մուտքագրում++) 가[փորակ_մուտքագրում] = 나[փորակ_մուտքագրում];
    return նպատակակետ_արժեք;
}
void *memset(void *նպատակակետ_արժեք, int արժեք, size_t 바이트수) {
    unsigned char *տվյալ = նպատակակետ_արժեք;
    for (size_t փորակ_մուտքագրում = 0; փորակ_մուտքագրում < 바이트수; փորակ_մուտքագրում++) տվյալ[փորակ_մուտքագրում] = արժեք;
    return նպատակակետ_արժեք;
}
int putchar(int 문자) { unsigned char արժեք = 문자; return write(1, &արժեք, 1) == 1 ? արժեք : EOF; }
int puts(const char *տող_արժեք_6ca8363c) {
    size_t տեւողություն_արժեք = strlen(տող_արժեք_6ca8363c), Դիրք = 0;
    while (Դիրք < տեւողություն_արժեք) { ssize_t չափ = write(1, տող_արժեք_6ca8363c + Դիրք, տեւողություն_արժեք - Դիրք); if (չափ <= 0) return EOF; Դիրք += չափ; }
    return putchar('\n') == EOF ? EOF : 0;
}

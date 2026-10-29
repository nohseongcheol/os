#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *سلک_قدر) { size_t لمبا_ئی_قدر = 0; while (سلک_قدر[لمبا_ئی_قدر]) لمبا_ئی_قدر++; return لمبا_ئی_قدر; }
int strcmp(const char *앞, const char *واپس_قدر) {
    while (*앞 && *앞 == *واپس_قدر) { 앞++; واپس_قدر++; }
    return (unsigned char)*앞 - (unsigned char)*واپس_قدر;
}
int memcmp(const void *앞, const void *واپس_قدر, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = واپس_قدر;
    for (size_t سلاٹ_اندراج = 0; سلاٹ_اندراج < 바이트수; سلاٹ_اندراج++) if (가[سلاٹ_اندراج] != 나[سلاٹ_اندراج]) return 가[سلاٹ_اندراج] - 나[سلاٹ_اندراج];
    return 0;
}
void *memcpy(void *منزل_مقصود_قدر, const void *원본, size_t 바이트수) {
    unsigned char *가 = منزل_مقصود_قدر; const unsigned char *나 = 원본;
    for (size_t سلاٹ_اندراج = 0; سلاٹ_اندراج < 바이트수; سلاٹ_اندراج++) 가[سلاٹ_اندراج] = 나[سلاٹ_اندراج];
    return منزل_مقصود_قدر;
}
void *memset(void *منزل_مقصود_قدر, int قدر, size_t 바이트수) {
    unsigned char *کوائف = منزل_مقصود_قدر;
    for (size_t سلاٹ_اندراج = 0; سلاٹ_اندراج < 바이트수; سلاٹ_اندراج++) کوائف[سلاٹ_اندراج] = قدر;
    return منزل_مقصود_قدر;
}
int putchar(int 문자) { unsigned char قدر = 문자; return write(1, &قدر, 1) == 1 ? قدر : EOF; }
int puts(const char *سلک_قدر) {
    size_t لمبا_ئی_قدر = strlen(سلک_قدر), مقام = 0;
    while (مقام < لمبا_ئی_قدر) { ssize_t پیمائش = write(1, سلک_قدر + مقام, لمبا_ئی_قدر - مقام); if (پیمائش <= 0) return EOF; مقام += پیمائش; }
    return putchar('\n') == EOF ? EOF : 0;
}

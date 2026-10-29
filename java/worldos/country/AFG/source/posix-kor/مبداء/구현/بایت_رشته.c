#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *رشته_مقدار_6ca8363c) { size_t طول_مقدار = 0; while (رشته_مقدار_6ca8363c[طول_مقدار]) طول_مقدار++; return طول_مقدار; }
int strcmp(const char *جلو_مقدار, const char *برگشت_مقدار) {
    while (*جلو_مقدار && *جلو_مقدار == *برگشت_مقدار) { جلو_مقدار++; برگشت_مقدار++; }
    return (unsigned char)*جلو_مقدار - (unsigned char)*برگشت_مقدار;
}
int memcmp(const void *جلو_مقدار, const void *برگشت_مقدار, size_t 바이트수) {
    const unsigned char *가 = جلو_مقدار, *나 = برگشت_مقدار;
    for (size_t شکاف_ورودی = 0; شکاف_ورودی < 바이트수; شکاف_ورودی++) if (가[شکاف_ورودی] != 나[شکاف_ورودی]) return 가[شکاف_ورودی] - 나[شکاف_ورودی];
    return 0;
}
void *memcpy(void *مقصد_مقدار, const void *원본, size_t 바이트수) {
    unsigned char *가 = مقصد_مقدار; const unsigned char *나 = 원본;
    for (size_t شکاف_ورودی = 0; شکاف_ورودی < 바이트수; شکاف_ورودی++) 가[شکاف_ورودی] = 나[شکاف_ورودی];
    return مقصد_مقدار;
}
void *memset(void *مقصد_مقدار, int مقدار, size_t 바이트수) {
    unsigned char *داده_ها = مقصد_مقدار;
    for (size_t شکاف_ورودی = 0; شکاف_ورودی < 바이트수; شکاف_ورودی++) داده_ها[شکاف_ورودی] = مقدار;
    return مقصد_مقدار;
}
int putchar(int 문자) { unsigned char مقدار = 문자; return write(1, &مقدار, 1) == 1 ? مقدار : EOF; }
int puts(const char *رشته_مقدار_6ca8363c) {
    size_t طول_مقدار = strlen(رشته_مقدار_6ca8363c), مرتب_کردن = 0;
    while (مرتب_کردن < طول_مقدار) { ssize_t سنجش = write(1, رشته_مقدار_6ca8363c + مرتب_کردن, طول_مقدار - مرتب_کردن); if (سنجش <= 0) return EOF; مرتب_کردن += سنجش; }
    return putchar('\n') == EOF ? EOF : 0;
}

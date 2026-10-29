#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *سلسلة_قيمة) { size_t 길이 = 0; while (سلسلة_قيمة[길이]) 길이++; return 길이; }
int strcmp(const char *الكاميرا_الأمامية_قيمة, const char *عودة_قيمة) {
    while (*الكاميرا_الأمامية_قيمة && *الكاميرا_الأمامية_قيمة == *عودة_قيمة) { الكاميرا_الأمامية_قيمة++; عودة_قيمة++; }
    return (unsigned char)*الكاميرا_الأمامية_قيمة - (unsigned char)*عودة_قيمة;
}
int memcmp(const void *الكاميرا_الأمامية_قيمة, const void *عودة_قيمة, size_t 바이트수) {
    const unsigned char *가 = الكاميرا_الأمامية_قيمة, *나 = عودة_قيمة;
    for (size_t فتحة_إدخال = 0; فتحة_إدخال < 바이트수; فتحة_إدخال++) if (가[فتحة_إدخال] != 나[فتحة_إدخال]) return 가[فتحة_إدخال] - 나[فتحة_إدخال];
    return 0;
}
void *memcpy(void *وجهة_قيمة, const void *원본, size_t 바이트수) {
    unsigned char *가 = وجهة_قيمة; const unsigned char *나 = 원본;
    for (size_t فتحة_إدخال = 0; فتحة_إدخال < 바이트수; فتحة_إدخال++) 가[فتحة_إدخال] = 나[فتحة_إدخال];
    return وجهة_قيمة;
}
void *memset(void *وجهة_قيمة, int قيمة, size_t 바이트수) {
    unsigned char *بيانات = وجهة_قيمة;
    for (size_t فتحة_إدخال = 0; فتحة_إدخال < 바이트수; فتحة_إدخال++) بيانات[فتحة_إدخال] = قيمة;
    return وجهة_قيمة;
}
int putchar(int 문자) { unsigned char قيمة = 문자; return write(1, &قيمة, 1) == 1 ? قيمة : EOF; }
int puts(const char *سلسلة_قيمة) {
    size_t 길이 = strlen(سلسلة_قيمة), موضع = 0;
    while (موضع < 길이) { ssize_t نتيجة = write(1, سلسلة_قيمة + موضع, 길이 - موضع); if (نتيجة <= 0) return EOF; موضع += نتيجة; }
    return putchar('\n') == EOF ? EOF : 0;
}

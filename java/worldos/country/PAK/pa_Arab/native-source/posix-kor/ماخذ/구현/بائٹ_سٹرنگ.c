#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *سٹرنگ_قدر) { size_t لمبائی_قدر = 0; while (سٹرنگ_قدر[لمبائی_قدر]) لمبائی_قدر++; return لمبائی_قدر; }
int strcmp(const char *앞, const char *پیچھے_قدر) {
    while (*앞 && *앞 == *پیچھے_قدر) { 앞++; پیچھے_قدر++; }
    return (unsigned char)*앞 - (unsigned char)*پیچھے_قدر;
}
int memcmp(const void *앞, const void *پیچھے_قدر, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = پیچھے_قدر;
    for (size_t سلاٹ_داخلہ = 0; سلاٹ_داخلہ < 바이트수; سلاٹ_داخلہ++) if (가[سلاٹ_داخلہ] != 나[سلاٹ_داخلہ]) return 가[سلاٹ_داخلہ] - 나[سلاٹ_داخلہ];
    return 0;
}
void *memcpy(void *منزل_مقصود_قدر, const void *원본, size_t 바이트수) {
    unsigned char *가 = منزل_مقصود_قدر; const unsigned char *나 = 원본;
    for (size_t سلاٹ_داخلہ = 0; سلاٹ_داخلہ < 바이트수; سلاٹ_داخلہ++) 가[سلاٹ_داخلہ] = 나[سلاٹ_داخلہ];
    return منزل_مقصود_قدر;
}
void *memset(void *منزل_مقصود_قدر, int قدر, size_t 바이트수) {
    unsigned char *کوائف = منزل_مقصود_قدر;
    for (size_t سلاٹ_داخلہ = 0; سلاٹ_داخلہ < 바이트수; سلاٹ_داخلہ++) کوائف[سلاٹ_داخلہ] = قدر;
    return منزل_مقصود_قدر;
}
int putchar(int 문자) { unsigned char قدر = 문자; return write(1, &قدر, 1) == 1 ? قدر : EOF; }
int puts(const char *سٹرنگ_قدر) {
    size_t لمبائی_قدر = strlen(سٹرنگ_قدر), 위치 = 0;
    while (위치 < لمبائی_قدر) { ssize_t 결과 = write(1, سٹرنگ_قدر + 위치, لمبائی_قدر - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

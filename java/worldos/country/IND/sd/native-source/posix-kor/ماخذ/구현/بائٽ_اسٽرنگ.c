#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *اسٽرنگ_قدر) { size_t لمبائي_قدر = 0; while (اسٽرنگ_قدر[لمبائي_قدر]) لمبائي_قدر++; return لمبائي_قدر; }
int strcmp(const char *앞, const char *واپس_قدر) {
    while (*앞 && *앞 == *واپس_قدر) { 앞++; واپس_قدر++; }
    return (unsigned char)*앞 - (unsigned char)*واپس_قدر;
}
int memcmp(const void *앞, const void *واپس_قدر, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = واپس_قدر;
    for (size_t سوراخ_داخلا = 0; سوراخ_داخلا < 바이트수; سوراخ_داخلا++) if (가[سوراخ_داخلا] != 나[سوراخ_داخلا]) return 가[سوراخ_داخلا] - 나[سوراخ_داخلا];
    return 0;
}
void *memcpy(void *منزل_مقصود_قدر, const void *원본, size_t 바이트수) {
    unsigned char *가 = منزل_مقصود_قدر; const unsigned char *나 = 원본;
    for (size_t سوراخ_داخلا = 0; سوراخ_داخلا < 바이트수; سوراخ_داخلا++) 가[سوراخ_داخلا] = 나[سوراخ_داخلا];
    return منزل_مقصود_قدر;
}
void *memset(void *منزل_مقصود_قدر, int قدر, size_t 바이트수) {
    unsigned char *ڪوائف = منزل_مقصود_قدر;
    for (size_t سوراخ_داخلا = 0; سوراخ_داخلا < 바이트수; سوراخ_داخلا++) ڪوائف[سوراخ_داخلا] = قدر;
    return منزل_مقصود_قدر;
}
int putchar(int 문자) { unsigned char قدر = 문자; return write(1, &قدر, 1) == 1 ? قدر : EOF; }
int puts(const char *اسٽرنگ_قدر) {
    size_t لمبائي_قدر = strlen(اسٽرنگ_قدر), 위치 = 0;
    while (위치 < لمبائي_قدر) { ssize_t 결과 = write(1, اسٽرنگ_قدر + 위치, لمبائي_قدر - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

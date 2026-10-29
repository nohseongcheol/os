#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *сатр_қимат_6ca8363c) { size_t дарозӣ_қимат = 0; while (сатр_қимат_6ca8363c[дарозӣ_қимат]) дарозӣ_қимат++; return дарозӣ_қимат; }
int strcmp(const char *앞, const char *Бозгашт_қимат) {
    while (*앞 && *앞 == *Бозгашт_қимат) { 앞++; Бозгашт_қимат++; }
    return (unsigned char)*앞 - (unsigned char)*Бозгашт_қимат;
}
int memcmp(const void *앞, const void *Бозгашт_қимат, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Бозгашт_қимат;
    for (size_t ковокӣ_ворида = 0; ковокӣ_ворида < 바이트수; ковокӣ_ворида++) if (가[ковокӣ_ворида] != 나[ковокӣ_ворида]) return 가[ковокӣ_ворида] - 나[ковокӣ_ворида];
    return 0;
}
void *memcpy(void *ҷои_таъинот_қимат, const void *원본, size_t 바이트수) {
    unsigned char *가 = ҷои_таъинот_қимат; const unsigned char *나 = 원본;
    for (size_t ковокӣ_ворида = 0; ковокӣ_ворида < 바이트수; ковокӣ_ворида++) 가[ковокӣ_ворида] = 나[ковокӣ_ворида];
    return ҷои_таъинот_қимат;
}
void *memset(void *ҷои_таъинот_қимат, int қимат, size_t 바이트수) {
    unsigned char *иттилоот = ҷои_таъинот_қимат;
    for (size_t ковокӣ_ворида = 0; ковокӣ_ворида < 바이트수; ковокӣ_ворида++) иттилоот[ковокӣ_ворида] = қимат;
    return ҷои_таъинот_қимат;
}
int putchar(int 문자) { unsigned char қимат = 문자; return write(1, &қимат, 1) == 1 ? қимат : EOF; }
int puts(const char *сатр_қимат_6ca8363c) {
    size_t дарозӣ_қимат = strlen(сатр_қимат_6ca8363c), 위치 = 0;
    while (위치 < дарозӣ_қимат) { ssize_t 결과 = write(1, сатр_қимат_6ca8363c + 위치, дарозӣ_қимат - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

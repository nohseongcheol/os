#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *مزى_ارزښت_6ca8363c) { size_t اوږدوالى_ارزښت = 0; while (مزى_ارزښت_6ca8363c[اوږدوالى_ارزښت]) اوږدوالى_ارزښت++; return اوږدوالى_ارزښت; }
int strcmp(const char *앞, const char *뒤) {
    while (*앞 && *앞 == *뒤) { 앞++; 뒤++; }
    return (unsigned char)*앞 - (unsigned char)*뒤;
}
int memcmp(const void *앞, const void *뒤, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = 뒤;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *موخه_ارزښت, const void *원본, size_t 바이트수) {
    unsigned char *가 = موخه_ارزښت; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return موخه_ارزښت;
}
void *memset(void *موخه_ارزښت, int ارزښت, size_t 바이트수) {
    unsigned char *اومتوک = موخه_ارزښت;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) اومتوک[칸] = ارزښت;
    return موخه_ارزښت;
}
int putchar(int 문자) { unsigned char ارزښت = 문자; return write(1, &ارزښت, 1) == 1 ? ارزښت : EOF; }
int puts(const char *مزى_ارزښت_6ca8363c) {
    size_t اوږدوالى_ارزښت = strlen(مزى_ارزښت_6ca8363c), ځای = 0;
    while (ځای < اوږدوالى_ارزښت) { ssize_t 결과 = write(1, مزى_ارزښت_6ca8363c + ځای, اوږدوالى_ارزښت - ځای); if (결과 <= 0) return EOF; ځای += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

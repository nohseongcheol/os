#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *streng_VÆRDI) { size_t varighed_VÆRDI = 0; while (streng_VÆRDI[varighed_VÆRDI]) varighed_VÆRDI++; return varighed_VÆRDI; }
int strcmp(const char *frontvendt_VÆRDI, const char *BACK_VÆRDI) {
    while (*frontvendt_VÆRDI && *frontvendt_VÆRDI == *BACK_VÆRDI) { frontvendt_VÆRDI++; BACK_VÆRDI++; }
    return (unsigned char)*frontvendt_VÆRDI - (unsigned char)*BACK_VÆRDI;
}
int memcmp(const void *frontvendt_VÆRDI, const void *BACK_VÆRDI, size_t byte_TÆL) {
    const unsigned char *가 = frontvendt_VÆRDI, *SEKUND_operand = BACK_VÆRDI;
    for (size_t udvidelsesstik_post = 0; udvidelsesstik_post < byte_TÆL; udvidelsesstik_post++) if (가[udvidelsesstik_post] != SEKUND_operand[udvidelsesstik_post]) return 가[udvidelsesstik_post] - SEKUND_operand[udvidelsesstik_post];
    return 0;
}
void *memcpy(void *destination_VÆRDI, const void *원본, size_t byte_TÆL) {
    unsigned char *가 = destination_VÆRDI; const unsigned char *SEKUND_operand = 원본;
    for (size_t udvidelsesstik_post = 0; udvidelsesstik_post < byte_TÆL; udvidelsesstik_post++) 가[udvidelsesstik_post] = SEKUND_operand[udvidelsesstik_post];
    return destination_VÆRDI;
}
void *memset(void *destination_VÆRDI, int VÆRDI, size_t byte_TÆL) {
    unsigned char *data = destination_VÆRDI;
    for (size_t udvidelsesstik_post = 0; udvidelsesstik_post < byte_TÆL; udvidelsesstik_post++) data[udvidelsesstik_post] = VÆRDI;
    return destination_VÆRDI;
}
int putchar(int 문자) { unsigned char VÆRDI = 문자; return write(1, &VÆRDI, 1) == 1 ? VÆRDI : EOF; }
int puts(const char *streng_VÆRDI) {
    size_t varighed_VÆRDI = strlen(streng_VÆRDI), Placering = 0;
    while (Placering < varighed_VÆRDI) { ssize_t KR = write(1, streng_VÆRDI + Placering, varighed_VÆRDI - Placering); if (KR <= 0) return EOF; Placering += KR; }
    return putchar('\n') == EOF ? EOF : 0;
}

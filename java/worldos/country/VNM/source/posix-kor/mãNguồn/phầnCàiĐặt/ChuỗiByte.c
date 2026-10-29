#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ChuỗiKýTự) { size_t độDài = 0; while (ChuỗiKýTự[độDài]) độDài++; return độDài; }
int strcmp(const char *giáTrịPhíaTrước, const char *giáTrịLùi) {
    while (*giáTrịPhíaTrước && *giáTrịPhíaTrước == *giáTrịLùi) { giáTrịPhíaTrước++; giáTrịLùi++; }
    return (unsigned char)*giáTrịPhíaTrước - (unsigned char)*giáTrịLùi;
}
int memcmp(const void *giáTrịPhíaTrước, const void *giáTrịLùi, size_t sốLượngByte) {
    const unsigned char *toánHạngĐầuTiên = giáTrịPhíaTrước, *toánHạngThứHai = giáTrịLùi;
    for (size_t mụcÔ = 0; mụcÔ < sốLượngByte; mụcÔ++) if (toánHạngĐầuTiên[mụcÔ] != toánHạngThứHai[mụcÔ]) return toánHạngĐầuTiên[mụcÔ] - toánHạngThứHai[mụcÔ];
    return 0;
}
void *memcpy(void *giáTrịĐích, const void *nguyênBản, size_t sốLượngByte) {
    unsigned char *toánHạngĐầuTiên = giáTrịĐích; const unsigned char *toánHạngThứHai = nguyênBản;
    for (size_t mụcÔ = 0; mụcÔ < sốLượngByte; mụcÔ++) toánHạngĐầuTiên[mụcÔ] = toánHạngThứHai[mụcÔ];
    return giáTrịĐích;
}
void *memset(void *giáTrịĐích, int giáTrị, size_t sốLượngByte) {
    unsigned char *DữLiệu = giáTrịĐích;
    for (size_t mụcÔ = 0; mụcÔ < sốLượngByte; mụcÔ++) DữLiệu[mụcÔ] = giáTrị;
    return giáTrịĐích;
}
int putchar(int KýTự) { unsigned char giáTrị = KýTự; return write(1, &giáTrị, 1) == 1 ? giáTrị : EOF; }
int puts(const char *ChuỗiKýTự) {
    size_t độDài = strlen(ChuỗiKýTự), vịTrí = 0;
    while (vịTrí < độDài) { ssize_t kếtQuả = write(1, ChuỗiKýTự + vịTrí, độDài - vịTrí); if (kếtQuả <= 0) return EOF; vịTrí += kếtQuả; }
    return putchar('\n') == EOF ? EOF : 0;
}

#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *dize_değer) { size_t süre_değer = 0; while (dize_değer[süre_değer]) süre_değer++; return süre_değer; }
int strcmp(const char *ön_kamera_değer, const char *BACK_değer) {
    while (*ön_kamera_değer && *ön_kamera_değer == *BACK_değer) { ön_kamera_değer++; BACK_değer++; }
    return (unsigned char)*ön_kamera_değer - (unsigned char)*BACK_değer;
}
int memcmp(const void *ön_kamera_değer, const void *BACK_değer, size_t bayt_BAĞ_DEĞ_SAY) {
    const unsigned char *가 = ön_kamera_değer, *SANİYE_işlenen = BACK_değer;
    for (size_t yuva_girdi = 0; yuva_girdi < bayt_BAĞ_DEĞ_SAY; yuva_girdi++) if (가[yuva_girdi] != SANİYE_işlenen[yuva_girdi]) return 가[yuva_girdi] - SANİYE_işlenen[yuva_girdi];
    return 0;
}
void *memcpy(void *hedef_değer, const void *원본, size_t bayt_BAĞ_DEĞ_SAY) {
    unsigned char *가 = hedef_değer; const unsigned char *SANİYE_işlenen = 원본;
    for (size_t yuva_girdi = 0; yuva_girdi < bayt_BAĞ_DEĞ_SAY; yuva_girdi++) 가[yuva_girdi] = SANİYE_işlenen[yuva_girdi];
    return hedef_değer;
}
void *memset(void *hedef_değer, int değer, size_t bayt_BAĞ_DEĞ_SAY) {
    unsigned char *veri = hedef_değer;
    for (size_t yuva_girdi = 0; yuva_girdi < bayt_BAĞ_DEĞ_SAY; yuva_girdi++) veri[yuva_girdi] = değer;
    return hedef_değer;
}
int putchar(int 문자) { unsigned char değer = 문자; return write(1, &değer, 1) == 1 ? değer : EOF; }
int puts(const char *dize_değer) {
    size_t süre_değer = strlen(dize_değer), konum = 0;
    while (konum < süre_değer) { ssize_t sonuç = write(1, dize_değer + konum, süre_değer - konum); if (sonuç <= 0) return EOF; konum += sonuç; }
    return putchar('\n') == EOF ? EOF : 0;
}

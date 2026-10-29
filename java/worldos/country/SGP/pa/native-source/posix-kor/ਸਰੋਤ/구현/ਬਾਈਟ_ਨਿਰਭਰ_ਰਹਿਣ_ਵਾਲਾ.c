#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ) { size_t ਲੰਬਾਈ_ਕੀਮਤ = 0; while (ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ[ਲੰਬਾਈ_ਕੀਮਤ]) ਲੰਬਾਈ_ਕੀਮਤ++; return ਲੰਬਾਈ_ਕੀਮਤ; }
int strcmp(const char *앞, const char *ਪਿਛਲਾ_ਕੀਮਤ) {
    while (*앞 && *앞 == *ਪਿਛਲਾ_ਕੀਮਤ) { 앞++; ਪਿਛਲਾ_ਕੀਮਤ++; }
    return (unsigned char)*앞 - (unsigned char)*ਪਿਛਲਾ_ਕੀਮਤ;
}
int memcmp(const void *앞, const void *ਪਿਛਲਾ_ਕੀਮਤ, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = ਪਿਛਲਾ_ਕੀਮਤ;
    for (size_t ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < 바이트수; ਸਲੌਟ_ਦਾਖਲਾ++) if (가[ਸਲੌਟ_ਦਾਖਲਾ] != 나[ਸਲੌਟ_ਦਾਖਲਾ]) return 가[ਸਲੌਟ_ਦਾਖਲਾ] - 나[ਸਲੌਟ_ਦਾਖਲਾ];
    return 0;
}
void *memcpy(void *ਮੰਜਿਲ_ਕੀਮਤ, const void *원본, size_t 바이트수) {
    unsigned char *가 = ਮੰਜਿਲ_ਕੀਮਤ; const unsigned char *나 = 원본;
    for (size_t ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < 바이트수; ਸਲੌਟ_ਦਾਖਲਾ++) 가[ਸਲੌਟ_ਦਾਖਲਾ] = 나[ਸਲੌਟ_ਦਾਖਲਾ];
    return ਮੰਜਿਲ_ਕੀਮਤ;
}
void *memset(void *ਮੰਜਿਲ_ਕੀਮਤ, int ਕੀਮਤ, size_t 바이트수) {
    unsigned char *ਸਮੱਗਰੀ = ਮੰਜਿਲ_ਕੀਮਤ;
    for (size_t ਸਲੌਟ_ਦਾਖਲਾ = 0; ਸਲੌਟ_ਦਾਖਲਾ < 바이트수; ਸਲੌਟ_ਦਾਖਲਾ++) ਸਮੱਗਰੀ[ਸਲੌਟ_ਦਾਖਲਾ] = ਕੀਮਤ;
    return ਮੰਜਿਲ_ਕੀਮਤ;
}
int putchar(int 문자) { unsigned char ਕੀਮਤ = 문자; return write(1, &ਕੀਮਤ, 1) == 1 ? ਕੀਮਤ : EOF; }
int puts(const char *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ) {
    size_t ਲੰਬਾਈ_ਕੀਮਤ = strlen(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ), ਸਥਿਤੀ = 0;
    while (ਸਥਿਤੀ < ਲੰਬਾਈ_ਕੀਮਤ) { ssize_t ਮਾਪ = write(1, ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ + ਸਥਿਤੀ, ਲੰਬਾਈ_ਕੀਮਤ - ਸਥਿਤੀ); if (ਮਾਪ <= 0) return EOF; ਸਥਿਤੀ += ਮਾਪ; }
    return putchar('\n') == EOF ? EOF : 0;
}

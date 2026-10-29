#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ) { size_t ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = 0; while (ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ[ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ]) ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ++; return ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; }
int strcmp(const char *앞, const char *ପଛ_ମୂଲ୍ୟ) {
    while (*앞 && *앞 == *ପଛ_ମୂଲ୍ୟ) { 앞++; ପଛ_ମୂଲ୍ୟ++; }
    return (unsigned char)*앞 - (unsigned char)*ପଛ_ମୂଲ୍ୟ;
}
int memcmp(const void *앞, const void *ପଛ_ମୂଲ୍ୟ, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = ପଛ_ମୂଲ୍ୟ;
    for (size_t ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 바이트수; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) if (가[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] != 나[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି]) return 가[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] - 나[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି];
    return 0;
}
void *memcpy(void *ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ, const void *원본, size_t 바이트수) {
    unsigned char *가 = ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ; const unsigned char *나 = 원본;
    for (size_t ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 바이트수; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) 가[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] = 나[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି];
    return ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ;
}
void *memset(void *ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ, int ମୂଲ୍ୟ, size_t 바이트수) {
    unsigned char *ଡାଟା = ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ;
    for (size_t ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 0; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି < 바이트수; ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି++) ଡାଟା[ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି] = ମୂଲ୍ୟ;
    return ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ;
}
int putchar(int 문자) { unsigned char ମୂଲ୍ୟ = 문자; return write(1, &ମୂଲ୍ୟ, 1) == 1 ? ମୂଲ୍ୟ : EOF; }
int puts(const char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ) {
    size_t ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = strlen(ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ), ଅବସ୍ଥାନ = 0;
    while (ଅବସ୍ଥାନ < ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) { ssize_t ମାପ = write(1, ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ + ଅବସ୍ଥାନ, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - ଅବସ୍ଥାନ); if (ମାପ <= 0) return EOF; ଅବସ୍ଥାନ += ମାପ; }
    return putchar('\n') == EOF ? EOF : 0;
}

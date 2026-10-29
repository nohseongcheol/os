#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ሕብረ_ቁምፊ_ዋጋ) { size_t ንውሓት_ዋጋ = 0; while (ሕብረ_ቁምፊ_ዋጋ[ንውሓት_ዋጋ]) ንውሓት_ዋጋ++; return ንውሓት_ዋጋ; }
int strcmp(const char *앞, const char *ድሕሪት_ዋጋ) {
    while (*앞 && *앞 == *ድሕሪት_ዋጋ) { 앞++; ድሕሪት_ዋጋ++; }
    return (unsigned char)*앞 - (unsigned char)*ድሕሪት_ዋጋ;
}
int memcmp(const void *앞, const void *ድሕሪት_ዋጋ, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = ድሕሪት_ዋጋ;
    for (size_t መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 바이트수; መሰኩዒ_ምእታው++) if (가[መሰኩዒ_ምእታው] != 나[መሰኩዒ_ምእታው]) return 가[መሰኩዒ_ምእታው] - 나[መሰኩዒ_ምእታው];
    return 0;
}
void *memcpy(void *መዓልቦ_ዋጋ, const void *원본, size_t 바이트수) {
    unsigned char *가 = መዓልቦ_ዋጋ; const unsigned char *나 = 원본;
    for (size_t መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 바이트수; መሰኩዒ_ምእታው++) 가[መሰኩዒ_ምእታው] = 나[መሰኩዒ_ምእታው];
    return መዓልቦ_ዋጋ;
}
void *memset(void *መዓልቦ_ዋጋ, int ዋጋ, size_t 바이트수) {
    unsigned char *ሓበሬታ = መዓልቦ_ዋጋ;
    for (size_t መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 바이트수; መሰኩዒ_ምእታው++) ሓበሬታ[መሰኩዒ_ምእታው] = ዋጋ;
    return መዓልቦ_ዋጋ;
}
int putchar(int 문자) { unsigned char ዋጋ = 문자; return write(1, &ዋጋ, 1) == 1 ? ዋጋ : EOF; }
int puts(const char *ሕብረ_ቁምፊ_ዋጋ) {
    size_t ንውሓት_ዋጋ = strlen(ሕብረ_ቁምፊ_ዋጋ), 위치 = 0;
    while (위치 < ንውሓት_ዋጋ) { ssize_t 결과 = write(1, ሕብረ_ቁምፊ_ዋጋ + 위치, ንውሓት_ዋጋ - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

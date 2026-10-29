#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ኅብረቁምፊ_እሴት) { size_t ርዝመት_እሴት = 0; while (ኅብረቁምፊ_እሴት[ርዝመት_እሴት]) ርዝመት_እሴት++; return ርዝመት_እሴት; }
int strcmp(const char *ፊት_እሴት, const char *ተመለስ_እሴት) {
    while (*ፊት_እሴት && *ፊት_እሴት == *ተመለስ_እሴት) { ፊት_እሴት++; ተመለስ_እሴት++; }
    return (unsigned char)*ፊት_እሴት - (unsigned char)*ተመለስ_እሴት;
}
int memcmp(const void *ፊት_እሴት, const void *ተመለስ_እሴት, size_t 바이트수) {
    const unsigned char *가 = ፊት_እሴት, *나 = ተመለስ_እሴት;
    for (size_t ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < 바이트수; ማስገቢያ_ቀዳዳ_ምዝግብ++) if (가[ማስገቢያ_ቀዳዳ_ምዝግብ] != 나[ማስገቢያ_ቀዳዳ_ምዝግብ]) return 가[ማስገቢያ_ቀዳዳ_ምዝግብ] - 나[ማስገቢያ_ቀዳዳ_ምዝግብ];
    return 0;
}
void *memcpy(void *መድረሻ_እሴት, const void *원본, size_t 바이트수) {
    unsigned char *가 = መድረሻ_እሴት; const unsigned char *나 = 원본;
    for (size_t ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < 바이트수; ማስገቢያ_ቀዳዳ_ምዝግብ++) 가[ማስገቢያ_ቀዳዳ_ምዝግብ] = 나[ማስገቢያ_ቀዳዳ_ምዝግብ];
    return መድረሻ_እሴት;
}
void *memset(void *መድረሻ_እሴት, int እሴት, size_t 바이트수) {
    unsigned char *ውሂብ = መድረሻ_እሴት;
    for (size_t ማስገቢያ_ቀዳዳ_ምዝግብ = 0; ማስገቢያ_ቀዳዳ_ምዝግብ < 바이트수; ማስገቢያ_ቀዳዳ_ምዝግብ++) ውሂብ[ማስገቢያ_ቀዳዳ_ምዝግብ] = እሴት;
    return መድረሻ_እሴት;
}
int putchar(int 문자) { unsigned char እሴት = 문자; return write(1, &እሴት, 1) == 1 ? እሴት : EOF; }
int puts(const char *ኅብረቁምፊ_እሴት) {
    size_t ርዝመት_እሴት = strlen(ኅብረቁምፊ_እሴት), አካባቢ = 0;
    while (አካባቢ < ርዝመት_እሴት) { ssize_t ልኬት = write(1, ኅብረቁምፊ_እሴት + አካባቢ, ርዝመት_እሴት - አካባቢ); if (ልኬት <= 0) return EOF; አካባቢ += ልኬት; }
    return putchar('\n') == EOF ? EOF : 0;
}

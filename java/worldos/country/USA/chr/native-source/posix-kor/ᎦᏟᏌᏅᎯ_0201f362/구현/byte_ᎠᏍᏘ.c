#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ) { size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 0; while (ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ[ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ]) ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ++; return ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ; }
int strcmp(const char *앞, const char *ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ) {
    while (*앞 && *앞 == *ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ) { 앞++; ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ++; }
    return (unsigned char)*앞 - (unsigned char)*ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ;
}
int memcmp(const void *앞, const void *ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ, const void *원본, size_t 바이트수) {
    unsigned char *가 = ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ;
}
void *memset(void *ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ, int ᏧᎬᏩᎶᏗᏯ, size_t 바이트수) {
    unsigned char *ᎦᏟᏌᏅᎯ = ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) ᎦᏟᏌᏅᎯ[칸] = ᏧᎬᏩᎶᏗᏯ;
    return ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ;
}
int putchar(int 문자) { unsigned char ᏧᎬᏩᎶᏗᏯ = 문자; return write(1, &ᏧᎬᏩᎶᏗᏯ, 1) == 1 ? ᏧᎬᏩᎶᏗᏯ : EOF; }
int puts(const char *ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ) {
    size_t ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = strlen(ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ), 위치 = 0;
    while (위치 < ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) { ssize_t 결과 = write(1, ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ + 위치, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}

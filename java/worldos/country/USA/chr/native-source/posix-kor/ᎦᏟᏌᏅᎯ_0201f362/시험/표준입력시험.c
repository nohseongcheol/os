#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ) {
    (void)개수; (void)Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ;
    char ᎦᏟᏌᏅᎯ[6]; int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = 0;
    puts("POSIX INPUT READY");
    while (ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ < 6) {
        int 결과 = 파일자료읽기(0, ᎦᏟᏌᏅᎯ + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ, 6 - ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
        if (결과 <= 0) return 1;
        ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ += 결과;
    }
    if (memcmp(ᎦᏟᏌᏅᎯ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

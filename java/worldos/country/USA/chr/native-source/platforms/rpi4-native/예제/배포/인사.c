#include <파일규약.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ) {
    if (인수개수 < 1 || !ᏗᏓᎦᏘᎸᏍᏗ_ᏕᎦᏅᏅᏛ[0]) return 2;
    const char 인사말[] = "자체 커널의 C와 한국어 POSIX\n";
    int 문서 = ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ("인사.txt", ᎠᎪᎵᏰᏗᏊ_ᎪᏪᎶᏗ | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(문서, 인사말, sizeof(인사말) - 1);
    ᎯᏍᏚᎲᎦ_ᎠᏍᏆᏂᎪᏙᏗ(문서);
    ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(1, 인사말, sizeof(인사말) - 1);
    return ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ == sizeof(인사말) - 1 ? 0 : 3;
}

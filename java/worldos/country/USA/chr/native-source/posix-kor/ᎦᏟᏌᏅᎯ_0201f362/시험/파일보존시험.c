#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ) {
    (void)개수; (void)Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ;
    int ᎠᏍᏆᏂᎪᏙᏗ = ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ("stored.txt", ᎠᎪᎵᏰᏗᏊ_ᎪᏪᎶᏗ | 없으면만들기 | 내용비우기, 0600);
    if (ᎠᏍᏆᏂᎪᏙᏗ < 0 || ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(ᎠᏍᏆᏂᎪᏙᏗ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ᎠᏍᏆᏂᎪᏙᏗ) < 0) return 2;
    if (ᎯᏍᏚᎲᎦ_ᎠᏍᏆᏂᎪᏙᏗ(ᎠᏍᏆᏂᎪᏙᏗ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

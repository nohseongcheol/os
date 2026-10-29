#include <파일규약.h>
#include <stdio.h>
int main(int item_COUNT, char **inskrywing_Lys) {
    (void)item_COUNT; (void)inskrywing_Lys;
    int Lêer = skep_lêer("stored.txt", lees_skryf | 없으면만들기 | 내용비우기, 0600);
    if (Lêer < 0 || skryf_lêer_data(Lêer, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Lêer) < 0) return 2;
    if (sluit_lêer(Lêer) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

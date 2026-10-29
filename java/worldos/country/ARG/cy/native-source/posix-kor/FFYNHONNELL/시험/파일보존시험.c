#include <파일규약.h>
#include <stdio.h>
int main(int eitem_COUNT, char **cofnod_Rhestr) {
    (void)eitem_COUNT; (void)cofnod_Rhestr;
    int Ffeil = agor_ffeil("stored.txt", darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600);
    if (Ffeil < 0 || ysgrifennu_ffeil_data(Ffeil, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Ffeil) < 0) return 2;
    if (cau_ffeil(Ffeil) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

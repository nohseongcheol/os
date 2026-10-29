#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **унос_Листа) {
    (void)개수; (void)унос_Листа;
    int Датотека = креирати_фајл("stored.txt", за_читање_писање | 없으면만들기 | 내용비우기, 0600);
    if (Датотека < 0 || писати_фајл_подаци(Датотека, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Датотека) < 0) return 2;
    if (затварање_фајл(Датотека) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **унос_списак) {
    (void)개수; (void)унос_списак;
    int фајл = отворити_фајл("stored.txt", и_за_читање_и_за_писање | 없으면만들기 | 내용비우기, 0600);
    if (фајл < 0 || писати_фајл_подаци(фајл, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(фајл) < 0) return 2;
    if (затворити_фајл(фајл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

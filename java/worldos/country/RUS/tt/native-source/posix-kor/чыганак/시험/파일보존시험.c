#include <파일규약.h>
#include <stdio.h>
int main(int элемент_COUNT, char **кертү_Исемлек) {
    (void)элемент_COUNT; (void)кертү_Исемлек;
    int Birem = ачу_файл("stored.txt", укымалы_язмалы | 없으면만들기 | 내용비우기, 0600);
    if (Birem < 0 || язу_файл_мәгълүмат(Birem, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Birem) < 0) return 2;
    if (чик_файл(Birem) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

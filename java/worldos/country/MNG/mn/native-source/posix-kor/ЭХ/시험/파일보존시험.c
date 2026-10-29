#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **оролт_Жагсаалт) {
    (void)개수; (void)оролт_Жагсаалт;
    int Файл = нээх_файл("stored.txt", унших_бичих | 없으면만들기 | 내용비우기, 0600);
    if (Файл < 0 || бичих_файл_өгөгдөл(Файл, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Файл) < 0) return 2;
    if (хаах_файл(Файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

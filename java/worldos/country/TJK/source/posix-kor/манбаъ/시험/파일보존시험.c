#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ворида_Рӯйхат) {
    (void)개수; (void)ворида_Рӯйхат;
    int Файл = кушодан_файл("stored.txt", хондан_навиштан | 없으면만들기 | 내용비우기, 0600);
    if (Файл < 0 || навиштан_файл_иттилоот(Файл, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Файл) < 0) return 2;
    if (пӯшидан_файл(Файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

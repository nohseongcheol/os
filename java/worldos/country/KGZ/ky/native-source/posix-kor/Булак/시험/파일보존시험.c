#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **киргизме_жазуу_Тизме) {
    (void)개수; (void)киргизме_жазуу_Тизме;
    int Файл = ачуу_файл("stored.txt", окуу_жазуу | 없으면만들기 | 내용비우기, 0600);
    if (Файл < 0 || жазуу_файл_берилмелер(Файл, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Файл) < 0) return 2;
    if (жабуу_файл(Файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **увядзенне_Спіс) {
    (void)개수; (void)увядзенне_Спіс;
    int Файл = адкрыць_файл("stored.txt", для_чытання_для_запісу | 없으면만들기 | 내용비우기, 0600);
    if (Файл < 0 || напісаць_файл_дадзеныя(Файл, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Файл) < 0) return 2;
    if (закрыць_файл(Файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

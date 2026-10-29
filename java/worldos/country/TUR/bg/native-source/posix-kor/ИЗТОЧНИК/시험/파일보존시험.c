#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **запис_Списък) {
    (void)개수; (void)запис_Списък;
    int Файл = отварям_Файл("stored.txt", 읽고쓰기 | 없으면만들기 | съкращавам_Съдържание, 0600);
    if (Файл < 0 || записване_Файл_данни(Файл, "saved-from-C", 12) != 12) return 1;
    if (фиксиране_място_за_съхранение_на_файлове(Файл) < 0) return 2;
    if (затварям_Файл(Файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

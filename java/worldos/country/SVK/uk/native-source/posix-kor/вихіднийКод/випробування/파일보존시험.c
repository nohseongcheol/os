#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **запис_список) {
    (void)개수; (void)запис_список;
    int файл = відкрито_Файл("stored.txt", 읽고쓰기 | 없으면만들기 | скорочувати_Зміст, 0600);
    if (файл < 0 || записування_Файл_дані(файл, "saved-from-C", 12) != 12) return 1;
    if (затвердження_файлове_сховище(файл) < 0) return 2;
    if (Закрити_Файл(файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

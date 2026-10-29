#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **енгізу_Тізім) {
    (void)개수; (void)енгізу_Тізім;
    int Файл = ашу_файл("stored.txt", оқу_жазу | 없으면만들기 | қысқарту_Мазмұны, 0600);
    if (Файл < 0 || жазу_файл_деректер(Файл, "saved-from-C", 12) != 12) return 1;
    if (бекіту_файл_сақтау_орны(Файл) < 0) return 2;
    if (Жабу_файл(Файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

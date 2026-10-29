#include <файл_ABI.h>
#include <stdio.h>
int main(int товар_СЧЁТ, char **ввод_Список) {
    (void)товар_СЧЁТ; (void)ввод_Список;
    int файл = открыть_файл("stored.txt", для_чтения_и_записи | 없으면만들기 | усечь_Оглавление, 0600);
    if (файл < 0 || запись_файл_данные(файл, "saved-from-C", 12) != 12) return 1;
    if (фиксация_Файлы(файл) < 0) return 2;
    if (Close_файл(файл) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

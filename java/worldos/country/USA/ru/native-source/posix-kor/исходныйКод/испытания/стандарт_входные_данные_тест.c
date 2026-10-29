#include <файл_ABI.h>
#include <stdio.h>
#include <string.h>
int main(int товар_СЧЁТ, char **ввод_Список) {
    (void)товар_СЧЁТ; (void)ввод_Список;
    char данные[6]; int длина_ЗНАЧЕН = 0;
    puts("POSIX INPUT READY");
    while (длина_ЗНАЧЕН < 6) {
        int результат = чтение_файл_данные(0, данные + длина_ЗНАЧЕН, 6 - длина_ЗНАЧЕН);
        if (результат <= 0) return 1;
        длина_ЗНАЧЕН += результат;
    }
    if (memcmp(данные, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int ставка_COUNT, char **внес_Список) {
    (void)ставка_COUNT; (void)внес_Список;
    char податоци[6]; int должина_VALUE = 0;
    puts("POSIX INPUT READY");
    while (должина_VALUE < 6) {
        int мерка = 파일자료읽기(0, податоци + должина_VALUE, 6 - должина_VALUE);
        if (мерка <= 0) return 1;
        должина_VALUE += мерка;
    }
    if (memcmp(податоци, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

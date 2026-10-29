#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ndebà_ndepụta) {
    (void)개수; (void)ndebà_ndepụta;
    char datà[6]; int ogologo_valuu = 0;
    puts("POSIX INPUT READY");
    while (ogologo_valuu < 6) {
        int 결과 = 파일자료읽기(0, datà + ogologo_valuu, 6 - ogologo_valuu);
        if (결과 <= 0) return 1;
        ogologo_valuu += 결과;
    }
    if (memcmp(datà, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

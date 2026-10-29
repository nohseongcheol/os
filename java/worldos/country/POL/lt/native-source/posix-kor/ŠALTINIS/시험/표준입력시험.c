#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int prekė_COUNT, char **įrašas_Sąrašas) {
    (void)prekė_COUNT; (void)įrašas_Sąrašas;
    char duomenys[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int REZULTATAS = 파일자료읽기(0, duomenys + 길이, 6 - 길이);
        if (REZULTATAS <= 0) return 1;
        길이 += REZULTATAS;
    }
    if (memcmp(duomenys, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

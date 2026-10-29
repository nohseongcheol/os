#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int element_COUNT, char **daxiletmə_Siyahı) {
    (void)element_COUNT; (void)daxiletmə_Siyahı;
    char verilənlər[6]; int uzunluq_VALUE = 0;
    puts("POSIX INPUT READY");
    while (uzunluq_VALUE < 6) {
        int ölçü = 파일자료읽기(0, verilənlər + uzunluq_VALUE, 6 - uzunluq_VALUE);
        if (ölçü <= 0) return 1;
        uzunluq_VALUE += ölçü;
    }
    if (memcmp(verilənlər, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

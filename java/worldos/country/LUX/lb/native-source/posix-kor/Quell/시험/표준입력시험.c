#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int Element_COUNT, char **Agab_Lëscht) {
    (void)Element_COUNT; (void)Agab_Lëscht;
    char Daten[6]; int Längt_VALUE = 0;
    puts("POSIX INPUT READY");
    while (Längt_VALUE < 6) {
        int Mooss = 파일자료읽기(0, Daten + Längt_VALUE, 6 - Längt_VALUE);
        if (Mooss <= 0) return 1;
        Längt_VALUE += Mooss;
    }
    if (memcmp(Daten, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

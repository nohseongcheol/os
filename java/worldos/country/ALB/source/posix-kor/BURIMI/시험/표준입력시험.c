#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int njësi_COUNT, char **futje_Listë) {
    (void)njësi_COUNT; (void)futje_Listë;
    char të_dhëna[6]; int gjatësi_VALUE = 0;
    puts("POSIX INPUT READY");
    while (gjatësi_VALUE < 6) {
        int llogaritje = 파일자료읽기(0, të_dhëna + gjatësi_VALUE, 6 - gjatësi_VALUE);
        if (llogaritje <= 0) return 1;
        gjatësi_VALUE += llogaritje;
    }
    if (memcmp(të_dhëna, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

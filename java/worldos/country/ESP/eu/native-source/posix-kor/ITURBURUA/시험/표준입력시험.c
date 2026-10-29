#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int elementu_ZENBATU, char **sarrera_Zerrenda) {
    (void)elementu_ZENBATU; (void)sarrera_Zerrenda;
    char datuak[6]; int luzera_balio = 0;
    puts("POSIX INPUT READY");
    while (luzera_balio < 6) {
        int EMAITZA = 파일자료읽기(0, datuak + luzera_balio, 6 - luzera_balio);
        if (EMAITZA <= 0) return 1;
        luzera_balio += EMAITZA;
    }
    if (memcmp(datuak, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

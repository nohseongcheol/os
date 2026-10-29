#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int item_AANTAL, char **invoer_Lijst_f07b3200) {
    (void)item_AANTAL; (void)invoer_Lijst_f07b3200;
    char gegevens[6]; int tijdsduur_WAARDE = 0;
    puts("POSIX INPUT READY");
    while (tijdsduur_WAARDE < 6) {
        int resultaat = 파일자료읽기(0, gegevens + tijdsduur_WAARDE, 6 - tijdsduur_WAARDE);
        if (resultaat <= 0) return 1;
        tijdsduur_WAARDE += resultaat;
    }
    if (memcmp(gegevens, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

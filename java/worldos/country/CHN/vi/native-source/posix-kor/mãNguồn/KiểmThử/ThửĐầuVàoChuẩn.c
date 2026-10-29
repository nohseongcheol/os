#include <ABITệp.h>
#include <stdio.h>
#include <string.h>
int main(int sốLượngPhầnMục, char **danhSáchMục) {
    (void)sốLượngPhầnMục; (void)danhSáchMục;
    char DữLiệu[6]; int độDài = 0;
    puts("POSIX INPUT READY");
    while (độDài < 6) {
        int kếtQuả = đọcDữLiệuTệp(0, DữLiệu + độDài, 6 - độDài);
        if (kếtQuả <= 0) return 1;
        độDài += kếtQuả;
    }
    if (memcmp(DữLiệu, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

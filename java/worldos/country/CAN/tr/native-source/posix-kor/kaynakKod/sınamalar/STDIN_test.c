#include <Dosya_ABI.h>
#include <stdio.h>
#include <string.h>
int main(int öğe_BAĞ_DEĞ_SAY, char **girdi_Liste) {
    (void)öğe_BAĞ_DEĞ_SAY; (void)girdi_Liste;
    char veri[6]; int süre_değer = 0;
    puts("POSIX INPUT READY");
    while (süre_değer < 6) {
        int sonuç = 파일자료읽기(0, veri + süre_değer, 6 - süre_değer);
        if (sonuç <= 0) return 1;
        süre_değer += sonuç;
    }
    if (memcmp(veri, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

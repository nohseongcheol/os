#include <파일규약.h>
#include <stdio.h>
int main(int elementu_ZENBATU, char **sarrera_Zerrenda) {
    (void)elementu_ZENBATU; (void)sarrera_Zerrenda;
    int Fitxategia = ireki_fitxategi("stored.txt", irakurri_idatzi | 없으면만들기 | 내용비우기, 0600);
    if (Fitxategia < 0 || idatzi_fitxategi_datuak(Fitxategia, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fitxategia) < 0) return 2;
    if (itxi_fitxategi(Fitxategia) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

#include <파일규약.h>
#include <stdio.h>
int main(int stavka_COUNT, char **unos_spisak) {
    (void)stavka_COUNT; (void)unos_spisak;
    int Fajl = kreirati_fajl("stored.txt", i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Fajl < 0 || pisati_fajl_podaci(Fajl, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fajl) < 0) return 2;
    if (zatvoriti_fajl(Fajl) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

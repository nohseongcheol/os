#include <파일규약.h>
#include <stdio.h>
int main(int cikk_DARAB, char **bejegyzés_Lista) {
    (void)cikk_DARAB; (void)bejegyzés_Lista;
    int Fájl = készít_Fájl("stored.txt", 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600);
    if (Fájl < 0 || ír_Fájl_adat(Fájl, "saved-from-C", 12) != 12) return 1;
    if (véglegesít_Files(Fájl) < 0) return 2;
    if (bezár_Fájl(Fájl) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

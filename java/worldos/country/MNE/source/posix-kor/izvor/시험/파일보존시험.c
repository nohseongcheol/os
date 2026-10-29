#include <파일규약.h>
#include <stdio.h>
int main(int stavka_COUNT, char **stavka_Lista) {
    (void)stavka_COUNT; (void)stavka_Lista;
    int Datoteka = otvoren_Datoteka("stored.txt", za_čitanje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Datoteka < 0 || 파일자료쓰기(Datoteka, "saved-from-C", 12) != 12) return 1;
    if (izvršavanje_skladište_datoteka(Datoteka) < 0) return 2;
    if (Zatvori_Datoteka(Datoteka) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

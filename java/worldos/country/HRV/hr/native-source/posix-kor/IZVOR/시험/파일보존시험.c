#include <파일규약.h>
#include <stdio.h>
int main(int artikl_COUNT, char **unos_Popis) {
    (void)artikl_COUNT; (void)unos_Popis;
    int Datoteka = otvoreno_Datoteka("stored.txt", 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600);
    if (Datoteka < 0 || zapisivanje_Datoteka_podaci(Datoteka, "saved-from-C", 12) != 12) return 1;
    if (izvršavanje_pohrana_datoteka(Datoteka) < 0) return 2;
    if (Zatvori_Datoteka(Datoteka) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

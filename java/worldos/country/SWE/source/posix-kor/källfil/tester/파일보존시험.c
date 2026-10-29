#include <파일규약.h>
#include <stdio.h>
int main(int objekt_ANTAL, char **post_ange) {
    (void)objekt_ANTAL; (void)post_ange;
    int filnamn = skapa_fil("stored.txt", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600);
    if (filnamn < 0 || skriva_fil_data(filnamn, "saved-from-C", 12) != 12) return 1;
    if (incheckning_Files(filnamn) < 0) return 2;
    if (Stäng_fil(filnamn) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

#include <파일규약.h>
#include <stdio.h>
int main(int prekė_COUNT, char **įrašas_Sąrašas) {
    (void)prekė_COUNT; (void)įrašas_Sąrašas;
    int Failas = kurti_Failas("stored.txt", 읽고쓰기 | 없으면만들기 | trumpinti_Turinys, 0600);
    if (Failas < 0 || rašymas_Failas_duomenys(Failas, "saved-from-C", 12) != 12) return 1;
    if (vykdymas_failų_saugykla(Failas) < 0) return 2;
    if (Uždaryti_Failas(Failas) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

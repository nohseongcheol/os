#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **Iliniku_Titiqpalliagaq) {
    (void)개수; (void)Iliniku_Titiqpalliagaq;
    int ini = matuirli_ini("stored.txt", uqalimaarli_titirarli | 없으면만들기 | 내용비우기, 0600);
    if (ini < 0 || titiraq_ini_titiqqat(ini, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ini) < 0) return 2;
    if (matuli_ini(ini) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

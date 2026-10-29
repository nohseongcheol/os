#include <파일규약.h>
#include <stdio.h>
int main(int element_COUNT, char **entrata_Lista) {
    (void)element_COUNT; (void)entrata_Lista;
    int fajl = fetaħ_fajl("stored.txt", qari_kitba | 없으면만들기 | 내용비우기, 0600);
    if (fajl < 0 || kiteb_fajl_data(fajl, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(fajl) < 0) return 2;
    if (agħlaq_fajl(fajl) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

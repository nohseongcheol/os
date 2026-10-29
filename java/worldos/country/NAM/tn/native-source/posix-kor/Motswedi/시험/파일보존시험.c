#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **tsenyo_lenaane) {
    (void)개수; (void)tsenyo_lenaane;
    int faele = bula_faele("stored.txt", buisa_kwala | 없으면만들기 | 내용비우기, 0600);
    if (faele < 0 || kwala_faele_tshedimosetso(faele, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(faele) < 0) return 2;
    if (tswala_faele(faele) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

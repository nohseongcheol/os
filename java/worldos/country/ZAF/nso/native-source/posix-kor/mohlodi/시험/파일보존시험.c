#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **go_tsenya_tshedimošo_Lenaneo) {
    (void)개수; (void)go_tsenya_tshedimošo_Lenaneo;
    int Faele = bula_faele("stored.txt", bala_ngwala | 없으면만들기 | 내용비우기, 0600);
    if (Faele < 0 || ngwala_faele_data(Faele, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Faele) < 0) return 2;
    if (tswalela_faele(Faele) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

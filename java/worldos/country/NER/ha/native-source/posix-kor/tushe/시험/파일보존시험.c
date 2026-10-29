#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **Mashigar_bayanai_Jeri) {
    (void)개수; (void)Mashigar_bayanai_Jeri;
    int Fayil = buɗe_Fayil("stored.txt", Rubutuwa_karantuwa | 없으면만들기 | 내용비우기, 0600);
    if (Fayil < 0 || Rubuta_Fayil_Tarin_bayani(Fayil, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fayil) < 0) return 2;
    if (Rufe_Fayil(Fayil) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

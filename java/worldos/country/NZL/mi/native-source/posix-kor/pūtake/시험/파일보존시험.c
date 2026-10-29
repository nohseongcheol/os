#include <파일규약.h>
#include <stdio.h>
int main(int tuemi_COUNT, char **tāurunga_Rārangi) {
    (void)tuemi_COUNT; (void)tāurunga_Rārangi;
    int Kōnae = tiwhikete_kōnae("stored.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (Kōnae < 0 || tuhi_kōnae_raraunga(Kōnae, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Kōnae) < 0) return 2;
    if (kati_kōnae(Kōnae) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

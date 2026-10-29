#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **girizmeklik_Sanaw) {
    (void)개수; (void)girizmeklik_Sanaw;
    int Faýl = aç_faýl("stored.txt", okalýan_ýazylýan | 없으면만들기 | 내용비우기, 0600);
    if (Faýl < 0 || ýaz_faýl_maglumat(Faýl, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Faýl) < 0) return 2;
    if (ýap_faýl(Faýl) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

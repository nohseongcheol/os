#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **dugal_xabaar_lim) {
    (void)개수; (void)dugal_xabaar_lim;
    int bara_denc = sos_bara_denc("stored.txt", jàng_bind | 없으면만들기 | 내용비우기, 0600);
    if (bara_denc < 0 || biir_bara_denc_mbir(bara_denc, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(bara_denc) < 0) return 2;
    if (Tej_bara_denc(bara_denc) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

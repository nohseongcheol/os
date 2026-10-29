#include <파일규약.h>
#include <stdio.h>
int main(int item_COUNT, char **pemasukan_Senarai) {
    (void)item_COUNT; (void)pemasukan_Senarai;
    int Fail = buka_fail("stored.txt", baca_tulis | 없으면만들기 | potong_TOC, 0600);
    if (Fail < 0 || tulis_fail_data(Fail, "saved-from-C", 12) != 12) return 1;
    if (lakukan_storan_fail(Fail) < 0) return 2;
    if (Tutup_fail(Fail) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int item_COUNT, char **entri_Daftar) {
    (void)item_COUNT; (void)entri_Daftar;
    char data[6]; int panjang_VALUE = 0;
    puts("POSIX INPUT READY");
    while (panjang_VALUE < 6) {
        int hasil = 파일자료읽기(0, data + panjang_VALUE, 6 - panjang_VALUE);
        if (hasil <= 0) return 1;
        panjang_VALUE += hasil;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

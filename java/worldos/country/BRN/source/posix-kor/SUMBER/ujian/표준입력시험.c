#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int item_COUNT, char **pemasukan_Senarai) {
    (void)item_COUNT; (void)pemasukan_Senarai;
    char data[6]; int kepanjangan_VALUE = 0;
    puts("POSIX INPUT READY");
    while (kepanjangan_VALUE < 6) {
        int ukuran = 파일자료읽기(0, data + kepanjangan_VALUE, 6 - kepanjangan_VALUE);
        if (ukuran <= 0) return 1;
        kepanjangan_VALUE += ukuran;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

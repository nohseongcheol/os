#include <檔案ABI.h>
#include <stdio.h>
#include <string.h>
int main(int 項目個數, char **條目列表) {
    (void)項目個數; (void)條目列表;
    char 資料[6]; int 長度 = 0;
    puts("POSIX INPUT READY");
    while (長度 < 6) {
        int 結果 = 讀取檔案資料(0, 資料 + 長度, 6 - 長度);
        if (結果 <= 0) return 1;
        長度 += 結果;
    }
    if (memcmp(資料, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

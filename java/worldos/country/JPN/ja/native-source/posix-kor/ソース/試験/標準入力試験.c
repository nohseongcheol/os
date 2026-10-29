#include <ファイルABI.h>
#include <stdio.h>
#include <string.h>
int main(int 項目個数, char **入口一覧) {
    (void)項目個数; (void)入口一覧;
    char データ[6]; int 長さ = 0;
    puts("POSIX INPUT READY");
    while (長さ < 6) {
        int 結果 = ファイルデータ読取(0, データ + 長さ, 6 - 長さ);
        if (結果 <= 0) return 1;
        長さ += 結果;
    }
    if (memcmp(データ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}

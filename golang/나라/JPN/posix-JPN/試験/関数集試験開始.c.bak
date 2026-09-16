#include <入出力と実行.h>
int 関数集の動作を試す(void);
int main(void)
{
    int 失敗行番号 = 関数集の動作を試す();
    if (失敗行番号) {
        char 資料緩衝領域[16];
        int 長さ = 0;
        書く(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { 資料緩衝領域[長さ++] = (char)('0' + 失敗行番号 % 10); 失敗行番号 /= 10; } while (失敗行番号);
        while (長さ) 書く(1, &資料緩衝領域[--長さ], 1);
        書く(1, "\n", 1);
        return 1;
    }
    return 書く(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}

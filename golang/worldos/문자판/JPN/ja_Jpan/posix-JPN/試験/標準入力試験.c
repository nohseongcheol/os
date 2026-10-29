#include <入出力と実行.h>

static void 電文を書く(const char *文字列, unsigned int 大きさ)
{
    (void)書く(標準出力番号, 文字列, 大きさ);
}

int main(void)
{
    char 入力位置[4];
    符号付き大きさ型 数量;

    電文を書く("\nPOSIX-STDIN:READY\n", 19);
    数量 = 読む(標準入力番号, 入力位置, sizeof(入力位置));
    if (数量 == 2 && 入力位置[0] == 'a' && 入力位置[1] == '\n') {
        電文を書く("POSIX-STDIN:PASS\n", 17);
        直ちに終了する(0);
    }
    電文を書く("POSIX-STDIN:FAIL\n", 17);
    直ちに終了する(1);
}

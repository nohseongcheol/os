#include <誤り番号.h>
#include <文書制御.h>
#include <体系/子の待機.h>
#include <入出力と実行.h>

static void 電文を書く(const char *文字列, unsigned int 大きさ)
{
    (void)書く(標準出力番号, 文字列, 大きさ);
}

int main(void)
{
    int 終了状態;
    int 文書記述番号;
    char *引数一覧[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *環境一覧[] = {(char *)"POSIX_TEST=1", (char *)0};

    電文を書く("\nPOSIX-EXEC:START\n", 18);
    誤り番号 = 0;
    if (指定した子を待つ(-1, &終了状態, 未準備なら待たない) == -1 && 誤り番号 == 誤り子実行過程なし)
        電文を書く("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        電文を書く("PTEST:FAIL:waitpid-echild-empty\n", 32);
    誤り番号 = 0;
    if (子を待つ(&終了状態) == -1 && 誤り番号 == 誤り子実行過程なし)
        電文を書く("PTEST:PASS:wait-echild-empty\n", 29);
    else
        電文を書く("PTEST:FAIL:wait-echild-empty\n", 29);

    文書記述番号 = 開く("/USER2", 読取専用で開く);
    if (文書記述番号 < 0 || 指定番号に文書参照を複製する(文書記述番号, 10) != 10 || 文書を制御する(10, 記述番号標識設定, 実行内容置換時に閉じる) != 0) {
        電文を書く("PTEST:FAIL:cloexec-setup\n", 25);
        直ちに終了する(98);
    }
    if (文書記述番号 != 10)
        (void)閉じる(文書記述番号);

    (void)実行内容を置き換える("/PXEXEC", 引数一覧, 環境一覧);
    電文を書く("PTEST:FAIL:exec-image\n", 22);
    直ちに終了する(99);
}

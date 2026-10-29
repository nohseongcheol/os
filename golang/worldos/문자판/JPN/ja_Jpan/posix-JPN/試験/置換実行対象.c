#include <誤り番号.h>
#include <文書制御.h>
#include <入出力と実行.h>

static int 文字列一致判定(const char *左の値, const char *右の値)
{
    unsigned int 項の添字 = 0;
    while (左の値[項の添字] != 0 && 右の値[項の添字] != 0) {
        if (左の値[項の添字] != 右の値[項の添字])
            return 0;
        項の添字++;
    }
    return 左の値[項の添字] == 右の値[項の添字];
}

int main(int 引数の数, char **引数一覧, char **環境一覧)
{
    static const char 読込値[] = "PTEST:PASS:exec-image\n";
    static const char 引数検査成功[] = "PTEST:PASS:exec-argv-envp\n";
    static const char 引数検査失敗[] = "PTEST:FAIL:exec-argv-envp\n";

    (void)書く(標準出力番号, 読込値, sizeof(読込値) - 1);
    if (引数の数 == 2 && 引数一覧 != (char **)0 && 環境一覧 != (char **)0 &&
        引数一覧[0] != (char *)0 && 引数一覧[1] != (char *)0 && 引数一覧[2] == (char *)0 &&
        環境一覧[0] != (char *)0 && 環境一覧[1] == (char *)0 &&
        環境変数一覧 == 環境一覧 && 文字列一致判定(引数一覧[0], "PXEXEC") &&
        文字列一致判定(引数一覧[1], "argument") && 文字列一致判定(環境一覧[0], "POSIX_TEST=1")) {
        (void)書く(標準出力番号, 引数検査成功, sizeof(引数検査成功) - 1);
    } else {
        (void)書く(標準出力番号, 引数検査失敗, sizeof(引数検査失敗) - 1);
        直ちに終了する(38);
    }
    誤り番号 = 0;
    if (文書を制御する(10, 記述番号標識取得) == -1 && 誤り番号 == 誤り記述番号不正) {
        static const char 実行置換時閉鎖成功[] = "PTEST:PASS:cloexec\n";
        (void)書く(標準出力番号, 実行置換時閉鎖成功, sizeof(実行置換時閉鎖成功) - 1);
        直ちに終了する(37);
    }
    {
        static const char 実行置換時閉鎖失敗[] = "PTEST:FAIL:cloexec\n";
        (void)書く(標準出力番号, 実行置換時閉鎖失敗, sizeof(実行置換時閉鎖失敗) - 1);
    }
    直ちに終了する(39);
}

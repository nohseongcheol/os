#include <ファイルABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 引数列個数, char **引数一覧) {
    if (引数列個数 < 1 || !引数一覧[0]) return 2;
    const char 挨拶文[] = "内蔵 커널의 C와 日本語 POSIX\n";
    int 文書 = ファイル開放("挨拶例.txt", 読取書込 | 作成条件未存在 | 切詰め内容, 0600);
    if (文書 < 0) return 1;
    入出力結果型 長さ = ファイルデータ書込(文書, 挨拶文, sizeof(挨拶文) - 1);
    ファイル閉鎖(文書);
    ファイルデータ書込(1, 挨拶文, sizeof(挨拶文) - 1);
    return 長さ == sizeof(挨拶文) - 1 ? 0 : 3;
}

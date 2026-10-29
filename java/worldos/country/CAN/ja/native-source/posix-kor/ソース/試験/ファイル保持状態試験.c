#include <ファイルABI.h>
#include <stdio.h>
int main(int 項目個数, char **入口一覧) {
    (void)項目個数; (void)入口一覧;
    int ファイル = ファイル開放("stored.txt", 読取書込 | 作成条件未存在 | 切詰め内容, 0600);
    if (ファイル < 0 || ファイルデータ書込(ファイル, "saved-from-C", 12) != 12) return 1;
    if (確定ファイル記憶装置(ファイル) < 0) return 2;
    if (ファイル閉鎖(ファイル) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

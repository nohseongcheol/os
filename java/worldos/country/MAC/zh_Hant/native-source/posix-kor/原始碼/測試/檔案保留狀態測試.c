#include <檔案ABI.h>
#include <stdio.h>
int main(int 項目個數, char **條目列表) {
    (void)項目個數; (void)條目列表;
    int 檔案 = 打開檔案("stored.txt", 讀取寫入 | 創建條件缺失 | 截斷內容, 0600);
    if (檔案 < 0 || 寫入檔案資料(檔案, "saved-from-C", 12) != 12) return 1;
    if (提交檔案存儲裝置(檔案) < 0) return 2;
    if (關閉檔案(檔案) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

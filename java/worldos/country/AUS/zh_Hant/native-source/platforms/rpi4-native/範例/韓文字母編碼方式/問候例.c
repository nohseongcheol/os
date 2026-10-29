#include "檔案ABI.h"
int 開始用戶程式(int 實參) {
    (void)實參;
    const char 問候語[] = "C에서 한글 이름과 posix-kor 調用\n";
    int 文檔集 = 打開檔案("C인사.txt", 讀取寫入 | 創建條件缺失 | 截斷內容, 0600);
    if (文檔集 < 0) return 1;
    輸入輸出結果類型 已記錄個數 = 寫入檔案資料(文檔集, 問候語, sizeof(問候語) - 1);
    關閉檔案(文檔集);
    寫入檔案資料(1, 問候語, sizeof(問候語) - 1);
    return 已記錄個數 == sizeof(問候語) - 1 ? 0 : 2;
}

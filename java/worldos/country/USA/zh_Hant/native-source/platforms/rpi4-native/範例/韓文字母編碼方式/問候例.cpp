#include "檔案ABI.h"
class 文檔管理器 {
    int 編號;
public:
    文檔管理器(const char *名稱) : 編號(打開檔案(名稱, 讀取寫入 | 創建條件缺失 | 截斷內容, 0600)) {}
    ~文檔管理器() { if (編號 >= 0) 關閉檔案(編號); }
    輸入輸出結果類型 寫入(const char *資料, 位元組個數類型 大小) { return 寫入檔案資料(編號, 資料, 大小); }
};
extern "C" int 開始用戶程式(int 實參) {
    (void)實參;
    const char 問候語[] = "C++에서 한글 클래스와 posix-kor 調用\n";
    文檔管理器 文檔集("C++問候例.txt");
    寫入檔案資料(1, 問候語, sizeof(問候語) - 1);
    return 文檔集.寫入(問候語, sizeof(問候語) - 1) == sizeof(問候語) - 1 ? 0 : 1;
}

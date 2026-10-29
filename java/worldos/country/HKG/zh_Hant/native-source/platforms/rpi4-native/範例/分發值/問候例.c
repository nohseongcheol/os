#include <檔案ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 參數列個數, char **實際參數列表) {
    if (參數列個數 < 1 || !實際參數列表[0]) return 2;
    const char 問候語[] = "內建 커널의 C와 中文 POSIX\n";
    int 文檔集 = 打開檔案("問候例.txt", 讀取寫入 | 創建條件缺失 | 截斷內容, 0600);
    if (文檔集 < 0) return 1;
    輸入輸出結果類型 長度 = 寫入檔案資料(文檔集, 問候語, sizeof(問候語) - 1);
    關閉檔案(文檔集);
    寫入檔案資料(1, 問候語, sizeof(問候語) - 1);
    return 長度 == sizeof(問候語) - 1 ? 0 : 3;
}

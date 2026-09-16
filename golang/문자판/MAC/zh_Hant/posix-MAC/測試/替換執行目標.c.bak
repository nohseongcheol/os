#include <錯誤編號.h>
#include <檔案控制.h>
#include <輸入輸出與執行.h>

static int 檢查文字相等(const char *左值, const char *右值)
{
    unsigned int 項目索引 = 0;
    while (左值[項目索引] != 0 && 右值[項目索引] != 0) {
        if (左值[項目索引] != 右值[項目索引])
            return 0;
        項目索引++;
    }
    return 左值[項目索引] == 右值[項目索引];
}

int main(int 引數數量, char **引數列表, char **環境列表)
{
    static const char 載入值[] = "PTEST:PASS:exec-image\n";
    static const char 引數檢查成功[] = "PTEST:PASS:exec-argv-envp\n";
    static const char 引數檢查失敗[] = "PTEST:FAIL:exec-argv-envp\n";

    (void)寫入(標準輸出編號, 載入值, sizeof(載入值) - 1);
    if (引數數量 == 2 && 引數列表 != (char **)0 && 環境列表 != (char **)0 &&
        引數列表[0] != (char *)0 && 引數列表[1] != (char *)0 && 引數列表[2] == (char *)0 &&
        環境列表[0] != (char *)0 && 環境列表[1] == (char *)0 &&
        環境變數列表 == 環境列表 && 檢查文字相等(引數列表[0], "PXEXEC") &&
        檢查文字相等(引數列表[1], "argument") && 檢查文字相等(環境列表[0], "POSIX_TEST=1")) {
        (void)寫入(標準輸出編號, 引數檢查成功, sizeof(引數檢查成功) - 1);
    } else {
        (void)寫入(標準輸出編號, 引數檢查失敗, sizeof(引數檢查失敗) - 1);
        立即結束(38);
    }
    錯誤編號 = 0;
    if (控制檔案(10, 取得描述編號旗標) == -1 && 錯誤編號 == 錯誤描述編號無效) {
        static const char 程式替換時關閉成功[] = "PTEST:PASS:cloexec\n";
        (void)寫入(標準輸出編號, 程式替換時關閉成功, sizeof(程式替換時關閉成功) - 1);
        立即結束(37);
    }
    {
        static const char 程式替換時關閉失敗[] = "PTEST:FAIL:cloexec\n";
        (void)寫入(標準輸出編號, 程式替換時關閉失敗, sizeof(程式替換時關閉失敗) - 1);
    }
    立即結束(39);
}

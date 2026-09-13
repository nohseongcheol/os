#include <錯誤編號.h>
#include <檔案控制.h>
#include <系統/子行程等待.h>
#include <輸入輸出與執行.h>

static void 寫出訊息(const char *字串, unsigned int 大小)
{
    (void)寫入(標準輸出編號, 字串, 大小);
}

int main(void)
{
    int 結束狀態;
    int 檔案描述編號;
    char *引數列表[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *環境列表[] = {(char *)"POSIX_TEST=1", (char *)0};

    寫出訊息("\nPOSIX-EXEC:START\n", 18);
    錯誤編號 = 0;
    if (等待指定子行程(-1, &結束狀態, 未就緒則不等待) == -1 && 錯誤編號 == 錯誤沒有子行程)
        寫出訊息("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        寫出訊息("PTEST:FAIL:waitpid-echild-empty\n", 32);
    錯誤編號 = 0;
    if (等待子行程(&結束狀態) == -1 && 錯誤編號 == 錯誤沒有子行程)
        寫出訊息("PTEST:PASS:wait-echild-empty\n", 29);
    else
        寫出訊息("PTEST:FAIL:wait-echild-empty\n", 29);

    檔案描述編號 = 開啟("/USER2", 唯讀開啟);
    if (檔案描述編號 < 0 || 按指定編號複製檔案參照(檔案描述編號, 10) != 10 || 控制檔案(10, 設定描述編號旗標, 替換程式時關閉) != 0) {
        寫出訊息("PTEST:FAIL:cloexec-setup\n", 25);
        立即結束(98);
    }
    if (檔案描述編號 != 10)
        (void)關閉(檔案描述編號);

    (void)替換執行內容("/PXEXEC", 引數列表, 環境列表);
    寫出訊息("PTEST:FAIL:exec-image\n", 22);
    立即結束(99);
}

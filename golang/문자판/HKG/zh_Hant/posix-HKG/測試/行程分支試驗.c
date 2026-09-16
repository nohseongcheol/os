/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <系統/子行程等待.h>
#include <檔案控制.h>
#include <輸入輸出與執行.h>

static void 寫出訊息(const char *字串, unsigned int 大小)
{
    (void)寫入(標準輸出編號, 字串, 大小);
}

int main(void)
{
    int 結束狀態;
    行程編號型別 父行程 = 取得行程編號();
    行程編號型別 子項位置;
    行程編號型別 已等待行程;
    volatile int 行程私有值 = 10;
    int 檔案描述編號;
    char 位元組值;
    int 迭代次數;

    寫出訊息("\nPOSIX-FORK:START\n", 18);
    子項位置 = 分出子行程();
    if (子項位置 == 0) {
        行程私有值 = 20;
        if (取得父行程編號() != 父行程 || 行程私有值 != 20)
            立即結束(90);
        立即結束(23);
    }
    if (子項位置 < 0) {
        寫出訊息("PTEST:FAIL:fork-return\n", 23);
        立即結束(1);
    }
    寫出訊息("PTEST:PASS:fork-return\n", 23);
    已等待行程 = 等待指定子行程(子項位置, &結束狀態, 0);
    if (已等待行程 == 子項位置 && 檢查正常結束(結束狀態) && 提取結束值(結束狀態) == 23 &&
        行程私有值 == 10) {
        寫出訊息("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        寫出訊息("PTEST:FAIL:fork-wait-exit\n", 26);
        立即結束(1);
    }

    子項位置 = 分出子行程();
    if (子項位置 == 0)
        立即結束(29);
    已等待行程 = 等待子行程(&結束狀態);
    if (已等待行程 == 子項位置 && 檢查正常結束(結束狀態) && 提取結束值(結束狀態) == 29)
        寫出訊息("PTEST:PASS:blocking-wait\n", 25);
    else {
        寫出訊息("PTEST:FAIL:blocking-wait\n", 25);
        立即結束(1);
    }

    檔案描述編號 = 開啟("/USER2", 唯讀開啟);
    子項位置 = 分出子行程();
    if (子項位置 == 0) {
        (void)關閉(檔案描述編號);
        立即結束(0);
    }
    已等待行程 = 等待指定子行程(子項位置, &結束狀態, 0);
    if (檔案描述編號 >= 0 && 已等待行程 == 子項位置 && 讀取(檔案描述編號, &位元組值, 1) == 1 &&
        (unsigned char)位元組值 == 0x7f)
        寫出訊息("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        寫出訊息("PTEST:FAIL:fork-fd-isolation\n", 29);
        立即結束(1);
    }
    (void)關閉(檔案描述編號);

    for (迭代次數 = 0; 迭代次數 < 2; 迭代次數++) {
        子項位置 = 分出子行程();
        if (子項位置 == 0)
            立即結束(迭代次數);
        if (子項位置 < 0 || 等待指定子行程(子項位置, &結束狀態, 0) != 子項位置 ||
            !檢查正常結束(結束狀態) || 提取結束值(結束狀態) != 迭代次數) {
            寫出訊息("PTEST:FAIL:fork-stress\n", 23);
            立即結束(1);
        }
    }
    寫出訊息("PTEST:PASS:fork-stress\n", 23);
    寫出訊息("POSIX-FORK:PASS\n", 16);
    立即結束(0);
}

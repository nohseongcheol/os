#include <系統/子行程等待.h>
#include <輸入輸出與執行.h>

static void 寫出訊息(const char *字串, unsigned int 大小)
{
    (void)寫入(標準輸出編號, 字串, 大小);
}

int main(void)
{
    volatile unsigned char *起始位置 = (volatile unsigned char *)移動動態記憶末端(0);
    volatile unsigned char *記憶體區域;
    行程編號型別 子項位置;
    int 結束狀態;

    寫出訊息("\nPOSIX-HEAP:START\n", 18);
    記憶體區域 = (volatile unsigned char *)移動動態記憶末端(32);
    if (起始位置 == (void *)-1 || 記憶體區域 != 起始位置 || 移動動態記憶末端(0) != (void *)(起始位置 + 32)) {
        寫出訊息("PTEST:FAIL:sbrk-grow\n", 22);
        立即結束(1);
    }
    寫出訊息("PTEST:PASS:sbrk-grow\n", 22);
    記憶體區域[0] = 0x5a;
    記憶體區域[31] = 0xa5;
    if (記憶體區域[0] != 0x5a || 記憶體區域[31] != 0xa5) {
        寫出訊息("PTEST:FAIL:sbrk-memory\n", 24);
        立即結束(1);
    }
    寫出訊息("PTEST:PASS:sbrk-memory\n", 24);
    if (設定動態記憶末端((void *)起始位置) != 0 || 移動動態記憶末端(0) != (void *)起始位置) {
        寫出訊息("PTEST:FAIL:brk-restore\n", 24);
        立即結束(1);
    }
    寫出訊息("PTEST:PASS:brk-restore\n", 24);

    子項位置 = 分出子行程();
    if (子項位置 == 0) {
        if (移動動態記憶末端(64) != (void *)起始位置)
            立即結束(2);
        立即結束(0);
    }
    if (子項位置 < 0 || 等待指定子行程(子項位置, &結束狀態, 0) != 子項位置 ||
        !檢查正常結束(結束狀態) || 提取結束值(結束狀態) != 0 ||
        移動動態記憶末端(0) != (void *)起始位置) {
        寫出訊息("PTEST:FAIL:brk-process-isolation\n", 33);
        立即結束(1);
    }
    寫出訊息("PTEST:PASS:brk-process-isolation\n", 33);
    寫出訊息("POSIX-HEAP:PASS\n", 16);
    立即結束(0);
}

#include <輸入輸出與執行.h>

static void 寫出訊息(const char *字串, unsigned int 大小)
{
    (void)寫入(標準輸出編號, 字串, 大小);
}

int main(void)
{
    char 輸入位置[4];
    有號大小型別 數量;

    寫出訊息("\nPOSIX-STDIN:READY\n", 19);
    數量 = 讀取(標準輸入編號, 輸入位置, sizeof(輸入位置));
    if (數量 == 2 && 輸入位置[0] == 'a' && 輸入位置[1] == '\n') {
        寫出訊息("POSIX-STDIN:PASS\n", 17);
        立即結束(0);
    }
    寫出訊息("POSIX-STDIN:FAIL\n", 17);
    立即結束(1);
}

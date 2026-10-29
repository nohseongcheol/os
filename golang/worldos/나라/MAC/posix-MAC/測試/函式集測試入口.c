#include <輸入輸出與執行.h>
int 測試函式集行為(void);
int main(void)
{
    int 失敗行號 = 測試函式集行為();
    if (失敗行號) {
        char 資料緩衝區域[16];
        int 長度 = 0;
        寫入(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { 資料緩衝區域[長度++] = (char)('0' + 失敗行號 % 10); 失敗行號 /= 10; } while (失敗行號);
        while (長度) 寫入(1, &資料緩衝區域[--長度], 1);
        寫入(1, "\n", 1);
        return 1;
    }
    return 寫入(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}

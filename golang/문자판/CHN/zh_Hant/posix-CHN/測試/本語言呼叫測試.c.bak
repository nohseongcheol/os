#include <輸入輸出與執行.h>
#include <檔案控制.h>
#include <錯誤編號.h>
#include <系統/檔案狀態.h>
int 測試函式集行為(void);

int main(void)
{
    char 資料緩衝區域[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int 檔案描述編號 = 開啟("/USER2", 唯讀開啟);
    struct 檔案狀態 狀態資料;
    if (檔案描述編號 < 0 || 取得開啟檔案狀態(檔案描述編號, &狀態資料) < 0 || 讀取(檔案描述編號, 資料緩衝區域, 4) != 4 ||
        (unsigned char)資料緩衝區域[0] != 0x7f || 資料緩衝區域[1] != 'E' || 資料緩衝區域[2] != 'L' || 資料緩衝區域[3] != 'F' ||
        移動讀寫位置(檔案描述編號, 0, 從起點定位) != 0 || 關閉(檔案描述編號) < 0 || 取得行程編號() <= 0)
        goto 失敗旗標;
    錯誤編號 = 0;
    if (讀取(-1, 資料緩衝區域, 1) != -1 || 錯誤編號 != 錯誤描述編號無效)
        goto 失敗旗標;
    if (測試函式集行為() != 0)
        goto 失敗旗標;
    if (寫入(標準輸出編號, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto 失敗旗標;
    return 0;
失敗旗標:
    寫入(標準輸出編號, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}

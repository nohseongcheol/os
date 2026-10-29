#include "檔案ABI.h"
#include "調用.h"
static int 初始設定器值;
static volatile int 初始設定器種子 = 72;
static volatile double 浮點型分種子 = 1.25;
static int 銷燬狀態個數;
struct 測試初始化 { 測試初始化() { 初始設定器值 = 初始設定器種子 + 1; } } 初始化靜態區;
class 自動化檔案 {
    int 編號;
public:
    explicit 自動化檔案(const char *名稱) : 編號(打開檔案(名稱, 讀取寫入 | 創建條件缺失 | 截斷內容, 0600)) {}
    ~自動化檔案() { if (編號 >= 0) 關閉檔案(編號); 銷燬狀態個數++; }
    int 描述符條目() const { return 編號; }
};
extern "C" int 開始用戶程式(int) {
    if (初始設定器值 != 73 || 用戶調用(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 浮點型分值 = 浮點型分種子 * 2.0 + 0.5;
    if (用戶調用(0, 0, 0, 0, 0, 0, 0) != 1 || 浮點型分值 != 3.0) return 16;
    static const char 內容值[] = "EL0 C++ → posix-kor → Java 檔案 · 안녕하세요 😀\n";
    char 讀取值[sizeof(內容值)] = {};
    {
        自動化檔案 檔案("使用者.txt");
        int 編號 = 檔案.描述符條目();
        if (編號 < 0 || 寫入檔案資料(編號, 內容值, sizeof(內容值)) != sizeof(內容值)) return 2;
        if (尋道檔案(編號, 0, 起點開頭) || 讀取檔案資料(編號, 讀取值, sizeof(讀取值)) != sizeof(讀取值)) return 3;
        for (unsigned 序數索引 = 0; 序數索引 < sizeof(內容值); 序數索引++) if (讀取值[序數索引] != 內容值[序數索引]) return 4;
    }
    if (銷燬狀態個數 != 1) return 5;
    if (寫入檔案資料(1, 內容值, sizeof(內容值) - 1) != sizeof(內容值) - 1) return 6;
    uintptr_t 底端條目 = 用戶記憶體結束(0);
    if (底端條目 != 0x02c00000 || 用戶記憶體結束(底端條目 + 8192) != (intptr_t)(底端條目 + 8192)) return 7;
    volatile unsigned char *記憶體 = (volatile unsigned char *)底端條目;
    if (記憶體[0] || 記憶體[8191]) return 8;
    記憶體[8191] = 137;
    if (用戶記憶體結束(底端條目) != (intptr_t)底端條目 || 用戶記憶體結束(底端條目 + 8192) != (intptr_t)(底端條目 + 8192) || 記憶體[8191]) return 9;
    // 잘못된 使用者 指針/번호는 오류이며 커널을 중단하지 않는다.
    if (寫入檔案資料(1, (const void *)0x80000, 8) != -1 || 錯誤編號 != 14) return 10;
    if (讀取檔案資料(0, (void *)內容值, 1) != -1 || 錯誤編號 != 14) return 11;
    if (用戶調用(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 屏幕跨度 = 讀取屏幕寬度(), 屏幕長度 = 讀取屏幕高度();
    if (屏幕跨度 <= 0 || 屏幕長度 <= 0 || 用戶調用(13, 屏幕跨度-1, 屏幕長度-1, 0, 2, 2, 0) != -22) return 13;
    if (屏幕矩形(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 退出程式 시 열린 서술자가 자동 정리되어야 한다.
    if (打開檔案("使用者.txt", 讀取僅用值) < 0) return 15;
    return 0;
}

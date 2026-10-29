#include "../命名/計算機連接名稱列.h"
#include "屏幕信息.h"
// EL0 執行命令 計算機 層值. 檔案 資料/정책은 기존 AOT Java 커널에 위임한다.
#include "使用者.h"
#include "檔案ABI.h"
#include "網路ABI.h"
#include "../通信網絡/通信網絡.h"
extern int32_t Java網絡遠程(int32_t), Java流地址(int32_t);
#define 計算機寄存器(首位值) (*(volatile uint32_t *)(uintptr_t)(首位值))
#define 中斷分發器 0xff841000ul
#define 中斷CPU接口 0xff842000ul
#define 頁大小 4096ul
#define 存取標記 (1ul << 10)
#define 無執行權限 (1ul << 53)
#define 用戶無執行 (1ul << 54)
#define 常規記憶體 ((1ul << 2) | (3ul << 8) | 存取標記)
#define 內核頁 (3ul | 常規記憶體 | 無執行權限 | 用戶無執行)
#define 用戶讀取寫入 (3ul | 常規記憶體 | (1ul << 6) | 無執行權限 | 用戶無執行)
#define 用戶讀取僅用 (3ul | 常規記憶體 | (3ul << 6) | 無執行權限 | 用戶無執行)
#define 用戶讀取執行 (3ul | 常規記憶體 | (3ul << 6) | 無執行權限)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 板寫字符(uintptr_t), 板取字符(void), 板經過毫秒(void);
extern uintptr_t 板像素(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 板幀緩衝(void);
extern uintptr_t 板終端(uintptr_t);
extern int 終端待處理(void);
extern int32_t Java交互殼交互式(void);
extern int32_t Java路徑開始(int32_t), Java路徑位元組(int32_t,int32_t);
extern int32_t Java創建目錄(void), Java移除目錄(void), Java條目種類(void);
extern int 調用屏幕(int,unsigned,int,int,int,int,int),屏幕文本(int,int,const uint32_t *,unsigned);
extern void 初始化屏幕(int),屏幕按下(int,unsigned);
extern int 用戶恢復執行(用戶幀 *,void *);
extern void 用戶浮點保存(void *);
extern int 用戶進入(uintptr_t 條目分, uintptr_t 棧存儲裝置, uintptr_t 已轉發值);
extern void 用戶發回(void);
extern void 內核致命停止(const char *) __attribute__((noreturn));
static uint64_t 根地址[512] __attribute__((aligned(4096)));
static uint64_t 中間[4][512] __attribute__((aligned(4096)));
static uint64_t 頁列表[用戶頁個數] __attribute__((aligned(4096)));
static uint8_t 權限列列表[用戶頁個數];
static int 活躍, 檔案列表[16], Linux調用約定;
static unsigned 通訊端端點列[24];
extern int32_t Java網絡通訊端(int32_t, int32_t, int32_t), Java網絡綁定(int32_t, int32_t, int32_t);
extern int32_t Java網絡放入(int32_t, int32_t), Java網絡獲取(int32_t), Java網絡發送(int32_t, int32_t, int32_t, int32_t);
extern int32_t Java網絡接收操作(int32_t, int32_t), Java網絡埠(int32_t), Java網絡地址(int32_t), Java網絡對端(int32_t), Java網絡關閉(int32_t);
extern int32_t Java流創建(void),Java流綁定(int32_t,int32_t,int32_t),Java流偵聽(int32_t,int32_t),Java流連接(int32_t,int32_t,int32_t),Java流接受(int32_t),Java流讀取(int32_t,int32_t),Java流寫入(int32_t,int32_t),Java流埠(int32_t),Java流對端(int32_t),Java流關閉(int32_t);
static int 關閉通訊端端點(unsigned 檔案句柄){return 檔案句柄<40?Java網絡關閉(檔案句柄):Java流關閉(檔案句柄);}
static uint64_t 頻率, 截止時間時間;
static uintptr_t 堆結束;
// 內核值 셸이 준비한 UTF-8 實參. EL0에는 複製值 호출만 제공한다.
static unsigned 已轉發實際參數個數, 已轉發實際參數長度[8];
static unsigned char 已轉發實際參數[8][256];
typedef struct {
    int 已暫停狀態,交互式,Linux調用約定,檔案列表[16]; unsigned 通訊端端點列[24],參數列個數,參數長度[8];
    unsigned char 實際參數陣列[8][256],權限列列表[用戶頁個數];
    uintptr_t 堆存儲裝置; 用戶幀 執行狀態幀;
    unsigned char 浮點型分狀態[528] __attribute__((aligned(16)));
} 已保存程序;
static 已保存程序 已保存[4];
static int 所有者物件,交互式;
static uint32_t 用戶編號[4], 用戶開始時間[4], 用戶累積時間[4], 用戶執行狀態時間[4], 下一用戶編號=10;
static unsigned char 用戶命令名稱[4][288];
uint32_t 讀取用戶狀態(unsigned 條目值, unsigned 編號) {
    unsigned 位置索引=編號&3;
    int 狀態值=(活躍 && 所有者物件==(int)位置索引) ? 1 : 已保存[位置索引].已暫停狀態 ? 2 : 0;
    if (條目值==0) return 狀態值;
    if (!狀態值) return 0;
    if (條目值==1) return 用戶編號[位置索引];
    if (條目值==2) {
        unsigned char *頁面列列表=狀態值==1?權限列列表:已保存[位置索引].權限列列表;
        unsigned 頁個數=0; for (unsigned 序數索引=0; 序數索引<用戶頁個數; 序數索引++) if(頁面列列表[序數索引]) 頁個數++;
        return 頁個數*4;
    }
    if (條目值==3) return (uint32_t)板經過毫秒()-用戶開始時間[位置索引];
    if (條目值==4) return 用戶累積時間[位置索引]+(狀態值==1?(uint32_t)板經過毫秒()-用戶執行狀態時間[位置索引]:0);
    if (條目值==5) return 編號/4<sizeof(用戶命令名稱[0])?用戶命令名稱[位置索引][編號/4]:0;
    return 0;
}
uintptr_t 板調用參數開始位置(uintptr_t 條目個數) {
    if (活躍 || 條目個數 > 8) return (uint32_t)-22;
    已轉發實際參數個數 = 條目個數;
    memset(已轉發實際參數長度, 0, sizeof(已轉發實際參數長度));
    memset(已轉發實際參數, 0, sizeof(已轉發實際參數));
    return 0;
}
uintptr_t 板調用參數位元組(uintptr_t 查找索引, uintptr_t 當前位置, uintptr_t 位元組資料) {
    if (活躍 || 查找索引 >= 已轉發實際參數個數 || 當前位置 >= 255 || 當前位置 != 已轉發實際參數長度[查找索引] || !位元組資料 || 位元組資料 > 255)
        return (uint32_t)-22;
    已轉發實際參數[查找索引][當前位置] = 位元組資料;
    已轉發實際參數長度[查找索引] = 當前位置 + 1;
    return 0;
}
static void 同步表列(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t 時鐘值(void) { uint64_t 臨時資料; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(臨時資料)); return 臨時資料; }
static void 停止超時(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    計算機寄存器(中斷分發器 + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 開始超時(void) {
    uint64_t 間距值 = 頻率 * 2, 啓用 = 1;
    截止時間時間 = 時鐘值() + 間距值;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(間距值), "r"(啓用) : "memory");
}
void 用戶系統初始化操作(void) {
    for (unsigned 資料塊 = 0; 資料塊 < 4; 資料塊++) {
        根地址[資料塊] = (uintptr_t)中間[資料塊] | 3;
        for (unsigned 序數索引 = 0; 序數索引 < 512; 序數索引++) {
            uintptr_t 地址 = ((uintptr_t)資料塊 << 30) | ((uintptr_t)序數索引 << 21);
            中間[資料塊][序數索引] = 地址 | 1 | 存取標記 | 用戶無執行;
            if (地址 >= 0xfc000000ul) 中間[資料塊][序數索引] |= 無執行權限; // Device-nGnRnE
            else 中間[資料塊][序數索引] |= 常規記憶體; // Normal, non-cacheable
        }
    }
    for (unsigned 第二值 = 0; 第二值 < 用戶頁個數 / 512; 第二值++)
        中間[0][(用戶基底 >> 21) + 第二值] = (uintptr_t)(頁列表 + 第二值 * 512) | 3;
    for (unsigned 序數索引 = 0; 序數索引 < 用戶頁個數; 序數索引++) 頁列表[序數索引] = (用戶基底 + 序數索引 * 頁大小) | 內核頁;
    uint64_t 記憶體屬性寄存器 = 0x4400, 地址翻譯控制 = 32 | (3ul << 12) | (1ul << 23), 系統控制寄存器;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(記憶體屬性寄存器), "r"(地址翻譯控制), "r"((uintptr_t)根地址) : "memory");
    同步表列();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(系統控制寄存器));
    系統控制寄存器 = (系統控制寄存器 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(系統控制寄存器) : "memory");
    uint64_t 浮點型分狀態 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(浮點型分狀態) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(頻率));
    停止超時();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 條目分值 때만 允許值.
    計算機寄存器(中斷分發器) = 0;
    計算機寄存器(中斷分發器 + 0x180) = 0xffffffff;
    計算機寄存器(中斷分發器 + 0x80) = 0xffffffff;
    計算機寄存器(中斷分發器 + 0x280) = 1u << 30;
    計算機寄存器(中斷分發器 + 0x41c) = 0x80808080;
    計算機寄存器(中斷分發器 + 0x100) = 1u << 30;
    計算機寄存器(中斷CPU接口 + 4) = 0xff;
    計算機寄存器(中斷CPU接口 + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 是否常規 확인할 數 있다.
    int 安全性 = (計算機寄存器(中斷分發器 + 4) & (1u << 10)) != 0;
    計算機寄存器(中斷分發器) = 安全性 ? 1 : 3;
    計算機寄存器(中斷CPU接口) = 安全性 ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 標識碼[16]; uint16_t 類型分類, 計算機類型; uint32_t 版本編號;
    uint64_t 條目分, 程式標頭偏移, 區段標頭偏移; uint32_t 配置項位元列;
    uint16_t 可執行文件標頭大小, 程式標頭條目大小, 程式標頭個數, 區段標頭條目大小, 區段標頭個數, 區段名稱表索引;
} ELF標頭;
typedef struct { uint32_t 類型分類, 配置項位元列; uint64_t 偏移值, 地址, 物理地址, 文件區域大小, 內存區大小, 對齊邊界位置; } ELF程式;
_Static_assert(sizeof(ELF標頭) == 64 && sizeof(ELF程式) == 56, "ELF layout");
_Static_assert(sizeof(用戶幀) == 272, "exception assembly layout");
static int 已包含(uint64_t 偏移值, uint64_t 大小, uint64_t 結束偏移) {
    return 偏移值 <= 結束偏移 && 大小 <= 結束偏移 - 偏移值;
}
static int 檢查輔助信息(const unsigned char *資料位置, size_t 大小) {
    size_t 當前位置 = 0;
    while (已包含(當前位置, 12, 大小)) {
        uint32_t 詞法用單詞列[3]; memcpy(詞法用單詞列, 資料位置 + 當前位置, 12); 當前位置 += 12;
        uint64_t 名稱區域大小 = ((uint64_t)詞法用單詞列[0] + 3) & ~3ul;
        uint64_t 描述區大小 = ((uint64_t)詞法用單詞列[1] + 3) & ~3ul;
        if (!已包含(當前位置, 名稱區域大小, 大小) || !已包含(當前位置 + 名稱區域大小, 描述區大小, 大小)) return 0;
        const unsigned char 名稱[] = {'J','K','O','R','O','S',0};
        int 是否相等 = 詞法用單詞列[0] == sizeof(名稱) && 詞法用單詞列[1] == 4 && 詞法用單詞列[2] == 1;
        if (是否相等) for (unsigned 序數索引 = 0; 序數索引 < sizeof(名稱); 序數索引++) if (資料位置[當前位置 + 序數索引] != 名稱[序數索引]) 是否相等 = 0;
        uint32_t 版本編號 = 0;
        if (是否相等) memcpy(&版本編號, 資料位置 + 當前位置 + 名稱區域大小, 4);
        if (是否相等 && 版本編號 == 1) return 1;
        當前位置 += 名稱區域大小 + 描述區大小;
    }
    return 0;
}
static int 有效性校驗ELF(const unsigned char *資料, size_t 大小, int Linux模式) {
    if (大小 < sizeof(ELF標頭)) return 用戶可執行文件錯誤;
    ELF標頭 可執行文件標頭; memcpy(&可執行文件標頭, 資料, sizeof(可執行文件標頭));
    if (可執行文件標頭.標識碼[0] != 127 || 可執行文件標頭.標識碼[1] != 'E' || 可執行文件標頭.標識碼[2] != 'L' || 可執行文件標頭.標識碼[3] != 'F' ||
        可執行文件標頭.標識碼[4] != 2 || 可執行文件標頭.標識碼[5] != 1 || 可執行文件標頭.標識碼[6] != 1 || (可執行文件標頭.標識碼[7] != 0 && (!Linux模式 || 可執行文件標頭.標識碼[7] != 3)) ||
        可執行文件標頭.類型分類 != 2 || 可執行文件標頭.計算機類型 != 183 || 可執行文件標頭.版本編號 != 1 || 可執行文件標頭.配置項位元列 || 可執行文件標頭.可執行文件標頭大小 != sizeof(可執行文件標頭) ||
        可執行文件標頭.程式標頭條目大小 != sizeof(ELF程式) || !可執行文件標頭.程式標頭個數 || 可執行文件標頭.程式標頭個數 > 16 ||
        可執行文件標頭.程式標頭偏移 < sizeof(可執行文件標頭) || !已包含(可執行文件標頭.程式標頭偏移, (uint64_t)可執行文件標頭.程式標頭個數 * sizeof(ELF程式), 大小)) return 用戶可執行文件錯誤;
    uint8_t 已使用容量[(用戶映像結束 - 用戶基底) / 頁大小] = {0};
    int 有效條目分 = 0, ABI正常確認 = 0, 載入項 = 0;
    for (unsigned 序數索引 = 0; 序數索引 < 可執行文件標頭.程式標頭個數; 序數索引++) {
        ELF程式 資料位置; memcpy(&資料位置, 資料 + 可執行文件標頭.程式標頭偏移 + 序數索引 * sizeof(資料位置), sizeof(資料位置));
        if (資料位置.類型分類 == 4) {
            if (!已包含(資料位置.偏移值, 資料位置.文件區域大小, 大小)) return 用戶可執行文件錯誤;
            if (檢查輔助信息(資料 + 資料位置.偏移值, 資料位置.文件區域大小)) ABI正常確認 = 1;
            continue;
        }
        if (資料位置.類型分類 == 0 || 資料位置.類型分類 == 6 || (資料位置.類型分類 == 0x6474e551 && !(資料位置.配置項位元列 & 1))) continue;
        if (資料位置.類型分類 != 1) return 用戶可執行文件錯誤; // PT_INTERP, DYNAMIC, TLS 是否不支持
        if (!資料位置.內存區大小) continue;
        if (資料位置.配置項位元列 & ~7u || !(資料位置.配置項位元列 & 4) || (資料位置.配置項位元列 & 3) == 3 || 資料位置.文件區域大小 > 資料位置.內存區大小 ||
            (資料位置.文件區域大小 && !已包含(資料位置.偏移值, 資料位置.文件區域大小, 大小)) || 資料位置.地址 < 用戶基底 ||
            !已包含(資料位置.地址, 資料位置.內存區大小, 用戶映像結束) ||
            (!Linux模式 && ((資料位置.地址 & (頁大小 - 1)) || (資料位置.偏移值 & (頁大小 - 1)) || 資料位置.對齊邊界位置 != 頁大小)) ||
            (Linux模式 && (((資料位置.地址 ^ 資料位置.偏移值) & (頁大小 - 1)) || !資料位置.對齊邊界位置 ||
                (資料位置.對齊邊界位置 & (資料位置.對齊邊界位置 - 1)) || 資料位置.對齊邊界位置 > 0x200000 || ((資料位置.地址 ^ 資料位置.偏移值) & (資料位置.對齊邊界位置 - 1))))) return 用戶可執行文件錯誤;
        unsigned 首位條目 = (資料位置.地址 - 用戶基底) / 頁大小;
        unsigned 條目個數 = ((資料位置.地址 & (頁大小 - 1)) + 資料位置.內存區大小 + 頁大小 - 1) / 頁大小;
        for (unsigned 頁值 = 首位條目; 頁值 < 首位條目 + 條目個數; 頁值++) {
            if (已使用容量[頁值]) return 用戶可執行文件錯誤;
            已使用容量[頁值] = 1;
        }
        if ((資料位置.配置項位元列 & 1) && 可執行文件標頭.條目分 >= 資料位置.地址 && 可執行文件標頭.條目分 < 資料位置.地址 + 資料位置.文件區域大小 && !(可執行文件標頭.條目分 & 3)) 有效條目分 = 1;
        載入項++;
    }
    return 有效條目分 && (Linux模式 ? !ABI正常確認 : ABI正常確認) && 載入項 ? 0 : 用戶可執行文件錯誤;
}
int 用戶有效性校驗ELF(const unsigned char *資料, size_t 大小) { return 有效性校驗ELF(資料, 大小, 0); }
static void 頁導航(uintptr_t 地址, uint64_t 配置項位元列, unsigned 存取權限列) {
    unsigned 查找索引 = (地址 - 用戶基底) / 頁大小;
    頁列表[查找索引] = 地址 | 配置項位元列;
    權限列列表[查找索引] = 存取權限列;
}
static int 用戶範圍(uintptr_t 地址, size_t 條目個數, int 寫入中) {
    if (地址 < 用戶基底 || !已包含(地址, 條目個數, 用戶結束)) return 0;
    if (!條目個數) return 1;
    unsigned 首位條目 = (地址 - 用戶基底) / 頁大小, 最後項目 = (地址 + 條目個數 - 1 - 用戶基底) / 頁大小;
    for (unsigned 序數索引 = 首位條目; 序數索引 <= 最後項目; 序數索引++) if (!(權限列列表[序數索引] & (寫入中 ? 2 : 1))) return 0;
    return 1;
}
static int 複製路徑(uintptr_t 地址, char *路徑) {
    for (unsigned 序數索引 = 0; 序數索引 < 65; 序數索引++) {
        if (!用戶範圍(地址, 1, 0)) return -14;
        路徑[序數索引] = *(const char *)地址++;
        if (!路徑[序數索引]) return 0;
    }
    return -36;
}
static intptr_t 內核結果(intptr_t 結果) { return 結果 < 0 ? -錯誤編號 : 結果; }
static int 已映射文件描述符(uint64_t 檔案句柄) { return 檔案句柄 >= 3 && 檔案句柄 < 19 ? 檔案列表[檔案句柄 - 3] : -1; }
static int 通訊端端點所有者(uint64_t 檔案句柄) { return 檔案句柄 >= 32 && 檔案句柄 < 56 && 通訊端端點列[檔案句柄 - 32]; }
static int 地址輸入(uintptr_t 指向中值, size_t 長度, struct pk_sockaddr_in *地址) {
    if (長度 != sizeof(*地址)) return -22;
    if (!用戶範圍(指向中值, 長度, 0)) return -14;
    memcpy(地址, (const void *)指向中值, sizeof(*地址));
    return 地址->sin_family == AF_INET ? 0 : -97;
}
static int 地址輸出檢查(uintptr_t 指向中值, uintptr_t 長度指針, pk_socklen_t *緩衝區容量) {
    if (!用戶範圍(長度指針, sizeof(*緩衝區容量), 1)) return -14;
    memcpy(緩衝區容量, (const void *)長度指針, sizeof(*緩衝區容量));
    if (*緩衝區容量 > sizeof(struct pk_sockaddr_in)) *緩衝區容量 = sizeof(struct pk_sockaddr_in);
    if (*緩衝區容量 && !用戶範圍(指向中值, *緩衝區容量, 1)) return -14;
    return 0;
}
static void 地址輸出(uintptr_t 指向中值, uintptr_t 長度指針, pk_socklen_t 緩衝區容量, int 地址, int 埠編號) {
    struct pk_sockaddr_in 值; memset(&值, 0, sizeof(值));
    值.sin_family = AF_INET; 值.sin_port = pk_htons(埠編號); 值.sin_addr.s_addr = pk_htonl(地址);
    if (緩衝區容量) memcpy((void *)指向中值, &值, 緩衝區容量);
    pk_socklen_t 長度 = sizeof(值); memcpy((void *)長度指針, &長度, sizeof(長度));
}
extern uintptr_t 板信道(uintptr_t, uintptr_t);
static intptr_t 原生系統呼叫(用戶幀 *檔案條目) {
    uintptr_t 首位值 = 檔案條目->寄存器資料[0], 第二值 = 檔案條目->寄存器資料[1], 字元程式碼 = 檔案條目->寄存器資料[2];
    char 路徑[65];
    int 檔案句柄, 結果;
    switch (檔案條目->寄存器資料[8]) {
    case 0: return 1; // 內建 ABI 버전
    case 1: // write: 指針 전체를 검사한 後端值 輸出/檔案 更改值
        if (字元程式碼 > 65536) return -22;
        if (!用戶範圍(第二值, 字元程式碼, 0)) return -14;
        if (首位值 == 1 || 首位值 == 2) {
            uint64_t 開始輸出=時鐘值();
            for (size_t 序數索引 = 0; 序數索引 < 字元程式碼; 序數索引++) 板信道(首位值, ((const unsigned char *)第二值)[序數索引]);
            /* 큰 tty를 그린 內核值 시간만 돌려준다. EL0 計算結果 기한은 늘리지 않는다. */
            if(交互式){
                截止時間時間+=時鐘值()-開始輸出;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(截止時間時間) : "memory");
            }
            return 字元程式碼;
        }
        if(首位值>=40&&通訊端端點所有者(首位值)){
            size_t 項目個數=字元程式碼>512?512:字元程式碼;for(size_t 序數索引=0;序數索引<項目個數;序數索引++)Java網絡放入(序數索引,((const unsigned char *)第二值)[序數索引]);return Java流寫入(首位值,項目個數);
        }
        檔案句柄 = 已映射文件描述符(首位值); if (檔案句柄 < 0) return -9;
        return 內核結果(pk_write(檔案句柄, (const void *)第二值, 字元程式碼));
    case 2:
        if (字元程式碼 > 65536) return -22;
        if (!用戶範圍(第二值, 字元程式碼, 1)) return -14;
        if (首位值 == 0) {
            size_t 項目個數 = 0;
            while (項目個數 < 字元程式碼) {
                int 字元值 = (int32_t)板取字符(); if (字元值 == -2) return 項目個數; if (字元值 < 0) break;
                ((unsigned char *)第二值)[項目個數++] = 字元值;
            }
            return 項目個數 ? (intptr_t)項目個數 : (字元程式碼 ? -11 : 0);
        }
        if(首位值>=40&&通訊端端點所有者(首位值)){
            結果=Java流讀取(首位值,字元程式碼>512?512:字元程式碼);if(結果>0)for(int 序數索引=0;序數索引<結果;序數索引++)((unsigned char *)第二值)[序數索引]=Java網絡獲取(序數索引);return 結果;
        }
        檔案句柄 = 已映射文件描述符(首位值); if (檔案句柄 < 0) return -9;
        return 內核結果(pk_read(檔案句柄, (void *)第二值, 字元程式碼));
    case 3:
        結果 = 複製路徑(首位值, 路徑); if (結果) return 結果;
        if (第二值 > 0x7ff) return -22;
        for (unsigned 序數索引 = 0; 序數索引 < 16; 序數索引++) if (檔案列表[序數索引] < 0) {
            檔案句柄 = pk_open(路徑, (int)第二值, 0600);
            if (檔案句柄 < 0) return -錯誤編號;
            檔案列表[序數索引] = 檔案句柄; return 序數索引 + 3;
        }
        return -24;
    case 4:
        if (通訊端端點所有者(首位值)) { 結果 = 關閉通訊端端點(首位值); if (!結果) 通訊端端點列[首位值 - 32] = 0; return 結果; }
        檔案句柄 = 已映射文件描述符(首位值); if (檔案句柄 < 0) return -9;
        結果 = pk_close(檔案句柄); if (!結果) 檔案列表[首位值 - 3] = -1;
        return 內核結果(結果);
    case 5:
        檔案句柄 = 已映射文件描述符(首位值); if (檔案句柄 < 0) return -9;
        if (字元程式碼 > 2) return -22;
        return 內核結果(pk_lseek(檔案句柄, (int64_t)第二值, 字元程式碼));
    case 7: return 板經過毫秒();
    case 8: { // brk: 별도 使用者 RW/NX 堆值, 새로 노출되는 페이지는 0으로 初始化
        if (!首位值) return 堆結束;
        if (首位值 < 用戶映像結束 || 首位值 > 用戶堆結束) return -12;
        uintptr_t 舊頁面列 = (堆結束 + 頁大小 - 1) & ~(頁大小 - 1);
        uintptr_t 新建頁面列 = (首位值 + 頁大小 - 1) & ~(頁大小 - 1);
        if (新建頁面列 > 舊頁面列) {
            for (uintptr_t 資料位置 = 舊頁面列; 資料位置 < 新建頁面列; 資料位置 += 頁大小) 頁導航(資料位置, 內核頁, 0);
            同步表列();
            memset((void *)舊頁面列, 0, 新建頁面列 - 舊頁面列);
            for (uintptr_t 資料位置 = 舊頁面列; 資料位置 < 新建頁面列; 資料位置 += 頁大小) 頁導航(資料位置, 用戶讀取寫入, 3);
        } else {
            for (uintptr_t 資料位置 = 新建頁面列; 資料位置 < 舊頁面列; 資料位置 += 頁大小) {
                頁列表[(資料位置 - 用戶基底) / 頁大小] = 0; 權限列列表[(資料位置 - 用戶基底) / 頁大小] = 0;
            }
        }
        堆結束 = 首位值; 同步表列(); return 首位值;
    }
    case 9:
        檔案句柄 = 已映射文件描述符(首位值); return 檔案句柄 < 0 ? -9 : 內核結果(pk_size(檔案句柄));
    case 10:
        檔案句柄 = 已映射文件描述符(首位值); return 檔案句柄 < 0 ? -9 : 內核結果(pk_ftruncate(檔案句柄, (int64_t)第二值));
    case 11:
        結果 = 複製路徑(首位值, 路徑); return 結果 ? 結果 : 內核結果(pk_unlink(路徑));
    case 12:
        檔案句柄 = 已映射文件描述符(首位值); return 檔案句柄 < 0 ? -9 : 內核結果(pk_fsync(檔案句柄));
    case 13: { // 그래픽 기초 API: 使用者 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 已請求寬度值 = 檔案條目->寄存器資料[3], 已請求高度值 = 檔案條目->寄存器資料[4];
        if (!板幀緩衝()) return -19;
        uintptr_t 屏幕跨度 = 板屏幕寬度(), 屏幕長度 = 板屏幕高度();
        if (首位值 > 屏幕跨度 || 第二值 > 屏幕長度 || 已請求寬度值 > 屏幕跨度 - 首位值 || 已請求高度值 > 屏幕長度 - 第二值) return -22;
        for (uintptr_t Y_按鈕座標 = 第二值; Y_按鈕座標 < 第二值 + 已請求高度值; Y_按鈕座標++) for (uintptr_t 橫座標座標 = 首位值; 橫座標座標 < 首位值 + 已請求寬度值; 橫座標座標++) 板像素(橫座標座標, Y_按鈕座標, 字元程式碼);
        return 0;
    }
    case 14: return (int32_t)板取字符();
    case 15: // args(-1,0,0)=項目個數; args(index,buffer,capacity)=UTF-8 長度
        if (首位值 == UINTPTR_MAX) return 已轉發實際參數個數;
        if (首位值 >= 已轉發實際參數個數) return -22;
        if (字元程式碼 <= 已轉發實際參數長度[首位值]) return -36;
        if (!用戶範圍(第二值, 已轉發實際參數長度[首位值] + 1, 1)) return -14;
        memcpy((void *)第二值, 已轉發實際參數[首位值], 已轉發實際參數長度[首位值] + 1);
        return 已轉發實際參數長度[首位值];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(首位值==0){if(!Java交互殼交互式())return -95;交互式=1;return 板終端(13);}
        if(首位值==2){交互式=0;return 0;}
        if(首位值==3)return 板終端(13);
        if(首位值!=1||!交互式)return -22;
        結果=(int32_t)板取字符();
        if(結果==-4096)return 結果;
        開始超時();return 結果<0?-11:結果;
    case 17: { // 유한한 협력 等待狀態值: 通信 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (首位值 > 100) return -22;
        uint64_t 結束時間 = 時鐘值() + 頻率 * 首位值 / 1000;
        do { 審查網路(); 審查檔案傳送(); __asm__ volatile("yield"); } while (時鐘值() < 結束時間);
        開始超時(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 父值·빈 폴더를 검사한다.
        if (第二值 > 2) return -22;
        結果 = 複製路徑(首位值, 路徑); if (結果) return 結果;
        unsigned 長度 = 0; while (路徑[長度]) 長度++;
        結果 = Java路徑開始(長度); if (結果 < 0) return 結果;
        for (unsigned 序數索引 = 0; 序數索引 < 長度; 序數索引++) Java路徑位元組(序數索引, (unsigned char)路徑[序數索引]);
        return 第二值 == 0 ? Java條目種類() : 第二值 == 1 ? Java創建目錄() : Java移除目錄();
    }
    case 20:
        if(首位值==5){int 字元值=(int32_t)板取字符();if(字元值==-4096)return 字元值;if(字元值>=0)屏幕按下(所有者物件,字元值);開始超時();}
        if(首位值==3&&字元程式碼){if(!Java交互殼交互式())return -95;交互式=1;板終端(300);}
        return 調用屏幕(所有者物件,首位值,第二值,字元程式碼,檔案條目->寄存器資料[3],檔案條目->寄存器資料[4],檔案條目->寄存器資料[5]);
    case 21:
        if(字元程式碼>127)return -22;if(!用戶範圍(第二值,字元程式碼*sizeof(uint32_t),0))return -14;
        return 屏幕文本(所有者物件,首位值,(const uint32_t *)第二值,字元程式碼);
    case 22: // 屏幕 大小 查詢值: 0=寬度值, 1=高度值. 사용자에게 주소를 노출하지 않는다.
        if (首位值 > 1) return -22;
        if (!板幀緩衝()) return -19;
        return 首位值 == 0 ? 板屏幕寬度() : 板屏幕高度();
    case 32:
        if (首位值 != AF_INET) return -97;
        if(第二值==SOCK_STREAM&&(字元程式碼==0||字元程式碼==6))結果=Java流創建();
        else if(第二值==SOCK_DGRAM&&(字元程式碼==0||字元程式碼==IPPROTO_UDP))結果=Java網絡通訊端(首位值,第二值,字元程式碼);
        else return -93;
        if (結果 >= 32 && 結果 < 56) 通訊端端點列[結果 - 32] = 1;
        return 結果;
    case 33: {
        if (!通訊端端點所有者(首位值)) return -9;
        struct pk_sockaddr_in 地址;
        結果 = 地址輸入(第二值, 字元程式碼, &地址); if (結果) return 結果;
        return 首位值>=40?Java流綁定(首位值,pk_htonl(地址.sin_addr.s_addr),pk_htons(地址.sin_port)):Java網絡綁定(首位值, pk_htonl(地址.sin_addr.s_addr), pk_htons(地址.sin_port));
    }
    case 34: {
        if (!通訊端端點所有者(首位值)) return -9;
        if(首位值>=40)return -95;
        if (檔案條目->寄存器資料[3]) return -95;
        if (字元程式碼 > 512) return -90;
        if (字元程式碼 && !用戶範圍(第二值, 字元程式碼, 0)) return -14;
        struct pk_sockaddr_in 地址;
        結果 = 地址輸入(檔案條目->寄存器資料[4], 檔案條目->寄存器資料[5], &地址); if (結果) return 結果;
        for (unsigned 序數索引 = 0; 序數索引 < 字元程式碼; 序數索引++) Java網絡放入(序數索引, ((const unsigned char *)第二值)[序數索引]);
        return Java網絡發送(首位值, pk_htonl(地址.sin_addr.s_addr), pk_htons(地址.sin_port), 字元程式碼);
    }
    case 35: {
        if (!通訊端端點所有者(首位值)) return -9;
        if(首位值>=40)return -95;
        if (檔案條目->寄存器資料[3]) return -95;
        if (字元程式碼 > 512) return -90;
        if (字元程式碼 && !用戶範圍(第二值, 字元程式碼, 1)) return -14;
        pk_socklen_t 緩衝區容量 = 0;
        if (檔案條目->寄存器資料[4]) { 結果 = 地址輸出檢查(檔案條目->寄存器資料[4], 檔案條目->寄存器資料[5], &緩衝區容量); if (結果) return 結果; }
        結果 = Java網絡接收操作(首位值, 字元程式碼); if (結果 < 0) return 結果;
        for (int 序數索引 = 0; 序數索引 < 結果; 序數索引++) ((unsigned char *)第二值)[序數索引] = Java網絡獲取(序數索引);
        if (檔案條目->寄存器資料[4]) 地址輸出(檔案條目->寄存器資料[4], 檔案條目->寄存器資料[5], 緩衝區容量, Java網絡遠程(首位值), Java網絡對端(首位值));
        return 結果;
    }
    case 36: {
        if (!通訊端端點所有者(首位值)) return -9;
        pk_socklen_t 緩衝區容量;
        結果 = 地址輸出檢查(第二值, 字元程式碼, &緩衝區容量); if (結果) return 結果;
        地址輸出(第二值,字元程式碼,緩衝區容量,首位值>=40?Java流地址(首位值):Java網絡地址(首位值),首位值>=40?Java流埠(首位值):Java網絡埠(首位值)); return 0;
    }
    case 37: {
        if(首位值<40||!通訊端端點所有者(首位值))return -9;struct pk_sockaddr_in 地址;
        結果=地址輸入(第二值,字元程式碼,&地址);if(結果)return 結果;
        return Java流連接(首位值,pk_htonl(地址.sin_addr.s_addr),pk_htons(地址.sin_port));
    }
    case 38: return 首位值>=40&&通訊端端點所有者(首位值)?Java流偵聽(首位值,第二值):-9;
    case 39:
        if(首位值<40||!通訊端端點所有者(首位值))return -9;
        if(第二值||字元程式碼)return -95;結果=Java流接受(首位值);if(結果>=40&&結果<56)通訊端端點列[結果-32]=1;return 結果;
    case 40: return 首位值>=40&&通訊端端點所有者(首位值)?Java流對端(首位值):-9;
    default: return -38; // 是否不支持 기능을 성공으로 가장하지 않음
    }
}
#include "Linux兼容性.inc"
static intptr_t 系統呼叫(用戶幀 *檔案條目) {
    network_poll();
    return Linux調用約定 ? Linux系統呼叫(檔案條目) : 原生系統呼叫(檔案條目);
}
static void 發回內核(用戶幀 *檔案條目, int 結果) {
    停止超時();
    檔案條目->寄存器資料[0] = (uint64_t)(int64_t)結果;
    檔案條目->命令位置 = (uintptr_t)用戶發回;
    檔案條目->狀態程式碼 = 0x3c5; // EL1h, DAIF masked
}
int 用戶異常(用戶幀 *檔案條目, unsigned 攔截) {
    if (!活躍 || (檔案條目->狀態程式碼 & 15) != 0) return 0;
    if (攔截) {
        uint32_t 確認應答值 = 計算機寄存器(中斷CPU接口 + 0xc), 標識符值 = 確認應答值 & 1023;
        if (標識符值 == 30) { 發回內核(檔案條目, 用戶超時); 計算機寄存器(中斷CPU接口 + 0x10) = 確認應答值; return 1; }
        if (標識符值 < 1020) 計算機寄存器(中斷CPU接口 + 0x10) = 確認應答值;
        return 1;
    }
    uint64_t 異常狀態; __asm__ volatile("mrs %0, esr_el1" : "=r"(異常狀態));
    if (時鐘值() >= 截止時間時間) { 發回內核(檔案條目, 用戶超時); return 1; }
    unsigned 異常分類 = 異常狀態 >> 26;
    if (異常分類 == 0x15 && (異常狀態 & 0xffff) == 0) {
        if (Linux調用約定 ? 檔案條目->寄存器資料[8] == 93 || 檔案條目->寄存器資料[8] == 94 : 檔案條目->寄存器資料[8] == 6) 發回內核(檔案條目, (int)(檔案條目->寄存器資料[0] & 255));
        else {
            intptr_t 結果=系統呼叫(檔案條目);
            if(結果==-4096&&交互式){
                已保存[所有者物件].執行狀態幀=*檔案條目;已保存[所有者物件].執行狀態幀.命令位置-=4;
                用戶浮點保存(已保存[所有者物件].浮點型分狀態);發回內核(檔案條目,用戶已中斷);
            }else 檔案條目->寄存器資料[0]=(uint64_t)結果;
        }
    } else 發回內核(檔案條目, 異常分類 == 0x24 ? 用戶資料錯誤 : 異常分類 == 0x20 ? 用戶執行狀態錯誤 : 用戶無效指令);
    return 1;
}

// 생성된 const ELF 組值: 실행은 반드시 程式 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *資料; size_t 大小; unsigned 已轉發值; } 執行條目;
#include "programs.h"
static void *快照(unsigned 位置索引){return (void *)(0x04000000ul+位置索引*(用戶結束-用戶基底));}
static int 結束操作程式(int 結果){
    用戶累積時間[所有者物件]+=(uint32_t)板經過毫秒()-用戶執行狀態時間[所有者物件];
    停止超時();活躍=0;
    if(結果==用戶已中斷){
        已保存程序 *字符串資料=&已保存[所有者物件];字符串資料->已暫停狀態=1;字符串資料->交互式=交互式;字符串資料->Linux調用約定=Linux調用約定;字符串資料->堆存儲裝置=堆結束;字符串資料->參數列個數=已轉發實際參數個數;
        memcpy(字符串資料->權限列列表,權限列列表,sizeof(權限列列表));memcpy(字符串資料->檔案列表,檔案列表,sizeof(檔案列表));memcpy(字符串資料->通訊端端點列,通訊端端點列,sizeof(通訊端端點列));
        memcpy(字符串資料->實際參數陣列,已轉發實際參數,sizeof(已轉發實際參數));memcpy(字符串資料->參數長度,已轉發實際參數長度,sizeof(已轉發實際參數長度));
        for(unsigned 序數索引=0;序數索引<用戶頁個數;序數索引++)if(權限列列表[序數索引])memcpy((unsigned char *)快照(所有者物件)+序數索引*頁大小,(void *)(用戶基底+序數索引*頁大小),頁大小);
    }else{
        已保存[所有者物件].已暫停狀態=0;初始化屏幕(所有者物件);
        for(unsigned 序數索引=0;序數索引<16;序數索引++)if(檔案列表[序數索引]>=0)pk_close(檔案列表[序數索引]);
        for(unsigned 序數索引=0;序數索引<24;序數索引++)if(通訊端端點列[序數索引])關閉通訊端端點(序數索引+32);
    }
    for(unsigned 序數索引=0;序數索引<用戶頁個數;序數索引++){頁列表[序數索引]=0;權限列列表[序數索引]=0;}同步表列();return 結果;
}
uintptr_t 板用戶控制(uintptr_t 動作){
    unsigned 位置索引=動作&15;if(位置索引>=4||活躍)return (uint32_t)-22;
    已保存程序 *字符串資料=&已保存[位置索引];
    if(動作>=32){if(字符串資料->已暫停狀態){for(unsigned 序數索引=0;序數索引<16;序數索引++)if(字符串資料->檔案列表[序數索引]>=0)pk_close(字符串資料->檔案列表[序數索引]);for(unsigned 序數索引=0;序數索引<24;序數索引++)if(字符串資料->通訊端端點列[序數索引])關閉通訊端端點(序數索引+32);}字符串資料->已暫停狀態=0;初始化屏幕(位置索引);return 0;}
    if(動作>=16)return 字符串資料->已暫停狀態;
    if(!字符串資料->已暫停狀態)return (uint32_t)-22;
    所有者物件=位置索引;交互式=字符串資料->交互式;Linux調用約定=字符串資料->Linux調用約定;堆結束=字符串資料->堆存儲裝置;已轉發實際參數個數=字符串資料->參數列個數;
    memcpy(檔案列表,字符串資料->檔案列表,sizeof(檔案列表));memcpy(通訊端端點列,字符串資料->通訊端端點列,sizeof(通訊端端點列));memcpy(已轉發實際參數,字符串資料->實際參數陣列,sizeof(已轉發實際參數));memcpy(已轉發實際參數長度,字符串資料->參數長度,sizeof(已轉發實際參數長度));
    for(unsigned 序數索引=0;序數索引<用戶頁個數;序數索引++)頁列表[序數索引]=(用戶基底+序數索引*頁大小)|內核頁;同步表列();
    memset((void *)用戶基底,0,用戶結束-用戶基底);
    for(unsigned 序數索引=0;序數索引<用戶頁個數;序數索引++)if(字符串資料->權限列列表[序數索引])memcpy((void *)(用戶基底+序數索引*頁大小),(unsigned char *)快照(位置索引)+序數索引*頁大小,頁大小);
    memcpy(權限列列表,字符串資料->權限列列表,sizeof(權限列列表));
    for(unsigned 序數索引=0;序數索引<用戶頁個數;序數索引++){unsigned 資料位置=權限列列表[序數索引];頁列表[序數索引]=資料位置?(用戶基底+序數索引*頁大小)|(資料位置==3?用戶讀取寫入:資料位置==5?用戶讀取執行:用戶讀取僅用):0;}
    同步表列();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");活躍=1;字符串資料->已暫停狀態=0;開始超時();
    用戶執行狀態時間[所有者物件]=板經過毫秒();
    return (uint32_t)結束操作程式(用戶恢復執行(&字符串資料->執行狀態幀,字符串資料->浮點型分狀態));
}
static int 運行程式(const unsigned char *資料, size_t 大小, unsigned 已轉發值, int Linux模式, const char *名稱) {
    if (活躍) return -16;
    所有者物件=板終端(11);if(所有者物件<0||所有者物件>3||已保存[所有者物件].已暫停狀態)return -16;交互式=0;
    int 有效 = 有效性校驗ELF(資料, 大小, Linux模式); if (有效) return 有效;
    Linux調用約定 = Linux模式;
    unsigned 名稱索引=0;
    while (*名稱 && 名稱索引<31) 用戶命令名稱[所有者物件][名稱索引++]=(unsigned char)*名稱++;
    if (已轉發實際參數個數 && 已轉發實際參數長度[0]) {
        if (名稱索引) 用戶命令名稱[所有者物件][名稱索引++]=' ';
        for (unsigned 位置索引=0; 位置索引<已轉發實際參數長度[0]; 位置索引++) 用戶命令名稱[所有者物件][名稱索引++]=已轉發實際參數[0][位置索引];
    }
    用戶命令名稱[所有者物件][名稱索引]=0; 用戶編號[所有者物件]=下一用戶編號++;
    if (下一用戶編號>0x7fffffffu) 下一用戶編號=10;
    用戶開始時間[所有者物件]=板經過毫秒(); 用戶累積時間[所有者物件]=0;
    for (unsigned 序數索引 = 0; 序數索引 < 用戶頁個數; 序數索引++) 頁列表[序數索引] = (用戶基底 + 序數索引 * 頁大小) | 內核頁;
    同步表列();
    memset((void *)用戶基底, 0, 用戶結束 - 用戶基底);
    memset(權限列列表, 0, sizeof(權限列列表));
    ELF標頭 可執行文件標頭; memcpy(&可執行文件標頭, 資料, sizeof(可執行文件標頭));
    for (unsigned 序數索引 = 0; 序數索引 < 可執行文件標頭.程式標頭個數; 序數索引++) {
        ELF程式 資料位置; memcpy(&資料位置, 資料 + 可執行文件標頭.程式標頭偏移 + 序數索引 * sizeof(資料位置), sizeof(資料位置));
        if (資料位置.類型分類 != 1 || !資料位置.內存區大小) continue;
        if (資料位置.文件區域大小) memcpy((void *)(uintptr_t)資料位置.地址, 資料 + 資料位置.偏移值, 資料位置.文件區域大小);
        for (uintptr_t 當前位置 = 資料位置.地址 & ~(頁大小 - 1); 當前位置 < 資料位置.地址 + 資料位置.內存區大小; 當前位置 += 頁大小) {
            權限列列表[(當前位置 - 用戶基底) / 頁大小] = (資料位置.配置項位元列 & 2) ? 3 : ((資料位置.配置項位元列 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 當前位置 = 用戶棧地址; 當前位置 < 用戶結束; 當前位置 += 頁大小) 權限列列表[(當前位置 - 用戶基底) / 頁大小] = 3;
    uintptr_t 初始棧 = Linux模式 ? Linux開始棧(可執行文件標頭.條目分) : 用戶結束;
    for (unsigned 序數索引 = 0; 序數索引 < 用戶頁個數; 序數索引++) {
        unsigned 存取權限列 = 權限列列表[序數索引];
        頁列表[序數索引] = 存取權限列 ? (用戶基底 + 序數索引 * 頁大小) | (存取權限列 == 3 ? 用戶讀取寫入 : 存取權限列 == 5 ? 用戶讀取執行 : 用戶讀取僅用) : 0;
    }
    同步表列();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 序數索引 = 0; 序數索引 < 16; 序數索引++) 檔案列表[序數索引] = -1;
    memset(通訊端端點列, 0, sizeof(通訊端端點列));
    堆結束 = 用戶映像結束;
    活躍 = 1; 開始超時();
    用戶執行狀態時間[所有者物件]=板經過毫秒();
    int 結果 = 用戶進入(可執行文件標頭.條目分, 初始棧, 已轉發值);
    return 結束操作程式(結果);
}
uintptr_t 板用戶運行(uintptr_t 查找索引) {
    if (查找索引 >= sizeof(可執行文件條目列) / sizeof(可執行文件條目列[0])) return (uint32_t)-22;
    const char *名稱=查找索引==10?"javac":查找索引==11?"java":查找索引==12?"python":查找索引==13?"vi":查找索引==14?"jar":查找索引==15?"cc":查找索引==16?"jaot":"ELF";
    return (uint32_t)運行程式(可執行文件條目列[查找索引].資料, 可執行文件條目列[查找索引].大小, 可執行文件條目列[查找索引].已轉發值, 0, 名稱);
}
static uintptr_t 執行檔案(int Linux模式) {
    static unsigned char 映像[16384];
    if (活躍 || !已轉發實際參數個數) return (uint32_t)-22;
    int 檔案句柄 = pk_open((const char *)已轉發實際參數[0], 讀取僅用值, 0);
    if (檔案句柄 < 0) return (uint32_t)-錯誤編號;
    int 大小 = pk_size(檔案句柄);
    if (大小 < 0 || (unsigned)大小 > sizeof(映像)) { pk_close(檔案句柄); return (uint32_t)-27; }
    int 已接收個數 = pk_read(檔案句柄, 映像, 大小); pk_close(檔案句柄);
    if (已接收個數 != 大小) return (uint32_t)-5;
    return (uint32_t)運行程式(映像, 大小, 0, Linux模式, "");
}
uintptr_t 板用戶檔案(void) { return 執行檔案(0); }
uintptr_t 板用戶Linux檔案(void) { return 執行檔案(1); }
uintptr_t 板用戶有效性校驗(void) {
    for (unsigned 序數索引 = 0; 序數索引 < sizeof(無效可執行項列) / sizeof(無效可執行項列[0]); 序數索引++)
        if (用戶有效性校驗ELF(無效可執行項列[序數索引].資料, 無效可執行項列[序數索引].大小) != 用戶可執行文件錯誤) return 序數索引 + 1;
    return 0;
}

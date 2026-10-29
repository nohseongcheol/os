#include "../命名/計算機連接名稱列.h"
#include "屏幕信息.h"
#include <stdint.h>
#include <stddef.h>
#include "使用者.h"
#include "../通信網絡/通信網絡.h"
typedef uintptr_t 計算機機器字;
#define 計算機寄存器(首位值) (*(volatile uint32_t *)(uintptr_t)(首位值))
#define 串行設備 0xfe201000u
#define 通用型用途輸入輸出 0xfe200000u
#define 郵箱地址 0xfe00b880u
static inline void 記憶體屏障(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 時鐘個數(void) { uint64_t 臨時資料; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(臨時資料)); return 臨時資料; }
static uint64_t 頻率;
static volatile uint32_t 郵箱資料[64] __attribute__((aligned(16)));
static unsigned 屏幕就緒;
static uint32_t ARM記憶體千二進制字節單位;

void *memset(void *資料位置, int 字元程式碼, size_t 項目個數) { unsigned char *下一偏移 = 資料位置; while (項目個數--) *下一偏移++ = 字元程式碼; return 資料位置; }
void *memcpy(void *目的地址資料, const void *字符串資料, size_t 項目個數) { unsigned char *首位值 = 目的地址資料; const unsigned char *第二值 = 字符串資料; while (項目個數--) *首位值++ = *第二值++; return 目的地址資料; }

static int 郵箱(void) {
    uint32_t 申請 = (uint32_t)(uintptr_t)郵箱資料 | 8;
    uint64_t 運行 = 時鐘個數();
    記憶體屏障();
    while (計算機寄存器(郵箱地址 + 0x38) & 0x80000000u)
        if (時鐘個數() - 運行 > 頻率) return 0;
    計算機寄存器(郵箱地址 + 0x20) = 申請;
    for (;;) {
        if (!(計算機寄存器(郵箱地址 + 0x18) & 0x40000000u)) {
            uint32_t 回覆 = 計算機寄存器(郵箱地址);
            if (回覆 == 申請) { 記憶體屏障(); return 郵箱資料[1] == 0x80000000u; }
        }
        if (時鐘個數() - 運行 > 頻率) return 0;
    }
}

extern int32_t Java交互殼輸出(int32_t, int32_t), Java交互殼輸入(void);
extern void 終端位元組(unsigned);
extern int 終端待處理(void);
extern void 終端指針(unsigned,int,int),終端熱鍵(unsigned);
extern void 終端輸入模式(unsigned);
#include "../遠程值/遠程值.h"
static int 數據流集;
static unsigned UART上一個;
計算機機器字 板數據流集(計算機機器字 是否已使用) { 數據流集=是否已使用!=0; return 0; }
計算機機器字 板信道(計算機機器字 信道, 計算機機器字 字元程式碼) {
    if(數據流集 && Java交互殼輸出((int32_t)信道,(int32_t)(字元程式碼&255))) return 0;
    終端位元組(字元程式碼&255);
    遠程輸出(字元程式碼&255);
    if ((字元程式碼&255)==10 && UART上一個!=13) {
        while (計算機寄存器(串行設備 + 0x18) & 0x20) __asm__ volatile("yield");
        計算機寄存器(串行設備)=13;
    }
    UART上一個=字元程式碼&255;
    while (計算機寄存器(串行設備 + 0x18) & 0x20) __asm__ volatile("yield");
    計算機寄存器(串行設備) = (uint32_t)字元程式碼 & 255;
    return 0;
}
計算機機器字 板寫字符(計算機機器字 字元程式碼) { return 板信道(1,字元程式碼); }
計算機機器字 板原始數據取字符(void) {
    int 遠程字元=遠程輸入();if(遠程字元>=0)return 遠程字元;
    if (計算機寄存器(串行設備 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t 值 = 計算機寄存器(串行設備);
    if (值 & 0xf00) { 計算機寄存器(串行設備 + 4) = 0; return (uint32_t)-1; }
    return 值 & 255;
}
計算機機器字 板取字符(void) {
    network_poll();
    static unsigned 輸入側數據包,已使用容量; static unsigned char 數據包資料[6];
    if(終端待處理())return (uint32_t)-4096;
    if(數據流集){int32_t 字元程式碼=Java交互殼輸入();if(字元程式碼!=-3)return (uint32_t)字元程式碼;}
    for(;;){
        int 字元程式碼=(int32_t)板原始數據取字符();if(字元程式碼<0)return (uint32_t)字元程式碼;
        if(!輸入側數據包){if(字元程式碼!=30)return 字元程式碼;輸入側數據包=1;已使用容量=0;continue;}
        數據包資料[已使用容量++]=字元程式碼;if(已使用容量<6)continue;輸入側數據包=0;
        if(數據包資料[0]==1)終端指針(數據包資料[1],數據包資料[2]+數據包資料[3]*256,數據包資料[4]+數據包資料[5]*256);
        if(數據包資料[0]==2)終端熱鍵(數據包資料[1]);
        if(數據包資料[0]==3)終端輸入模式(數據包資料[1]);
        if(終端待處理())return (uint32_t)-4096;
    }
}
計算機機器字 板經過毫秒(void) { return (uint32_t)(時鐘個數() / (頻率 / 1000)); }
計算機機器字 板當前異常級別(void) { uint64_t 臨時資料; __asm__ volatile("mrs %0, CurrentEL" : "=r"(臨時資料)); return 臨時資料 >> 2; }
static void 輸出行UART(const char *字符串資料) { while (*字符串資料) 板寫字符((unsigned char)*字符串資料++); }
static void 十六進制UART(計算機機器字 項目個數) { const char *十六進制數位數 = "0123456789abcdef"; for (int 字符串資料 = 60; 字符串資料 >= 0; 字符串資料 -= 4) 板寫字符(十六進制數位數[(項目個數 >> 字符串資料) & 15]); }
計算機機器字 板停止(計算機機器字 狀態值) {
    輸出行UART("\r\nHALTED "); 十六進制UART(狀態值); 輸出行UART("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 內核致命停止(const char *原因值) __attribute__((noreturn));
void 內核致命停止(const char *原因值) { 輸出行UART("\r\nPANIC: "); 輸出行UART(原因值); 板停止(1); __builtin_unreachable(); }
void 板異常(計算機機器字 異常狀態, 計算機機器字 命令位置, 計算機機器字 無效地址) {
    輸出行UART("\r\nEXCEPTION ESR="); 十六進制UART(異常狀態);
    輸出行UART(" PC="); 十六進制UART(命令位置); 輸出行UART(" FAR="); 十六進制UART(無效地址);
    板停止(2);
}
int 板物理硬件(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    郵箱資料[0]=32;郵箱資料[1]=0;郵箱資料[2]=0x10004;郵箱資料[3]=8;郵箱資料[4]=0;
    郵箱資料[5]=郵箱資料[6]=郵箱資料[7]=0;
    return 郵箱()&&郵箱資料[4]==0x80000008u&&(郵箱資料[5]||郵箱資料[6]);
}
int 板計算機地址(unsigned char *地址) {
    郵箱資料[0]=32;郵箱資料[1]=0;郵箱資料[2]=0x10003;郵箱資料[3]=8;郵箱資料[4]=0;
    郵箱資料[5]=郵箱資料[6]=郵箱資料[7]=0;
    if(!郵箱()||(郵箱資料[4]&0x80000000u)==0||(郵箱資料[4]&0xffff)!=6)return 0;
    const unsigned char *資料=(const unsigned char*)&郵箱資料[5];unsigned 總和值=0;
    for(unsigned 序數索引=0;序數索引<6;序數索引++){地址[序數索引]=資料[序數索引];總和值|=資料[序數索引];}return 總和值&&!(地址[0]&1);
}
void 板初始化操作(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(頻率));
    計算機寄存器(串行設備 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    計算機寄存器(通用型用途輸入輸出 + 4) = (計算機寄存器(通用型用途輸入輸出 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    計算機寄存器(通用型用途輸入輸出 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. 失敗值 시 config.txt의 48MHz를 사용한다.
    郵箱資料[0] = 36; 郵箱資料[1] = 0; 郵箱資料[2] = 0x38002; 郵箱資料[3] = 12;
    郵箱資料[4] = 0; 郵箱資料[5] = 2; 郵箱資料[6] = 48000000; 郵箱資料[7] = 0; 郵箱資料[8] = 0;
    int 時鐘正常 = 郵箱();
    uint32_t 速度值 = 時鐘正常 && 郵箱資料[6] >= 1843200 ? 郵箱資料[6] : 48000000;
    郵箱資料[0]=32; 郵箱資料[1]=0; 郵箱資料[2]=0x10005; 郵箱資料[3]=8; 郵箱資料[4]=0;
    郵箱資料[5]=郵箱資料[6]=郵箱資料[7]=0;
    if (郵箱() && 郵箱資料[4]==0x80000008u) ARM記憶體千二進制字節單位=郵箱資料[6]/1024;
    uint32_t 除數64 = (uint32_t)(((uint64_t)速度值 * 4 + 57600) / 115200);
    計算機寄存器(串行設備 + 0x44) = 0x7ff;
    計算機寄存器(串行設備 + 0x24) = 除數64 / 64;
    計算機寄存器(串行設備 + 0x28) = 除數64 % 64;
    計算機寄存器(串行設備 + 0x2c) = (3u << 5) | (1u << 4);
    計算機寄存器(串行設備 + 0x38) = 0;
    計算機寄存器(串行設備 + 0x30) = 0x301;
    記憶體屏障();
    輸出行UART("JKOROS AARCH64 BARE METAL\r\n");
    用戶系統初始化操作();
    network_init();
}
計算機機器字 板FTP(計算機機器字 動作) { return (uint32_t)ftp_control((int)動作); }
計算機機器字 板網路運行狀態(計算機機器字 條目值, 計算機機器字 編號) { return 讀取網路運行狀態(條目值, 編號); }
計算機機器字 板網路設置(計算機機器字 動作, 計算機機器字 地址, 計算機機器字 掩碼值, 計算機機器字 網關值) { return (uint32_t)設定配置網路(動作, 地址, 掩碼值, 網關值); }
計算機機器字 板發送響應(計算機機器字 地址, 計算機機器字 排序值) { return (uint32_t)開始響應測試(地址, 排序值); }
計算機機器字 板讀取響應(計算機機器字 條目值) { return (uint32_t)讀取響應測試(條目值); }
計算機機器字 板電源關閉側(void) {
    ftp_control(0);
    for (unsigned 編號=0; 編號<32; 編號++) 關閉網路(編號);
    for (unsigned 編號=0; 編號<4; 編號++) 板用戶控制(32+編號);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    輸出行UART("\r\nPOWER OFF\r\n");
    while (計算機寄存器(串行設備+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    計算機寄存器(0xfe100020ul)=0x5a000000u | (計算機寄存器(0xfe100020ul)&~0xfffu) | 0x555;
    計算機寄存器(0xfe100024ul)=0x5a000000u | 10;
    計算機寄存器(0xfe10001cul)=0x5a000000u | (計算機寄存器(0xfe10001cul)&~0x30u) | 0x20;
    記憶體屏障();
    for (;;) __asm__ volatile("wfe");
}

計算機機器字 板幀緩衝(void) {
    if (屏幕就緒) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 當前項目 크기를 읽는다. */
    const uint32_t 查詢值[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 已請求寬度 = 640, 已請求高度 = 480;
    for (size_t 序數索引 = 0; 序數索引 < sizeof(查詢值)/4; 序數索引++) 郵箱資料[序數索引] = 查詢值[序數索引];
    if (郵箱() && 郵箱資料[4] == 0x80000008u &&
        郵箱資料[5] >= 640 && 郵箱資料[5] <= 1920 &&
        郵箱資料[6] >= 480 && 郵箱資料[6] <= 1080) {
        已請求寬度 = 郵箱資料[5]; 已請求高度 = 郵箱資料[6];
    }
    const uint32_t 申請[] = {
        35 * 4, 0,
        0x48003, 8, 0, 已請求寬度, 已請求高度,
        0x48004, 8, 0, 已請求寬度, 已請求高度,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 序數索引 = 0; 序數索引 < sizeof(申請)/4; 序數索引++) 郵箱資料[序數索引] = 申請[序數索引];
    // 頂端值 메시지의 實際資料 길이를 使用值: 태그 追加條目 시 長度 불일치를 방지한다.
    郵箱資料[0] = sizeof(申請);
    if (!郵箱()) return 0;
    const unsigned 響應列[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 響應長度[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 序數索引 = 0; 序數索引 < sizeof(響應列)/sizeof(響應列[0]); 序數索引++)
        if (郵箱資料[響應列[序數索引]] != (0x80000000u | 響應長度[序數索引])) return 0;
    uint32_t 背景值 = 郵箱資料[28] & 0x3fffffffu;
    uint32_t 大小 = 郵箱資料[29];
    uint32_t 已接收寬度 = 郵箱資料[5], 已接收高度 = 郵箱資料[6], 已接收行間距 = 郵箱資料[33];
    if (郵箱資料[15] != 32 || 郵箱資料[19] != 1 ||
        已接收寬度 < 640 || 已接收寬度 > 1920 || 已接收高度 < 480 || 已接收高度 > 1080 ||
        郵箱資料[10] < 已接收寬度 || 郵箱資料[11] < 已接收高度 || 郵箱資料[23] || 郵箱資料[24] ||
        !背景值 || 背景值 < 0x1000000 || (背景值 & 3) || 已接收行間距 < 已接收寬度 * 4 || (已接收行間距 & 3) ||
        (uint64_t)已接收行間距 * 已接收高度 > 大小 || (uint64_t)背景值 + 大小 > 0x40000000u)
        return 0;
    板準備繪圖((volatile uint32_t *)(uintptr_t)背景值, 已接收寬度, 已接收高度, 已接收行間距);
    屏幕就緒 = 1;
    return 1;
}

// 단일 코어의 협력식 執行緒值. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 已保存[13]; } 上下文;
static 上下文 上下文列[3];
static unsigned char 棧集[2][65536] __attribute__((aligned(16)));
static int 是否運行中[3] = {1, 0, 0};
static int 當前任務;
extern void 上下文切換(上下文 *, 上下文 *);
extern void Java任務(int32_t);
計算機機器字 板掛起(void) {
    network_poll();
    int 上一個項目 = 當前任務, 下一項目 = (上一個項目 + 1) % 3;
    while (下一項目 != 上一個項目 && !是否運行中[下一項目]) 下一項目 = (下一項目 + 1) % 3;
    if (下一項目 != 上一個項目) {
        for (unsigned 序數索引 = 0; 序數索引 < 2; 序數索引++)
            if (是否運行中[序數索引 + 1] && *(uint64_t *)棧集[序數索引] != 0x6b6f726f7373746bull)
                內核致命停止("task stack guard");
        當前任務 = 下一項目;
        上下文切換(&上下文列[上一個項目], &上下文列[下一項目]);
    }
    return 0;
}
static void 任務引導(void) {
    Java任務(當前任務);
    是否運行中[當前任務] = 0;
    板掛起();
    內核致命停止("finished task resumed");
}
計算機機器字 板任務創建(計算機機器字 標識符值) {
    if (標識符值 < 1 || 標識符值 > 2 || 是否運行中[標識符值]) return (uint32_t)-1;
    memset(&上下文列[標識符值], 0, sizeof(上下文));
    *(uint64_t *)棧集[標識符值 - 1] = 0x6b6f726f7373746bull;
    上下文列[標識符值].已保存[11] = (uintptr_t)任務引導;
    上下文列[標識符值].已保存[12] = (uintptr_t)(棧集[標識符值 - 1] + sizeof(棧集[0]));
    是否運行中[標識符值] = 1;
    return 0;
}
計算機機器字 板任務狀態(計算機機器字 標識符值) { return 標識符值 < 3 ? 是否運行中[標識符值] : (uint32_t)-1; }
extern 計算機機器字 提前編譯記憶體查找(計算機機器字);
extern uint32_t 讀取用戶狀態(unsigned, unsigned);
extern unsigned char 棧頂端[];
計算機機器字 板查詢系統(計算機機器字 條目值, 計算機機器字 編號) {
    if (條目值==0) return ARM記憶體千二進制字節單位;
    if (條目值==1) return ((uintptr_t)棧頂端-0x80000+1023)/1024;
    if (條目值==2 || 條目值==3) return 提前編譯記憶體查找(條目值==3);
    if (條目值==4) return 屏幕就緒 ? (板屏幕寬度()*板屏幕高度()*4+1023)/1024 : 0;
    if (條目值==5) return 80*1024; /* 執行命令 地址區域 16 MiB + 네 세션 保留值 地址區域. */
    if (條目值>=20) return 讀取用戶狀態(條目值-20, 編號);
    return 0;
}
int *pk_errno_location(void) { static int 錯誤列[3]; return &錯誤列[當前任務]; }

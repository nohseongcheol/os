#include "../命名/計算機連接名稱列.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "通信網絡.h"
#include "string.h"
#include "檔案ABI.h"
extern uintptr_t 板經過毫秒(void);
extern int32_t Java文件系統條目長度(int32_t), Java文件系統條目位元組(int32_t,int32_t), Java文件系統條目大小(int32_t);
extern int32_t Java文件系統條目個數(void);
static int 接收埠 = -1, 控制 = -1, 手冊連接狀態 = -1, 資料 = -1;
static unsigned 是否已記日誌輸入側, 用戶正常確認, 行大小, 行錯誤, 結束程序, 執行中任務, 已使用容量, 已發送個數, 擁有失敗;
static unsigned 回覆大小, 回覆已發送, 下一埠編號;
static uint32_t 活動;
static char 行[256], 回覆列[2048], 檔案條目名稱[64], 傳送名稱[64];
static unsigned char 傳送狀態[16384];
static int 相等(const char *首位值, const char *第二值) { while (*首位值 && *首位值 == *第二值) { 首位值++; 第二值++; } return *首位值 == *第二值; }
static void 回覆(const char *字符串資料) {
    size_t 項目個數 = strlen(字符串資料);
    if (回覆已發送) { memmove(回覆列, 回覆列 + 回覆已發送, 回覆大小 - 回覆已發送); 回覆大小 -= 回覆已發送; 回覆已發送 = 0; }
    if (項目個數 > sizeof(回覆列) - 回覆大小) { 結束程序 = 1; return; }
    memcpy(回覆列 + 回覆大小, 字符串資料, 項目個數); 回覆大小 += 項目個數;
}
static void 數值值(unsigned 值, char *結果資料, unsigned *項目個數) {
    char 數字個數[10]; unsigned 條目個數 = 0;
    do { 數字個數[條目個數++] = '0' + 值 % 10; 值 /= 10; } while (值);
    while (條目個數) 結果資料[(*項目個數)++] = 數字個數[--條目個數];
}
static void 停止傳送(void) {
    if (資料 >= 0) 關閉網路(資料); if (手冊連接狀態 >= 0) 關閉網路(手冊連接狀態);
    資料 = 手冊連接狀態 = -1; 執行中任務 = 已使用容量 = 已發送個數 = 擁有失敗 = 0;
}
static void 斷開連接(void) {
    停止傳送(); if (控制 >= 0) 關閉網路(控制); 控制 = -1;
    是否已記日誌輸入側 = 用戶正常確認 = 行大小 = 行錯誤 = 回覆大小 = 回覆已發送 = 結束程序 = 0;
}
int 檔案傳送控制(int 動作) {
    if (動作 == 2) return 接收埠 >= 0;
    if (動作 == 0) { 斷開連接(); if (接收埠 >= 0) 關閉網路(接收埠); 接收埠 = -1; return 0; }
    if (動作 != 1) return -22; if (接收埠 >= 0) return 0;
    接收埠 = 創建通訊端端點(1); if (接收埠 < 0) return 接收埠;
    int 已返回值 = 網路層綁定(接收埠, 讀取網路運行狀態(0,0), 21); if (!已返回值) 已返回值 = 網路層偵聽(接收埠);
    if (已返回值 < 0) { 關閉網路(接收埠); 接收埠 = -1; } return 已返回值;
}
static int 路徑(const char *名稱) {
    unsigned 項目個數 = 0; if (*名稱 == '/') 名稱++;
    if (!*名稱 || 相等(名稱, ".") || 相等(名稱, "..")) return 0;
    檔案條目名稱[項目個數++] = '/';
    while (*名稱) {
        unsigned char 字元程式碼 = *名稱++;
        if (項目個數 >= 63 || 字元程式碼 < 32 || 字元程式碼 == 127 || 字元程式碼 == '/' || 字元程式碼 == '\\') return 0;
        檔案條目名稱[項目個數++] = 字元程式碼;
    }
    檔案條目名稱[項目個數] = 0; return 1;
}
static void 發送列表(int 詳情) {
    已使用容量 = 已發送個數 = 0;
    for (int 序數索引 = 0; 序數索引 < Java文件系統條目個數(); 序數索引++) {
        int 項目個數 = Java文件系統條目長度(序數索引); if (項目個數 <= 0) continue;
        const char *前導部分 = 詳情 == 2 ? "type=file;size=" : 詳情 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 條目個數 = strlen(前導部分); memcpy(傳送狀態 + 已使用容量, 前導部分, 條目個數); 已使用容量 += 條目個數;
        if (詳情) 數值值(Java文件系統條目大小(序數索引), (char *)傳送狀態, &已使用容量);
        const char *後綴值 = 詳情 == 2 ? "; " : 詳情 == 1 ? " Jan 01 00:00 " : "";
        條目個數 = strlen(後綴值); memcpy(傳送狀態 + 已使用容量, 後綴值, 條目個數); 已使用容量 += 條目個數;
        for (int 內部側序數 = 0; 內部側序數 < 項目個數; 內部側序數++) 傳送狀態[已使用容量++] = Java文件系統條目位元組(序數索引,內部側序數);
        傳送狀態[已使用容量++] = '\r'; 傳送狀態[已使用容量++] = '\n';
    }
}
static void 準備手冊連接狀態(int 已擴展) {
    if (執行中任務) { 回覆("450 Transfer in progress\r\n"); return; }
    停止傳送(); 手冊連接狀態 = 創建通訊端端點(1);
    if (手冊連接狀態 >= 0) 複用通訊端地址(手冊連接狀態);
    unsigned 埠編號 = 50000 + 下一埠編號++ % 8;
    if (手冊連接狀態 < 0 || 網路層綁定(手冊連接狀態, 讀取網路運行狀態(0,0), 埠編號) || 網路層偵聽(手冊連接狀態)) {
        停止傳送(); 回覆("425 Cannot open passive listener\r\n"); return;
    }
    char 響應[96]; const char *前導部分 = 已擴展 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 項目個數 = strlen(前導部分); memcpy(響應, 前導部分, 項目個數);
    if (已擴展) { 數值值(埠編號, 響應, &項目個數); 響應[項目個數++] = '|'; }
    else {
        uint32_t 地址=讀取網路運行狀態(0,0);
        for (int 位置索引=24;位置索引>=0;位置索引-=8) { 數值值((地址>>位置索引)&255,響應,&項目個數);響應[項目個數++]=','; }
        數值值(埠編號 / 256, 響應, &項目個數); 響應[項目個數++] = ','; 數值值(埠編號 % 256, 響應, &項目個數);
    }
    響應[項目個數++] = ')'; 響應[項目個數++] = '\r'; 響應[項目個數++] = '\n'; 響應[項目個數] = 0; 回覆(響應);
}
static void 命令(void) {
    行[行大小] = 0;
    char *附加參數列 = 行; while (*附加參數列 && *附加參數列 != ' ') { if (*附加參數列 >= 'a' && *附加參數列 <= 'z') *附加參數列 -= 32; 附加參數列++; }
    if (*附加參數列) *附加參數列++ = 0; while (*附加參數列 == ' ') 附加參數列++;
    if (相等(行, "QUIT")) { 停止傳送(); 回覆("221 Goodbye\r\n"); 結束程序 = 1; return; }
    if (相等(行, "NOOP")) { 回覆("200 OK\r\n"); return; }
    if (相等(行, "SYST")) { 回覆("215 UNIX Type: L8\r\n"); return; }
    if (相等(行, "FEAT")) { 回覆("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (相等(行, "USER")) { 是否已記日誌輸入側 = 0; 用戶正常確認 = 相等(附加參數列, "anonymous") || 相等(附加參數列, "jkoros"); 回覆(用戶正常確認 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (相等(行, "PASS")) { 是否已記日誌輸入側 = 用戶正常確認; 回覆(是否已記日誌輸入側 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!是否已記日誌輸入側) { 回覆("530 Login first\r\n"); return; }
    if (相等(行, "PWD")) 回覆("257 \"/\"\r\n");
    else if (相等(行, "CWD")) 回覆(相等(附加參數列, "/") || 相等(附加參數列, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (相等(行, "TYPE")) 回覆(相等(附加參數列, "I") || 相等(附加參數列, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (相等(行, "OPTS")) 回覆(相等(附加參數列, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (相等(行, "PASV")) 準備手冊連接狀態(0);
    else if (相等(行, "EPSV")) { if (*附加參數列 && !相等(附加參數列, "1")) 回覆("522 IPv4 only\r\n"); else 準備手冊連接狀態(1); }
    else if (相等(行, "ABOR")) { 停止傳送(); 回覆("226 Transfer aborted\r\n"); }
    else if (相等(行, "DELE")) { 回覆(路徑(附加參數列) && pk_unlink(檔案條目名稱) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (相等(行, "LIST") || 相等(行, "NLST") || 相等(行, "MLSD")) {
        if (執行中任務) { 回覆("450 Transfer in progress\r\n"); return; }
        if (手冊連接狀態 < 0 && 資料 < 0) { 回覆("425 Use PASV or EPSV\r\n"); return; }
        if (*附加參數列 && !相等(附加參數列,"/") && !相等(附加參數列,".") && !相等(附加參數列,"-a") && !相等(附加參數列,"-l") && !相等(附加參數列,"-la")) { 回覆("550 Root listing only\r\n"); return; }
        發送列表(相等(行,"MLSD") ? 2 : 相等(行,"LIST") ? 1 : 0); 執行中任務 = 2;
        回覆("150 Opening directory listing\r\n");
    }
    else if (相等(行, "SIZE")) {
        if (!路徑(附加參數列)) { 回覆("550 Invalid filename\r\n"); return; }
        int 檔案句柄 = pk_open(檔案條目名稱, 讀取僅用值, 0); if (檔案句柄 < 0) { 回覆("550 File unavailable\r\n"); return; }
        int 大小 = pk_size(檔案句柄); pk_close(檔案句柄); char 響應[32] = "213 "; unsigned 項目個數 = 4;
        數值值(大小, 響應, &項目個數); 響應[項目個數++] = '\r'; 響應[項目個數++] = '\n'; 響應[項目個數] = 0; 回覆(響應);
    } else if (相等(行, "STOR") || 相等(行, "RETR")) {
        if (執行中任務) { 回覆("450 Transfer in progress\r\n"); return; }
        if (手冊連接狀態 < 0 && 資料 < 0) { 回覆("425 Use PASV or EPSV\r\n"); return; }
        if (!路徑(附加參數列)) { 回覆("550 Invalid filename\r\n"); return; }
        執行中任務 = 相等(行, "STOR") ? 1 : 2; 已使用容量 = 已發送個數 = 擁有失敗 = 0;
        memcpy(傳送名稱, 檔案條目名稱, strlen(檔案條目名稱) + 1);
        if (執行中任務 == 2) {
            int 檔案句柄 = pk_open(檔案條目名稱, 讀取僅用值, 0);
            if (檔案句柄 < 0) { 執行中任務 = 0; 回覆("550 File unavailable\r\n"); return; }
            int 項目個數 = pk_read(檔案句柄, 傳送狀態, sizeof(傳送狀態)); pk_close(檔案句柄);
            if (項目個數 < 0) { 執行中任務 = 0; 回覆("451 Read failed\r\n"); return; } 已使用容量 = 項目個數;
        }
        回覆("150 Opening binary data connection\r\n");
    } else 回覆("502 Command not implemented\r\n");
}
void 審查檔案傳送(void) {
    if (接收埠 < 0) return;
    int 傳入連接狀態 = 網路層接受(接收埠);
    if (傳入連接狀態 >= 0) {
        if (控制 >= 0) { 網路層寫入(傳入連接狀態, "421 One session at a time\r\n", 27); 關閉網路(傳入連接狀態); }
        else { 控制 = 傳入連接狀態; 活動 = 板經過毫秒(); 回覆("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (控制 < 0) return;
    if ((uint32_t)(板經過毫秒() - 活動) > 60000) { 斷開連接(); return; }
    if (!結束程序) for (unsigned 預算 = 0; 預算 < 256; 預算++) {
        unsigned char 字元程式碼; int 已返回值 = 網路層讀取(控制, &字元程式碼, 1);
        if (已返回值 == -11) break; if (已返回值 <= 0) { 斷開連接(); return; } 活動 = 板經過毫秒();
        if (字元程式碼 == '\n') { if (行錯誤) 回覆("500 Command too long or invalid\r\n"); else 命令(); 行大小 = 行錯誤 = 0; if (結束程序) break; }
        else if (字元程式碼 != '\r') { if (!字元程式碼 || 行大小 >= sizeof(行) - 1) 行錯誤 = 1; else 行[行大小++] = 字元程式碼; }
    }
    if (手冊連接狀態 >= 0 && 資料 < 0) {
        int 已返回值 = 網路層接受(手冊連接狀態);
        if (已返回值 >= 0) {
            if (網路層對端地址(已返回值) != 網路層對端地址(控制)) 關閉網路(已返回值);
            else { 資料 = 已返回值; 關閉網路(手冊連接狀態); 手冊連接狀態 = -1; 活動 = 板經過毫秒(); }
        }
    }
    if (執行中任務 == 1 && 資料 >= 0) for (unsigned 預算 = 0; 預算 < 8; 預算++) {
        unsigned char 資料塊[512]; int 項目個數 = 網路層讀取(資料, 資料塊, sizeof(資料塊));
        if (項目個數 == -11) break;
        if (項目個數 < 0) { 停止傳送(); 回覆("426 Data connection failed\r\n"); break; }
        活動 = 板經過毫秒();
        if (項目個數 == 0) {
            int 結果 = -1;
            if (!擁有失敗) {
                int 檔案句柄 = pk_open(傳送名稱, 寫入僅用值 | 創建條件缺失 | 截斷內容, 0600);
                if (檔案句柄 >= 0) { 結果 = pk_write(檔案句柄, 傳送狀態, 已使用容量); pk_close(檔案句柄); }
            }
            int 是否已成功 = !擁有失敗 && 結果 == (int)已使用容量; 停止傳送(); 回覆(是否已成功 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)項目個數 > sizeof(傳送狀態) - 已使用容量) 擁有失敗 = 1;
        if (!擁有失敗) { memcpy(傳送狀態 + 已使用容量, 資料塊, 項目個數); 已使用容量 += 項目個數; }
    }
    if (執行中任務 == 2 && 資料 >= 0) {
        int 項目個數 = 網路層寫入(資料, 傳送狀態 + 已發送個數, 已使用容量 - 已發送個數);
        if (項目個數 >= 0) { 已發送個數 += 項目個數; 活動 = 板經過毫秒(); if (已發送個數 == 已使用容量) { 停止傳送(); 回覆("226 Transfer complete\r\n"); } }
        else if (項目個數 != -11) { 停止傳送(); 回覆("426 Data connection failed\r\n"); }
    }
    if (回覆已發送 < 回覆大小) {
        int 項目個數 = 網路層寫入(控制, 回覆列 + 回覆已發送, 回覆大小 - 回覆已發送);
        if (項目個數 > 0) 回覆已發送 += 項目個數; else if (項目個數 != -11) { 斷開連接(); return; }
    }
    if (回覆已發送 == 回覆大小) { 回覆大小 = 回覆已發送 = 0; if (結束程序) 斷開連接(); }
}

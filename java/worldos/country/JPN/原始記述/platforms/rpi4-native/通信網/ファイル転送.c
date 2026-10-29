#include "../命名/機械連結名前一覧.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "通信網.h"
#include "string.h"
#include "ファイルABI.h"
extern uintptr_t 基板経過ミリ秒(void);
extern int32_t Javaファイル体系入口長さ(int32_t), Javaファイル体系入口バイト(int32_t,int32_t), Javaファイル体系入口容量(int32_t);
extern int32_t Javaファイル体系入口個数(void);
static int ポート受取 = -1, 制御 = -1, 手順書接続状態 = -1, データ = -1;
static unsigned 判定記録状態入力側, 利用者正常状態, 行容量, 行不正, 脱出プログラム, 実行中作業, 使用済み容積, 送信済み個数, 保有失敗済み;
static unsigned 返答容量, 返答送信済み, 次回ポート番号;
static uint32_t 活動;
static char 行[256], 応答一覧[2048], ファイル入口名前[64], 転送名前[64];
static unsigned char 転送状況[16384];
static int 等価(const char *先頭位置値, const char *第二値) { while (*先頭位置値 && *先頭位置値 == *第二値) { 先頭位置値++; 第二値++; } return *先頭位置値 == *第二値; }
static void 返答(const char *文字列データ) {
    size_t 項目個数 = strlen(文字列データ);
    if (返答送信済み) { memmove(応答一覧, 応答一覧 + 返答送信済み, 返答容量 - 返答送信済み); 返答容量 -= 返答送信済み; 返答送信済み = 0; }
    if (項目個数 > sizeof(応答一覧) - 返答容量) { 脱出プログラム = 1; return; }
    memcpy(応答一覧 + 返答容量, 文字列データ, 項目個数); 返答容量 += 項目個数;
}
static void 数値値(unsigned 値, char *結果データ, unsigned *項目個数) {
    char 桁個数[10]; unsigned 入口個数 = 0;
    do { 桁個数[入口個数++] = '0' + 値 % 10; 値 /= 10; } while (値);
    while (入口個数) 結果データ[(*項目個数)++] = 桁個数[--入口個数];
}
static void 転送停止(void) {
    if (データ >= 0) 通信網閉鎖(データ); if (手順書接続状態 >= 0) 通信網閉鎖(手順書接続状態);
    データ = 手順書接続状態 = -1; 実行中作業 = 使用済み容積 = 送信済み個数 = 保有失敗済み = 0;
}
static void 切断(void) {
    転送停止(); if (制御 >= 0) 通信網閉鎖(制御); 制御 = -1;
    判定記録状態入力側 = 利用者正常状態 = 行容量 = 行不正 = 返答容量 = 返答送信済み = 脱出プログラム = 0;
}
int ファイル転送制御(int 動作) {
    if (動作 == 2) return ポート受取 >= 0;
    if (動作 == 0) { 切断(); if (ポート受取 >= 0) 通信網閉鎖(ポート受取); ポート受取 = -1; return 0; }
    if (動作 != 1) return -22; if (ポート受取 >= 0) return 0;
    ポート受取 = ソケット通信端点作成(1); if (ポート受取 < 0) return ポート受取;
    int 返却済み値 = 網結合(ポート受取, 通信網状態読取(0,0), 21); if (!返却済み値) 返却済み値 = 網接続待機(ポート受取);
    if (返却済み値 < 0) { 通信網閉鎖(ポート受取); ポート受取 = -1; } return 返却済み値;
}
static int 経路(const char *名前) {
    unsigned 項目個数 = 0; if (*名前 == '/') 名前++;
    if (!*名前 || 等価(名前, ".") || 等価(名前, "..")) return 0;
    ファイル入口名前[項目個数++] = '/';
    while (*名前) {
        unsigned char 文字コード = *名前++;
        if (項目個数 >= 63 || 文字コード < 32 || 文字コード == 127 || 文字コード == '/' || 文字コード == '\\') return 0;
        ファイル入口名前[項目個数++] = 文字コード;
    }
    ファイル入口名前[項目個数] = 0; return 1;
}
static void 一覧送信(int 詳細) {
    使用済み容積 = 送信済み個数 = 0;
    for (int 序数添字 = 0; 序数添字 < Javaファイル体系入口個数(); 序数添字++) {
        int 項目個数 = Javaファイル体系入口長さ(序数添字); if (項目個数 <= 0) continue;
        const char *先行部分 = 詳細 == 2 ? "type=file;size=" : 詳細 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned 入口個数 = strlen(先行部分); memcpy(転送状況 + 使用済み容積, 先行部分, 入口個数); 使用済み容積 += 入口個数;
        if (詳細) 数値値(Javaファイル体系入口容量(序数添字), (char *)転送状況, &使用済み容積);
        const char *接尾辞値 = 詳細 == 2 ? "; " : 詳細 == 1 ? " Jan 01 00:00 " : "";
        入口個数 = strlen(接尾辞値); memcpy(転送状況 + 使用済み容積, 接尾辞値, 入口個数); 使用済み容積 += 入口個数;
        for (int 内側序数 = 0; 内側序数 < 項目個数; 内側序数++) 転送状況[使用済み容積++] = Javaファイル体系入口バイト(序数添字,内側序数);
        転送状況[使用済み容積++] = '\r'; 転送状況[使用済み容積++] = '\n';
    }
}
static void 手順書接続状態用意(int 拡張済み) {
    if (実行中作業) { 返答("450 Transfer in progress\r\n"); return; }
    転送停止(); 手順書接続状態 = ソケット通信端点作成(1);
    if (手順書接続状態 >= 0) 再利用ソケット番地(手順書接続状態);
    unsigned ポート番号 = 50000 + 次回ポート番号++ % 8;
    if (手順書接続状態 < 0 || 網結合(手順書接続状態, 通信網状態読取(0,0), ポート番号) || 網接続待機(手順書接続状態)) {
        転送停止(); 返答("425 Cannot open passive listener\r\n"); return;
    }
    char 応答[96]; const char *先行部分 = 拡張済み ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned 項目個数 = strlen(先行部分); memcpy(応答, 先行部分, 項目個数);
    if (拡張済み) { 数値値(ポート番号, 応答, &項目個数); 応答[項目個数++] = '|'; }
    else {
        uint32_t 番地=通信網状態読取(0,0);
        for (int 位置添字=24;位置添字>=0;位置添字-=8) { 数値値((番地>>位置添字)&255,応答,&項目個数);応答[項目個数++]=','; }
        数値値(ポート番号 / 256, 応答, &項目個数); 応答[項目個数++] = ','; 数値値(ポート番号 % 256, 応答, &項目個数);
    }
    応答[項目個数++] = ')'; 応答[項目個数++] = '\r'; 応答[項目個数++] = '\n'; 応答[項目個数] = 0; 返答(応答);
}
static void 命令(void) {
    行[行容量] = 0;
    char *追加分引数列 = 行; while (*追加分引数列 && *追加分引数列 != ' ') { if (*追加分引数列 >= 'a' && *追加分引数列 <= 'z') *追加分引数列 -= 32; 追加分引数列++; }
    if (*追加分引数列) *追加分引数列++ = 0; while (*追加分引数列 == ' ') 追加分引数列++;
    if (等価(行, "QUIT")) { 転送停止(); 返答("221 Goodbye\r\n"); 脱出プログラム = 1; return; }
    if (等価(行, "NOOP")) { 返答("200 OK\r\n"); return; }
    if (等価(行, "SYST")) { 返答("215 UNIX Type: L8\r\n"); return; }
    if (等価(行, "FEAT")) { 返答("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (等価(行, "USER")) { 判定記録状態入力側 = 0; 利用者正常状態 = 等価(追加分引数列, "anonymous") || 等価(追加分引数列, "jkoros"); 返答(利用者正常状態 ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (等価(行, "PASS")) { 判定記録状態入力側 = 利用者正常状態; 返答(判定記録状態入力側 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!判定記録状態入力側) { 返答("530 Login first\r\n"); return; }
    if (等価(行, "PWD")) 返答("257 \"/\"\r\n");
    else if (等価(行, "CWD")) 返答(等価(追加分引数列, "/") || 等価(追加分引数列, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (等価(行, "TYPE")) 返答(等価(追加分引数列, "I") || 等価(追加分引数列, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (等価(行, "OPTS")) 返答(等価(追加分引数列, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (等価(行, "PASV")) 手順書接続状態用意(0);
    else if (等価(行, "EPSV")) { if (*追加分引数列 && !等価(追加分引数列, "1")) 返答("522 IPv4 only\r\n"); else 手順書接続状態用意(1); }
    else if (等価(行, "ABOR")) { 転送停止(); 返答("226 Transfer aborted\r\n"); }
    else if (等価(行, "DELE")) { 返答(経路(追加分引数列) && pk_unlink(ファイル入口名前) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (等価(行, "LIST") || 等価(行, "NLST") || 等価(行, "MLSD")) {
        if (実行中作業) { 返答("450 Transfer in progress\r\n"); return; }
        if (手順書接続状態 < 0 && データ < 0) { 返答("425 Use PASV or EPSV\r\n"); return; }
        if (*追加分引数列 && !等価(追加分引数列,"/") && !等価(追加分引数列,".") && !等価(追加分引数列,"-a") && !等価(追加分引数列,"-l") && !等価(追加分引数列,"-la")) { 返答("550 Root listing only\r\n"); return; }
        一覧送信(等価(行,"MLSD") ? 2 : 等価(行,"LIST") ? 1 : 0); 実行中作業 = 2;
        返答("150 Opening directory listing\r\n");
    }
    else if (等価(行, "SIZE")) {
        if (!経路(追加分引数列)) { 返答("550 Invalid filename\r\n"); return; }
        int ファイル取扱い = pk_open(ファイル入口名前, 専用値読取, 0); if (ファイル取扱い < 0) { 返答("550 File unavailable\r\n"); return; }
        int 容量 = pk_size(ファイル取扱い); pk_close(ファイル取扱い); char 応答[32] = "213 "; unsigned 項目個数 = 4;
        数値値(容量, 応答, &項目個数); 応答[項目個数++] = '\r'; 応答[項目個数++] = '\n'; 応答[項目個数] = 0; 返答(応答);
    } else if (等価(行, "STOR") || 等価(行, "RETR")) {
        if (実行中作業) { 返答("450 Transfer in progress\r\n"); return; }
        if (手順書接続状態 < 0 && データ < 0) { 返答("425 Use PASV or EPSV\r\n"); return; }
        if (!経路(追加分引数列)) { 返答("550 Invalid filename\r\n"); return; }
        実行中作業 = 等価(行, "STOR") ? 1 : 2; 使用済み容積 = 送信済み個数 = 保有失敗済み = 0;
        memcpy(転送名前, ファイル入口名前, strlen(ファイル入口名前) + 1);
        if (実行中作業 == 2) {
            int ファイル取扱い = pk_open(ファイル入口名前, 専用値読取, 0);
            if (ファイル取扱い < 0) { 実行中作業 = 0; 返答("550 File unavailable\r\n"); return; }
            int 項目個数 = pk_read(ファイル取扱い, 転送状況, sizeof(転送状況)); pk_close(ファイル取扱い);
            if (項目個数 < 0) { 実行中作業 = 0; 返答("451 Read failed\r\n"); return; } 使用済み容積 = 項目個数;
        }
        返答("150 Opening binary data connection\r\n");
    } else 返答("502 Command not implemented\r\n");
}
void ファイル転送調査(void) {
    if (ポート受取 < 0) return;
    int 到来接続状態 = 網受理(ポート受取);
    if (到来接続状態 >= 0) {
        if (制御 >= 0) { 網書込(到来接続状態, "421 One session at a time\r\n", 27); 通信網閉鎖(到来接続状態); }
        else { 制御 = 到来接続状態; 活動 = 基板経過ミリ秒(); 返答("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (制御 < 0) return;
    if ((uint32_t)(基板経過ミリ秒() - 活動) > 60000) { 切断(); return; }
    if (!脱出プログラム) for (unsigned 予算 = 0; 予算 < 256; 予算++) {
        unsigned char 文字コード; int 返却済み値 = 網読取(制御, &文字コード, 1);
        if (返却済み値 == -11) break; if (返却済み値 <= 0) { 切断(); return; } 活動 = 基板経過ミリ秒();
        if (文字コード == '\n') { if (行不正) 返答("500 Command too long or invalid\r\n"); else 命令(); 行容量 = 行不正 = 0; if (脱出プログラム) break; }
        else if (文字コード != '\r') { if (!文字コード || 行容量 >= sizeof(行) - 1) 行不正 = 1; else 行[行容量++] = 文字コード; }
    }
    if (手順書接続状態 >= 0 && データ < 0) {
        int 返却済み値 = 網受理(手順書接続状態);
        if (返却済み値 >= 0) {
            if (網通信相手番地(返却済み値) != 網通信相手番地(制御)) 通信網閉鎖(返却済み値);
            else { データ = 返却済み値; 通信網閉鎖(手順書接続状態); 手順書接続状態 = -1; 活動 = 基板経過ミリ秒(); }
        }
    }
    if (実行中作業 == 1 && データ >= 0) for (unsigned 予算 = 0; 予算 < 8; 予算++) {
        unsigned char データブロック[512]; int 項目個数 = 網読取(データ, データブロック, sizeof(データブロック));
        if (項目個数 == -11) break;
        if (項目個数 < 0) { 転送停止(); 返答("426 Data connection failed\r\n"); break; }
        活動 = 基板経過ミリ秒();
        if (項目個数 == 0) {
            int 結果 = -1;
            if (!保有失敗済み) {
                int ファイル取扱い = pk_open(転送名前, 専用値書込 | 作成条件未存在 | 切詰め内容, 0600);
                if (ファイル取扱い >= 0) { 結果 = pk_write(ファイル取扱い, 転送状況, 使用済み容積); pk_close(ファイル取扱い); }
            }
            int 判定成功済み = !保有失敗済み && 結果 == (int)使用済み容積; 転送停止(); 返答(判定成功済み ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)項目個数 > sizeof(転送状況) - 使用済み容積) 保有失敗済み = 1;
        if (!保有失敗済み) { memcpy(転送状況 + 使用済み容積, データブロック, 項目個数); 使用済み容積 += 項目個数; }
    }
    if (実行中作業 == 2 && データ >= 0) {
        int 項目個数 = 網書込(データ, 転送状況 + 送信済み個数, 使用済み容積 - 送信済み個数);
        if (項目個数 >= 0) { 送信済み個数 += 項目個数; 活動 = 基板経過ミリ秒(); if (送信済み個数 == 使用済み容積) { 転送停止(); 返答("226 Transfer complete\r\n"); } }
        else if (項目個数 != -11) { 転送停止(); 返答("426 Data connection failed\r\n"); }
    }
    if (返答送信済み < 返答容量) {
        int 項目個数 = 網書込(制御, 応答一覧 + 返答送信済み, 返答容量 - 返答送信済み);
        if (項目個数 > 0) 返答送信済み += 項目個数; else if (項目個数 != -11) { 切断(); return; }
    }
    if (返答送信済み == 返答容量) { 返答容量 = 返答送信済み = 0; if (脱出プログラム) 切断(); }
}

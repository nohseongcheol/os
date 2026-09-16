#include <通訊位址/位元組順序.h>
#include <錯誤編號.h>
#include <檔案控制.h>
#include <互聯網路/位址.h>
#include <基本定義.h>
#include <系統/通訊端點.h>
#include <系統/檔案狀態.h>
#include <系統/系統身分.h>
#include <系統/子行程等待.h>
#include <輸入輸出與執行.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { 輸入列容量 = 512, 最大引數個數 = 16, 最大命令檔案巢狀層數 = 4 };
static int 命令檔案巢狀深度;
struct 輸入串流 {
    int 輸入描述元;
    char 傳輸緩衝區[256];
    大小型別 位置;
    大小型別 長度;
};

static 大小型別 文字位元組長度(const char *文字)
{
    大小型別 長度 = 0;
    while (文字[長度] != '\0')
        長度++;
    return 長度;
}

static int 文字相同(const char *左側, const char *右側)
{
    大小型別 位置 = 0;
    while (左側[位置] == 右側[位置]) {
        if (左側[位置] == '\0')
            return 1;
        位置++;
    }
    return 0;
}

static void 寫出文字(const char *文字)
{
    大小型別 長度 = 文字位元組長度(文字);
    while (長度 > 0U) {
        有號大小型別 已寫位元組數 = 寫入(標準輸出編號, 文字, 長度);
        if (已寫位元組數 <= 0)
            return;
        文字 += 已寫位元組數;
        長度 -= (大小型別)已寫位元組數;
    }
}

static void 寫出整數(int 數值)
{
    char 數字字元[16];
    unsigned int 數位個數;
    unsigned int 無號數值;

    if (數值 < 0) {
        寫出文字("-");
        無號數值 = (unsigned int)(-(數值 + 1)) + 1U;
    } else {
        無號數值 = (unsigned int)數值;
    }
    數位個數 = 0;
    do {
        數字字元[數位個數++] = (char)('0' + 無號數值 % 10U);
        無號數值 /= 10U;
    } while (無號數值 != 0U);
    while (數位個數 > 0U) {
        數位個數--;
        (void)寫入(標準輸出編號, &數字字元[數位個數], 1);
    }
}

static void 回報錯誤(const char *操作)
{
    寫出文字("error: ");
    寫出文字(操作);
    寫出文字(" errno=");
    寫出整數(錯誤編號);
    寫出文字("\n");
}

static int 讀取輸入列(struct 輸入串流 *輸入, char *輸入列, 大小型別 容量)
{
    大小型別 位置 = 0;
    int 無效輸入列 = 0;
    char 字元;
    有號大小型別 已讀位元組數;
    if (容量 < 2U)
        return -2;
    for (;;) {
        if (輸入->位置 == 輸入->長度) {
            已讀位元組數 = 讀取(輸入->輸入描述元, 輸入->傳輸緩衝區, sizeof(輸入->傳輸緩衝區));
            if (已讀位元組數 < 0) {
                if (錯誤編號 == 錯誤操作被中斷)
                    continue;
                return -1;
            }
            if (已讀位元組數 == 0) {
                if (位置 == 0 && !無效輸入列)
                    return -1;
                break;
            }
            輸入->長度 = (大小型別)已讀位元組數;
            輸入->位置 = 0;
        }
        字元 = 輸入->傳輸緩衝區[輸入->位置++];
        if (字元 == '\n')
            break;
        if (輸入->輸入描述元 == 標準輸入編號 && 字元 == 4) {
            if (位置 == 0 && !無效輸入列)
                return -1;
            break;
        }
        if (輸入->輸入描述元 == 標準輸入編號 && (字元 == 8 || 字元 == 127)) {
            if (位置 > 0) {
                do {
                    位置--;
                } while (位置 > 0 && ((unsigned char)輸入列[位置] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (字元 == '\r')
            continue;
        if (字元 == '\0') {
            無效輸入列 = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (位置 + 1U < 容量)
            輸入列[位置++] = 字元;
        else
            無效輸入列 = 1;
    }
    輸入列[位置] = '\0';
    return 無效輸入列 ? -2 : (int)位置;
}

static int 拆分引數(char *輸入列, char **引數列表)
{
    int 引數個數 = 0;
    char *目前位置 = 輸入列;
    char *輸出位置 = 輸入列;

    while (*目前位置 != '\0') {
        char 引號 = '\0';
        while (*目前位置 == ' ' || *目前位置 == '\t')
            目前位置++;
        if (*目前位置 == '\0' || *目前位置 == '#')
            break;
        if (引數個數 == 最大引數個數 - 1)
            return -1;
        引數列表[引數個數++] = 輸出位置;
        while (*目前位置 != '\0') {
            char 字元 = *目前位置++;
            if (引號 == '\0' && (字元 == ' ' || 字元 == '\t'))
                break;
            if (字元 == '\\' && 引號 != '\'') {
                if (*目前位置 == '\0')
                    return -1;
                *輸出位置++ = *目前位置++;
            } else if (字元 == '\'' || 字元 == '"') {
                if (引號 == '\0')
                    引號 = 字元;
                else if (引號 == 字元)
                    引號 = '\0';
                else
                    *輸出位置++ = 字元;
            } else {
                *輸出位置++ = 字元;
            }
        }
        if (引號 != '\0')
            return -1;
        *輸出位置++ = '\0';
    }
    引數列表[引數個數] = (char *)0;
    return 引數個數;
}

static void 顯示說明(void)
{
    大小型別 位置;
    寫出文字(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    寫出文字("Native command proposals (ASCII aliases remain available):\n");
    for (位置 = 0; 位置 < sizeof(基準命令) / sizeof(基準命令[0]); 位置++) {
        寫出文字(本地語言命令別名[位置]);
        寫出文字(" = ");
        寫出文字(基準命令[位置]);
        寫出文字("\n");
    }
}

static int 命令相符(const char *文字, const char *命令)
{
    大小型別 位置;
    if (文字相同(文字, 命令))
        return 1;
    for (位置 = 0; 位置 < sizeof(基準命令) / sizeof(基準命令[0]); 位置++)
        if (文字相同(命令, 基準命令[位置]))
            return 文字相同(文字, 本地語言命令別名[位置]);
    return 0;
}

static int 解譯輸入(int 輸入描述元);

static int 解譯命令檔案(const char *檔名)
{
    int 檔案描述元;
    int 狀態;
    if (命令檔案巢狀深度 >= 最大命令檔案巢狀層數) {
        寫出文字("source: nesting limit\n");
        return 0;
    }
    檔案描述元 = 開啟(檔名, 唯讀開啟);
    if (檔案描述元 < 0) {
        回報錯誤(檔名);
        return 0;
    }
    命令檔案巢狀深度++;
    狀態 = 解譯輸入(檔案描述元);
    命令檔案巢狀深度--;
    (void)關閉(檔案描述元);
    return 狀態;
}

static void 顯示引數(int 引數個數, char **引數列表)
{
    int 位置;
    for (位置 = 1; 位置 < 引數個數; 位置++) {
        if (位置 != 1)
            寫出文字(" ");
        寫出文字(引數列表[位置]);
    }
    寫出文字("\n");
}

static void 顯示目前目錄(void)
{
    char 路徑[128];
    if (取得工作目錄路徑(路徑, sizeof(路徑)) == (char *)0) {
        回報錯誤("pwd");
        return;
    }
    寫出文字(路徑);
    寫出文字("\n");
}

static void 顯示檔案內容(const char *檔名)
{
    char 傳輸緩衝區[128];
    int 檔案描述元 = 開啟(檔名, 唯讀開啟);
    有號大小型別 已讀位元組數;

    if (檔案描述元 < 0) {
        回報錯誤("cat");
        return;
    }
    while ((已讀位元組數 = 讀取(檔案描述元, 傳輸緩衝區, sizeof(傳輸緩衝區))) > 0)
        (void)寫入(標準輸出編號, 傳輸緩衝區, (大小型別)已讀位元組數);
    if (已讀位元組數 < 0)
        回報錯誤("cat/read");
    (void)關閉(檔案描述元);
    寫出文字("\n");
}

static void 顯示檔案資訊(const char *檔名)
{
    struct 檔案狀態 狀態;
    if (檔案狀態(檔名, &狀態) < 0) {
        回報錯誤("stat");
        return;
    }
    寫出文字("size=");
    寫出整數((int)狀態.檔案大小);
    寫出文字(檢查目錄模式(狀態.檔案類型與權限) ? " type=directory\n" : " type=file\n");
}

static void 顯示行程編號(void)
{
    寫出文字("pid=");
    寫出整數((int)取得行程編號());
    寫出文字(" ppid=");
    寫出整數((int)取得父行程編號());
    寫出文字("\n");
}

static void 顯示系統資訊(void)
{
    struct 系統身分資訊 系統識別資訊;
    if (取得系統資訊(&系統識別資訊) < 0) {
        回報錯誤("uname");
        return;
    }
    寫出文字(系統識別資訊.系統名稱);
    寫出文字(" ");
    寫出文字(系統識別資訊.系統發行版);
    寫出文字(" ");
    寫出文字(系統識別資訊.機器類型);
    寫出文字("\n");
}

static void 執行程式(int 引數個數, char **引數列表)
{
    行程編號型別 子行程編號;
    int 子行程終止狀態 = 0;

    if (引數個數 < 2) {
        寫出文字("usage: run FILE [ARGS...]\n");
        return;
    }
    子行程編號 = 分出子行程();
    if (子行程編號 < 0) {
        回報錯誤("fork");
        return;
    }
    if (子行程編號 == 0) {
        替換執行內容(引數列表[1], &引數列表[1], (char *const *)0);
        回報錯誤("execve");
        立即結束(127);
    }
    if (等待指定子行程(子行程編號, &子行程終止狀態, 0) < 0) {
        回報錯誤("waitpid");
        return;
    }
    寫出文字("exit-status=");
    寫出整數(提取結束值(子行程終止狀態));
    寫出文字("\n");
}

static void 測試資料報回送(const char *訊息)
{
    struct 互聯網路端點位址 接收端點位址 = {0};
    struct 互聯網路端點位址 傳送端點位址 = {0};
    位址長度型別 傳送位址長度 = sizeof(傳送端點位址);
    char 收到的資料[96];
    大小型別 訊息位元組長度 = 文字位元組長度(訊息);
    int 接收通訊端 = -1;
    int 傳送通訊端 = -1;
    有號大小型別 接收位元組數;

    if (訊息位元組長度 >= sizeof(收到的資料)) {
        寫出文字("udp: message exceeds 95 bytes\n");
        return;
    }
    接收通訊端 = 建立通訊端點(互聯網路位址族, 資料報端點, 使用者資料報協定);
    傳送通訊端 = 建立通訊端點(互聯網路位址族, 資料報端點, 使用者資料報協定);
    if (接收通訊端 < 0 || 傳送通訊端 < 0) {
        回報錯誤("socket");
        goto 關閉通訊端;
    }
    接收端點位址.互聯位址族 = 互聯網路位址族;
    接收端點位址.通訊埠編號 = 轉為網路次序16位(40404);
    接收端點位址.互聯位址內容.位址值 = 轉為網路次序32位(本機迴送位址);
    if (繫結本地位址(接收通訊端, (const struct 通訊端點位址 *)&接收端點位址, sizeof(接收端點位址)) < 0) {
        回報錯誤("bind");
        goto 關閉通訊端;
    }
    if (連接對端(傳送通訊端, (const struct 通訊端點位址 *)&接收端點位址, sizeof(接收端點位址)) < 0) {
        回報錯誤("connect");
        goto 關閉通訊端;
    }
    if (傳送(傳送通訊端, 訊息, 訊息位元組長度, 0) != (有號大小型別)訊息位元組長度) {
        回報錯誤("send");
        goto 關閉通訊端;
    }
    接收位元組數 = 接收並取得來源位址(接收通訊端, 收到的資料, sizeof(收到的資料) - 1U, 0,
                         (struct 通訊端點位址 *)&傳送端點位址, &傳送位址長度);
    if (接收位元組數 < 0) {
        回報錯誤("recvfrom");
        goto 關閉通訊端;
    }
    收到的資料[接收位元組數] = '\0';
    寫出文字("udp-received: ");
    寫出文字(收到的資料);
    寫出文字("\n");

關閉通訊端:
    if (傳送通訊端 >= 0)
        (void)關閉(傳送通訊端);
    if (接收通訊端 >= 0)
        (void)關閉(接收通訊端);
}

static int 解譯輸入(int 輸入描述元)
{
    char 輸入列[輸入列容量];
    char *引數列表[最大引數個數];
    struct 輸入串流 輸入 = {0};
    輸入.輸入描述元 = 輸入描述元;

    for (;;) {
        int 引數個數;
        int 狀態;
        if (輸入描述元 == 標準輸入編號)
            寫出文字("worldos$ ");
        狀態 = 讀取輸入列(&輸入, 輸入列, sizeof(輸入列));
        if (狀態 == -1)
            return 0;
        if (狀態 == -2) {
            寫出文字("input rejected: overlong or binary line\n");
            continue;
        }
        引數個數 = 拆分引數(輸入列, 引數列表);
        if (引數個數 < 0) {
            寫出文字("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (引數個數 == 0)
            continue;
        if (命令相符(引數列表[0], "help"))
            顯示說明();
        else if (命令相符(引數列表[0], "echo"))
            顯示引數(引數個數, 引數列表);
        else if (命令相符(引數列表[0], "pwd"))
            顯示目前目錄();
        else if (命令相符(引數列表[0], "cd")) {
            if (引數個數 < 2)
                寫出文字("usage: cd PATH\n");
            else if (切換工作目錄(引數列表[1]) < 0)
                回報錯誤("cd");
        } else if (命令相符(引數列表[0], "cat")) {
            if (引數個數 < 2)
                寫出文字("usage: cat FILE\n");
            else
                顯示檔案內容(引數列表[1]);
        } else if (命令相符(引數列表[0], "stat")) {
            if (引數個數 < 2)
                寫出文字("usage: stat FILE\n");
            else
                顯示檔案資訊(引數列表[1]);
        } else if (命令相符(引數列表[0], "pid"))
            顯示行程編號();
        else if (命令相符(引數列表[0], "uname"))
            顯示系統資訊();
        else if (命令相符(引數列表[0], "run"))
            執行程式(引數個數, 引數列表);
        else if (命令相符(引數列表[0], "udp"))
            測試資料報回送(引數個數 >= 2 ? 引數列表[1] : "ping");
        else if (命令相符(引數列表[0], "source")) {
            if (引數個數 < 2)
                寫出文字("usage: source FILE\n");
            else if (解譯命令檔案(引數列表[1]))
                return 1;
        } else if (命令相符(引數列表[0], "exit"))
            return 1;
        else
            寫出文字("unknown command; type help\n");
    }
}

int main(void)
{
    寫出文字("WORLDOS-SHELL:READY\n");
    (void)解譯輸入(標準輸入編號);
    寫出文字("WORLDOS-SHELL:EXIT\n");
    return 0;
}

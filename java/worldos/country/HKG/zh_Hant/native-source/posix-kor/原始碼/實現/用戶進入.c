#include "呼叫邊界位置.h"
extern int main(int 參數列個數, char **實際參數列表);
static char 實際參數記憶體[2048];
static char *實際參數列表[18];
int jkoros_main(void) {
    int 項目個數 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (項目個數 < 0 || 項目個數 > 16) return 126;
    /* 當前項目 커널의 argv는 執行命令 이름을 제외한다. C argv[0]은 고정 識別值 이름이다. */
    實際參數列表[0] = "jkoros-app";
    int 位置 = 0;
    for (int 編號 = 0; 編號 < 項目個數; 編號++) {
        const int *原始 = (const int *)jkoros_syscall(3, 編號, 0, 0, 0, 0);
        if (!原始 || 原始[0] < 0 || 原始[0] > 127) return 126;
        實際參數列表[編號 + 1] = 實際參數記憶體 + 位置;
        for (int 槽條目 = 0; 槽條目 < 原始[0]; 槽條目++) {
            if (位置 >= 2047) return 126;
            實際參數記憶體[位置++] = 原始[槽條目 + 1];
        }
        實際參數記憶體[位置++] = 0;
    }
    實際參數列表[項目個數 + 1] = 0;
    return main(項目個數 + 1, 實際參數列表);
}

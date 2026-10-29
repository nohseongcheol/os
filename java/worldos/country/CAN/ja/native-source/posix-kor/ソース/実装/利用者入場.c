#include "呼出し境界位置.h"
extern int main(int 引数列個数, char **引数一覧);
static char 引数記憶[2048];
static char *引数一覧[18];
int jkoros_main(void) {
    int 項目個数 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (項目個数 < 0 || 項目個数 > 16) return 126;
    /* 現在項目 커널의 argv는 命令実行 이름을 제외한다. C argv[0]은 고정 値識別処理 이름이다. */
    引数一覧[0] = "jkoros-app";
    int 位置 = 0;
    for (int 番号 = 0; 番号 < 項目個数; 番号++) {
        const int *原本 = (const int *)jkoros_syscall(3, 番号, 0, 0, 0, 0);
        if (!原本 || 原本[0] < 0 || 原本[0] > 127) return 126;
        引数一覧[番号 + 1] = 引数記憶 + 位置;
        for (int 槽入口 = 0; 槽入口 < 原本[0]; 槽入口++) {
            if (位置 >= 2047) return 126;
            引数記憶[位置++] = 原本[槽入口 + 1];
        }
        引数記憶[位置++] = 0;
    }
    引数一覧[項目個数 + 1] = 0;
    return main(項目個数 + 1, 引数一覧);
}

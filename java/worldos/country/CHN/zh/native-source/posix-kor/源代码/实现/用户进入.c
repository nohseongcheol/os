#include "调用边界位置.h"
extern int main(int 参数列个数, char **参数列表);
static char 参数内存[2048];
static char *参数列表[18];
int jkoros_main(void) {
    int 项目个数 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (项目个数 < 0 || 项目个数 > 16) return 126;
    /* 当前项目 커널의 argv는 执行命令 이름을 제외한다. C argv[0]은 고정 识别值 이름이다. */
    参数列表[0] = "jkoros-app";
    int 位置 = 0;
    for (int 编号 = 0; 编号 < 项目个数; 编号++) {
        const int *原始 = (const int *)jkoros_syscall(3, 编号, 0, 0, 0, 0);
        if (!原始 || 原始[0] < 0 || 原始[0] > 127) return 126;
        参数列表[编号 + 1] = 参数内存 + 位置;
        for (int 槽条目 = 0; 槽条目 < 原始[0]; 槽条目++) {
            if (位置 >= 2047) return 126;
            参数内存[位置++] = 原始[槽条目 + 1];
        }
        参数内存[位置++] = 0;
    }
    参数列表[项目个数 + 1] = 0;
    return main(项目个数 + 1, 参数列表);
}

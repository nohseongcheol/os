#include <文件ABI.h>
#include <stdio.h>
int main(int 项目个数, char **条目列表) {
    (void)项目个数; (void)条目列表;
    int 文件 = 打开文件("stored.txt", 读取写入 | 创建条件缺失 | 截断内容, 0600);
    if (文件 < 0 || 写入文件数据(文件, "saved-from-C", 12) != 12) return 1;
    if (提交文件存储装置(文件) < 0) return 2;
    if (关闭文件(文件) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}

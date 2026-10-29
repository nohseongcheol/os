#include <文件ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 参数列个数, char **参数列表) {
    if (参数列个数 < 1 || !参数列表[0]) return 2;
    const char 问候语[] = "内置 커널의 C와 中文 POSIX\n";
    int 文档集 = 打开文件("问候例.txt", 读取写入 | 创建条件缺失 | 截断内容, 0600);
    if (文档集 < 0) return 1;
    输入输出结果类型 长度 = 写入文件数据(文档集, 问候语, sizeof(问候语) - 1);
    关闭文件(文档集);
    写入文件数据(1, 问候语, sizeof(问候语) - 1);
    return 长度 == sizeof(问候语) - 1 ? 0 : 3;
}

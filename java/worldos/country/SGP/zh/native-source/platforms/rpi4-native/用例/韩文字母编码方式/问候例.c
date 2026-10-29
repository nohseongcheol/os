#include "文件ABI.h"
int 开始用户程序(int 实参) {
    (void)实参;
    const char 问候语[] = "C에서 한글 이름과 posix-kor 调用\n";
    int 文档集 = 打开文件("C인사.txt", 读取写入 | 创建条件缺失 | 截断内容, 0600);
    if (文档集 < 0) return 1;
    输入输出结果类型 已记录个数 = 写入文件数据(文档集, 问候语, sizeof(问候语) - 1);
    关闭文件(文档集);
    写入文件数据(1, 问候语, sizeof(问候语) - 1);
    return 已记录个数 == sizeof(问候语) - 1 ? 0 : 2;
}

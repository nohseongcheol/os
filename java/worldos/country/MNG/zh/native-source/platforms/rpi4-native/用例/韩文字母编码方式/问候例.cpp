#include "文件ABI.h"
class 文档管理器 {
    int 编号;
public:
    文档管理器(const char *名称) : 编号(打开文件(名称, 读取写入 | 创建条件缺失 | 截断内容, 0600)) {}
    ~文档管理器() { if (编号 >= 0) 关闭文件(编号); }
    输入输出结果类型 写入(const char *数据, 字节个数类型 大小) { return 写入文件数据(编号, 数据, 大小); }
};
extern "C" int 开始用户程序(int 实参) {
    (void)实参;
    const char 问候语[] = "C++에서 한글 클래스와 posix-kor 调用\n";
    文档管理器 文档集("C++问候例.txt");
    写入文件数据(1, 问候语, sizeof(问候语) - 1);
    return 文档集.写入(问候语, sizeof(问候语) - 1) == sizeof(问候语) - 1 ? 0 : 1;
}

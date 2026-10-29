#include "文件ABI.h"
#include "调用.h"
static int 初始设定器值;
static volatile int 初始设定器种子 = 72;
static volatile double 浮点型分种子 = 1.25;
static int 销毁状态个数;
struct 测试初始化 { 测试初始化() { 初始设定器值 = 初始设定器种子 + 1; } } 初始化静态区;
class 自动化文件 {
    int 编号;
public:
    explicit 自动化文件(const char *名称) : 编号(打开文件(名称, 读取写入 | 创建条件缺失 | 截断内容, 0600)) {}
    ~自动化文件() { if (编号 >= 0) 关闭文件(编号); 销毁状态个数++; }
    int 描述符条目() const { return 编号; }
};
extern "C" int 开始用户程序(int) {
    if (初始设定器值 != 73 || 用户调用(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double 浮点型分值 = 浮点型分种子 * 2.0 + 0.5;
    if (用户调用(0, 0, 0, 0, 0, 0, 0) != 1 || 浮点型分值 != 3.0) return 16;
    static const char 内容值[] = "EL0 C++ → posix-kor → Java 文件 · 안녕하세요 😀\n";
    char 读取值[sizeof(内容值)] = {};
    {
        自动化文件 文件("用户.txt");
        int 编号 = 文件.描述符条目();
        if (编号 < 0 || 写入文件数据(编号, 内容值, sizeof(内容值)) != sizeof(内容值)) return 2;
        if (寻道文件(编号, 0, 起点开头) || 读取文件数据(编号, 读取值, sizeof(读取值)) != sizeof(读取值)) return 3;
        for (unsigned 序数索引 = 0; 序数索引 < sizeof(内容值); 序数索引++) if (读取值[序数索引] != 内容值[序数索引]) return 4;
    }
    if (销毁状态个数 != 1) return 5;
    if (写入文件数据(1, 内容值, sizeof(内容值) - 1) != sizeof(内容值) - 1) return 6;
    uintptr_t 底端条目 = 用户内存结束(0);
    if (底端条目 != 0x02c00000 || 用户内存结束(底端条目 + 8192) != (intptr_t)(底端条目 + 8192)) return 7;
    volatile unsigned char *内存 = (volatile unsigned char *)底端条目;
    if (内存[0] || 内存[8191]) return 8;
    内存[8191] = 137;
    if (用户内存结束(底端条目) != (intptr_t)底端条目 || 用户内存结束(底端条目 + 8192) != (intptr_t)(底端条目 + 8192) || 内存[8191]) return 9;
    // 잘못된 用户 指针/번호는 오류이며 커널을 중단하지 않는다.
    if (写入文件数据(1, (const void *)0x80000, 8) != -1 || 错误编号 != 14) return 10;
    if (读取文件数据(0, (void *)内容值, 1) != -1 || 错误编号 != 14) return 11;
    if (用户调用(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 屏幕跨度 = 读取屏幕宽度(), 屏幕长度 = 读取屏幕高度();
    if (屏幕跨度 <= 0 || 屏幕长度 <= 0 || 用户调用(13, 屏幕跨度-1, 屏幕长度-1, 0, 2, 2, 0) != -22) return 13;
    if (屏幕矩形(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 退出程序 시 열린 서술자가 자동 정리되어야 한다.
    if (打开文件("用户.txt", 读取仅用值) < 0) return 15;
    return 0;
}

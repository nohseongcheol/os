#include <输入输出与执行.h>

static void 写出报文(const char *字符串, unsigned int 大小)
{
    (void)写入(标准输出编号, 字符串, 大小);
}

int main(void)
{
    char 输入位置[4];
    有符号大小类型 数量;

    写出报文("\nPOSIX-STDIN:READY\n", 19);
    数量 = 读取(标准输入编号, 输入位置, sizeof(输入位置));
    if (数量 == 2 && 输入位置[0] == 'a' && 输入位置[1] == '\n') {
        写出报文("POSIX-STDIN:PASS\n", 17);
        立即结束(0);
    }
    写出报文("POSIX-STDIN:FAIL\n", 17);
    立即结束(1);
}

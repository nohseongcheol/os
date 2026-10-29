#include <错误编号.h>
#include <文件控制.h>
#include <系统/子进程等待.h>
#include <输入输出与执行.h>

static void 写出报文(const char *字符串, unsigned int 大小)
{
    (void)写入(标准输出编号, 字符串, 大小);
}

int main(void)
{
    int 结束状态;
    int 文件描述编号;
    char *参数列表[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *环境列表[] = {(char *)"POSIX_TEST=1", (char *)0};

    写出报文("\nPOSIX-EXEC:START\n", 18);
    错误编号 = 0;
    if (等待指定子进程(-1, &结束状态, 未就绪则不等待) == -1 && 错误编号 == 错误没有子进程)
        写出报文("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        写出报文("PTEST:FAIL:waitpid-echild-empty\n", 32);
    错误编号 = 0;
    if (等待子进程(&结束状态) == -1 && 错误编号 == 错误没有子进程)
        写出报文("PTEST:PASS:wait-echild-empty\n", 29);
    else
        写出报文("PTEST:FAIL:wait-echild-empty\n", 29);

    文件描述编号 = 打开("/USER2", 只读打开);
    if (文件描述编号 < 0 || 按指定编号复制文件引用(文件描述编号, 10) != 10 || 控制文件(10, 设置描述编号标志, 替换程序时关闭) != 0) {
        写出报文("PTEST:FAIL:cloexec-setup\n", 25);
        立即结束(98);
    }
    if (文件描述编号 != 10)
        (void)关闭(文件描述编号);

    (void)替换执行内容("/PXEXEC", 参数列表, 环境列表);
    写出报文("PTEST:FAIL:exec-image\n", 22);
    立即结束(99);
}

#include <错误编号.h>
#include <系统/系统调用.h>

int 错误编号;
char **环境变量列表;

long __syscall_result(long 结果)
{
    if ((unsigned long)结果 >= (unsigned long)-4095) {
        错误编号 = (int)-结果;
        return -1;
    }
    return 结果;
}

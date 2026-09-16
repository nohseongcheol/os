/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <输入输出与执行.h>
#include <文件控制.h>
#include <错误编号.h>
#include <系统/文件状态.h>
int 测试函数集行为(void);

int main(void)
{
    char 数据缓冲区域[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int 文件描述编号 = 打开("/USER2", 只读打开);
    struct 文件状态 状态资料;
    if (文件描述编号 < 0 || 取得打开文件状态(文件描述编号, &状态资料) < 0 || 读取(文件描述编号, 数据缓冲区域, 4) != 4 ||
        (unsigned char)数据缓冲区域[0] != 0x7f || 数据缓冲区域[1] != 'E' || 数据缓冲区域[2] != 'L' || 数据缓冲区域[3] != 'F' ||
        移动读写位置(文件描述编号, 0, 从起点定位) != 0 || 关闭(文件描述编号) < 0 || 取得进程编号() <= 0)
        goto 失败标志;
    错误编号 = 0;
    if (读取(-1, 数据缓冲区域, 1) != -1 || 错误编号 != 错误描述编号无效)
        goto 失败标志;
    if (测试函数集行为() != 0)
        goto 失败标志;
    if (写入(标准输出编号, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto 失败标志;
    return 0;
失败标志:
    写入(标准输出编号, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}

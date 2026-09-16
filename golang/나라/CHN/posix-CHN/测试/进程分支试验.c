/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <系统/子进程等待.h>
#include <文件控制.h>
#include <输入输出与执行.h>

static void 写出报文(const char *字符串, unsigned int 大小)
{
    (void)写入(标准输出编号, 字符串, 大小);
}

int main(void)
{
    int 结束状态;
    进程编号类型 父进程 = 取得进程编号();
    进程编号类型 子项位置;
    进程编号类型 已等待进程;
    volatile int 进程私有值 = 10;
    int 文件描述编号;
    char 字节值;
    int 迭代次数;

    写出报文("\nPOSIX-FORK:START\n", 18);
    子项位置 = 分出子进程();
    if (子项位置 == 0) {
        进程私有值 = 20;
        if (取得父进程编号() != 父进程 || 进程私有值 != 20)
            立即结束(90);
        立即结束(23);
    }
    if (子项位置 < 0) {
        写出报文("PTEST:FAIL:fork-return\n", 23);
        立即结束(1);
    }
    写出报文("PTEST:PASS:fork-return\n", 23);
    已等待进程 = 等待指定子进程(子项位置, &结束状态, 0);
    if (已等待进程 == 子项位置 && 检查正常退出(结束状态) && 提取退出值(结束状态) == 23 &&
        进程私有值 == 10) {
        写出报文("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        写出报文("PTEST:FAIL:fork-wait-exit\n", 26);
        立即结束(1);
    }

    子项位置 = 分出子进程();
    if (子项位置 == 0)
        立即结束(29);
    已等待进程 = 等待子进程(&结束状态);
    if (已等待进程 == 子项位置 && 检查正常退出(结束状态) && 提取退出值(结束状态) == 29)
        写出报文("PTEST:PASS:blocking-wait\n", 25);
    else {
        写出报文("PTEST:FAIL:blocking-wait\n", 25);
        立即结束(1);
    }

    文件描述编号 = 打开("/USER2", 只读打开);
    子项位置 = 分出子进程();
    if (子项位置 == 0) {
        (void)关闭(文件描述编号);
        立即结束(0);
    }
    已等待进程 = 等待指定子进程(子项位置, &结束状态, 0);
    if (文件描述编号 >= 0 && 已等待进程 == 子项位置 && 读取(文件描述编号, &字节值, 1) == 1 &&
        (unsigned char)字节值 == 0x7f)
        写出报文("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        写出报文("PTEST:FAIL:fork-fd-isolation\n", 29);
        立即结束(1);
    }
    (void)关闭(文件描述编号);

    for (迭代次数 = 0; 迭代次数 < 2; 迭代次数++) {
        子项位置 = 分出子进程();
        if (子项位置 == 0)
            立即结束(迭代次数);
        if (子项位置 < 0 || 等待指定子进程(子项位置, &结束状态, 0) != 子项位置 ||
            !检查正常退出(结束状态) || 提取退出值(结束状态) != 迭代次数) {
            写出报文("PTEST:FAIL:fork-stress\n", 23);
            立即结束(1);
        }
    }
    写出报文("PTEST:PASS:fork-stress\n", 23);
    写出报文("POSIX-FORK:PASS\n", 16);
    立即结束(0);
}

#include <系统/子进程等待.h>
#include <输入输出与执行.h>

static void 写出报文(const char *字符串, unsigned int 大小)
{
    (void)写入(标准输出编号, 字符串, 大小);
}

int main(void)
{
    volatile unsigned char *起始位置 = (volatile unsigned char *)移动动态存储末端(0);
    volatile unsigned char *内存区域;
    进程编号类型 子项位置;
    int 结束状态;

    写出报文("\nPOSIX-HEAP:START\n", 18);
    内存区域 = (volatile unsigned char *)移动动态存储末端(32);
    if (起始位置 == (void *)-1 || 内存区域 != 起始位置 || 移动动态存储末端(0) != (void *)(起始位置 + 32)) {
        写出报文("PTEST:FAIL:sbrk-grow\n", 22);
        立即结束(1);
    }
    写出报文("PTEST:PASS:sbrk-grow\n", 22);
    内存区域[0] = 0x5a;
    内存区域[31] = 0xa5;
    if (内存区域[0] != 0x5a || 内存区域[31] != 0xa5) {
        写出报文("PTEST:FAIL:sbrk-memory\n", 24);
        立即结束(1);
    }
    写出报文("PTEST:PASS:sbrk-memory\n", 24);
    if (设定动态存储末端((void *)起始位置) != 0 || 移动动态存储末端(0) != (void *)起始位置) {
        写出报文("PTEST:FAIL:brk-restore\n", 24);
        立即结束(1);
    }
    写出报文("PTEST:PASS:brk-restore\n", 24);

    子项位置 = 分出子进程();
    if (子项位置 == 0) {
        if (移动动态存储末端(64) != (void *)起始位置)
            立即结束(2);
        立即结束(0);
    }
    if (子项位置 < 0 || 等待指定子进程(子项位置, &结束状态, 0) != 子项位置 ||
        !检查正常退出(结束状态) || 提取退出值(结束状态) != 0 ||
        移动动态存储末端(0) != (void *)起始位置) {
        写出报文("PTEST:FAIL:brk-process-isolation\n", 33);
        立即结束(1);
    }
    写出报文("PTEST:PASS:brk-process-isolation\n", 33);
    写出报文("POSIX-HEAP:PASS\n", 16);
    立即结束(0);
}

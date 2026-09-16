/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <输入输出与执行.h>
int 测试函数集行为(void);
int main(void)
{
    int 失败行号 = 测试函数集行为();
    if (失败行号) {
        char 数据缓冲区域[16];
        int 长度 = 0;
        写入(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { 数据缓冲区域[长度++] = (char)('0' + 失败行号 % 10); 失败行号 /= 10; } while (失败行号);
        while (长度) 写入(1, &数据缓冲区域[--长度], 1);
        写入(1, "\n", 1);
        return 1;
    }
    return 写入(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}

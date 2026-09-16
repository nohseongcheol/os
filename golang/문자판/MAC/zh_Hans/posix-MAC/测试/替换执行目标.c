/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <错误编号.h>
#include <文件控制.h>
#include <输入输出与执行.h>

static int 检查文本相等(const char *左值, const char *右值)
{
    unsigned int 项目索引 = 0;
    while (左值[项目索引] != 0 && 右值[项目索引] != 0) {
        if (左值[项目索引] != 右值[项目索引])
            return 0;
        项目索引++;
    }
    return 左值[项目索引] == 右值[项目索引];
}

int main(int 参数数量, char **参数列表, char **环境列表)
{
    static const char 加载值[] = "PTEST:PASS:exec-image\n";
    static const char 参数检查成功[] = "PTEST:PASS:exec-argv-envp\n";
    static const char 参数检查失败[] = "PTEST:FAIL:exec-argv-envp\n";

    (void)写入(标准输出编号, 加载值, sizeof(加载值) - 1);
    if (参数数量 == 2 && 参数列表 != (char **)0 && 环境列表 != (char **)0 &&
        参数列表[0] != (char *)0 && 参数列表[1] != (char *)0 && 参数列表[2] == (char *)0 &&
        环境列表[0] != (char *)0 && 环境列表[1] == (char *)0 &&
        环境变量列表 == 环境列表 && 检查文本相等(参数列表[0], "PXEXEC") &&
        检查文本相等(参数列表[1], "argument") && 检查文本相等(环境列表[0], "POSIX_TEST=1")) {
        (void)写入(标准输出编号, 参数检查成功, sizeof(参数检查成功) - 1);
    } else {
        (void)写入(标准输出编号, 参数检查失败, sizeof(参数检查失败) - 1);
        立即结束(38);
    }
    错误编号 = 0;
    if (控制文件(10, 取得描述编号标志) == -1 && 错误编号 == 错误描述编号无效) {
        static const char 程序替换时关闭成功[] = "PTEST:PASS:cloexec\n";
        (void)写入(标准输出编号, 程序替换时关闭成功, sizeof(程序替换时关闭成功) - 1);
        立即结束(37);
    }
    {
        static const char 程序替换时关闭失败[] = "PTEST:FAIL:cloexec\n";
        (void)写入(标准输出编号, 程序替换时关闭失败, sizeof(程序替换时关闭失败) - 1);
    }
    立即结束(39);
}

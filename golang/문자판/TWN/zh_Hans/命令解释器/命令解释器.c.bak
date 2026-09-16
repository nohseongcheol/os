#include <通信地址/字节顺序.h>
#include <错误编号.h>
#include <文件控制.h>
#include <互联网络/地址.h>
#include <基本定义.h>
#include <系统/通信端点.h>
#include <系统/文件状态.h>
#include <系统/系统身份.h>
#include <系统/子进程等待.h>
#include <输入输出与执行.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { 输入行容量 = 512, 最大参数个数 = 16, 最大命令文件嵌套层数 = 4 };
static int 命令文件嵌套深度;
struct 输入流 {
    int 输入描述符;
    char 传输缓冲区[256];
    大小类型 位置;
    大小类型 长度;
};

static 大小类型 文本字节长度(const char *文本)
{
    大小类型 长度 = 0;
    while (文本[长度] != '\0')
        长度++;
    return 长度;
}

static int 文本相同(const char *左侧, const char *右侧)
{
    大小类型 位置 = 0;
    while (左侧[位置] == 右侧[位置]) {
        if (左侧[位置] == '\0')
            return 1;
        位置++;
    }
    return 0;
}

static void 写出文本(const char *文本)
{
    大小类型 长度 = 文本字节长度(文本);
    while (长度 > 0U) {
        有符号大小类型 已写字节数 = 写入(标准输出编号, 文本, 长度);
        if (已写字节数 <= 0)
            return;
        文本 += 已写字节数;
        长度 -= (大小类型)已写字节数;
    }
}

static void 写出整数(int 数值)
{
    char 数字字符[16];
    unsigned int 数位个数;
    unsigned int 无符号数值;

    if (数值 < 0) {
        写出文本("-");
        无符号数值 = (unsigned int)(-(数值 + 1)) + 1U;
    } else {
        无符号数值 = (unsigned int)数值;
    }
    数位个数 = 0;
    do {
        数字字符[数位个数++] = (char)('0' + 无符号数值 % 10U);
        无符号数值 /= 10U;
    } while (无符号数值 != 0U);
    while (数位个数 > 0U) {
        数位个数--;
        (void)写入(标准输出编号, &数字字符[数位个数], 1);
    }
}

static void 报告错误(const char *操作)
{
    写出文本("error: ");
    写出文本(操作);
    写出文本(" errno=");
    写出整数(错误编号);
    写出文本("\n");
}

static int 读取输入行(struct 输入流 *输入, char *输入行, 大小类型 容量)
{
    大小类型 位置 = 0;
    int 无效输入行 = 0;
    char 字符;
    有符号大小类型 已读字节数;
    if (容量 < 2U)
        return -2;
    for (;;) {
        if (输入->位置 == 输入->长度) {
            已读字节数 = 读取(输入->输入描述符, 输入->传输缓冲区, sizeof(输入->传输缓冲区));
            if (已读字节数 < 0) {
                if (错误编号 == 错误操作被中断)
                    continue;
                return -1;
            }
            if (已读字节数 == 0) {
                if (位置 == 0 && !无效输入行)
                    return -1;
                break;
            }
            输入->长度 = (大小类型)已读字节数;
            输入->位置 = 0;
        }
        字符 = 输入->传输缓冲区[输入->位置++];
        if (字符 == '\n')
            break;
        if (输入->输入描述符 == 标准输入编号 && 字符 == 4) {
            if (位置 == 0 && !无效输入行)
                return -1;
            break;
        }
        if (输入->输入描述符 == 标准输入编号 && (字符 == 8 || 字符 == 127)) {
            if (位置 > 0) {
                do {
                    位置--;
                } while (位置 > 0 && ((unsigned char)输入行[位置] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (字符 == '\r')
            continue;
        if (字符 == '\0') {
            无效输入行 = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (位置 + 1U < 容量)
            输入行[位置++] = 字符;
        else
            无效输入行 = 1;
    }
    输入行[位置] = '\0';
    return 无效输入行 ? -2 : (int)位置;
}

static int 拆分参数(char *输入行, char **参数列表)
{
    int 参数个数 = 0;
    char *当前位置 = 输入行;
    char *输出位置 = 输入行;

    while (*当前位置 != '\0') {
        char 引号 = '\0';
        while (*当前位置 == ' ' || *当前位置 == '\t')
            当前位置++;
        if (*当前位置 == '\0' || *当前位置 == '#')
            break;
        if (参数个数 == 最大参数个数 - 1)
            return -1;
        参数列表[参数个数++] = 输出位置;
        while (*当前位置 != '\0') {
            char 字符 = *当前位置++;
            if (引号 == '\0' && (字符 == ' ' || 字符 == '\t'))
                break;
            if (字符 == '\\' && 引号 != '\'') {
                if (*当前位置 == '\0')
                    return -1;
                *输出位置++ = *当前位置++;
            } else if (字符 == '\'' || 字符 == '"') {
                if (引号 == '\0')
                    引号 = 字符;
                else if (引号 == 字符)
                    引号 = '\0';
                else
                    *输出位置++ = 字符;
            } else {
                *输出位置++ = 字符;
            }
        }
        if (引号 != '\0')
            return -1;
        *输出位置++ = '\0';
    }
    参数列表[参数个数] = (char *)0;
    return 参数个数;
}

static void 显示帮助(void)
{
    大小类型 位置;
    写出文本(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    写出文本("Native command proposals (ASCII aliases remain available):\n");
    for (位置 = 0; 位置 < sizeof(基准命令) / sizeof(基准命令[0]); 位置++) {
        写出文本(本地语言命令别名[位置]);
        写出文本(" = ");
        写出文本(基准命令[位置]);
        写出文本("\n");
    }
}

static int 命令匹配(const char *文本, const char *命令)
{
    大小类型 位置;
    if (文本相同(文本, 命令))
        return 1;
    for (位置 = 0; 位置 < sizeof(基准命令) / sizeof(基准命令[0]); 位置++)
        if (文本相同(命令, 基准命令[位置]))
            return 文本相同(文本, 本地语言命令别名[位置]);
    return 0;
}

static int 解释输入(int 输入描述符);

static int 解释命令文件(const char *文件名)
{
    int 文件描述符;
    int 状态;
    if (命令文件嵌套深度 >= 最大命令文件嵌套层数) {
        写出文本("source: nesting limit\n");
        return 0;
    }
    文件描述符 = 打开(文件名, 只读打开);
    if (文件描述符 < 0) {
        报告错误(文件名);
        return 0;
    }
    命令文件嵌套深度++;
    状态 = 解释输入(文件描述符);
    命令文件嵌套深度--;
    (void)关闭(文件描述符);
    return 状态;
}

static void 显示参数(int 参数个数, char **参数列表)
{
    int 位置;
    for (位置 = 1; 位置 < 参数个数; 位置++) {
        if (位置 != 1)
            写出文本(" ");
        写出文本(参数列表[位置]);
    }
    写出文本("\n");
}

static void 显示当前目录(void)
{
    char 路径[128];
    if (取得工作目录路径(路径, sizeof(路径)) == (char *)0) {
        报告错误("pwd");
        return;
    }
    写出文本(路径);
    写出文本("\n");
}

static void 显示文件内容(const char *文件名)
{
    char 传输缓冲区[128];
    int 文件描述符 = 打开(文件名, 只读打开);
    有符号大小类型 已读字节数;

    if (文件描述符 < 0) {
        报告错误("cat");
        return;
    }
    while ((已读字节数 = 读取(文件描述符, 传输缓冲区, sizeof(传输缓冲区))) > 0)
        (void)写入(标准输出编号, 传输缓冲区, (大小类型)已读字节数);
    if (已读字节数 < 0)
        报告错误("cat/read");
    (void)关闭(文件描述符);
    写出文本("\n");
}

static void 显示文件信息(const char *文件名)
{
    struct 文件状态 状态;
    if (文件状态(文件名, &状态) < 0) {
        报告错误("stat");
        return;
    }
    写出文本("size=");
    写出整数((int)状态.文件大小);
    写出文本(检查目录模式(状态.文件类型与权限) ? " type=directory\n" : " type=file\n");
}

static void 显示进程编号(void)
{
    写出文本("pid=");
    写出整数((int)取得进程编号());
    写出文本(" ppid=");
    写出整数((int)取得父进程编号());
    写出文本("\n");
}

static void 显示系统信息(void)
{
    struct 系统身份信息_2 系统身份信息;
    if (取得系统信息(&系统身份信息) < 0) {
        报告错误("uname");
        return;
    }
    写出文本(系统身份信息.系统名称);
    写出文本(" ");
    写出文本(系统身份信息.系统发行版);
    写出文本(" ");
    写出文本(系统身份信息.机器类型);
    写出文本("\n");
}

static void 运行程序(int 参数个数, char **参数列表)
{
    进程编号类型 子进程编号;
    int 子进程终止状态 = 0;

    if (参数个数 < 2) {
        写出文本("usage: run FILE [ARGS...]\n");
        return;
    }
    子进程编号 = 分出子进程();
    if (子进程编号 < 0) {
        报告错误("fork");
        return;
    }
    if (子进程编号 == 0) {
        替换执行内容(参数列表[1], &参数列表[1], (char *const *)0);
        报告错误("execve");
        立即结束(127);
    }
    if (等待指定子进程(子进程编号, &子进程终止状态, 0) < 0) {
        报告错误("waitpid");
        return;
    }
    写出文本("exit-status=");
    写出整数(提取退出值(子进程终止状态));
    写出文本("\n");
}

static void 测试数据报回送(const char *消息)
{
    struct 互联网络端点地址 接收端点地址 = {0};
    struct 互联网络端点地址 发送端点地址 = {0};
    地址长度类型 发送地址长度 = sizeof(发送端点地址);
    char 收到的数据[96];
    大小类型 消息字节长度 = 文本字节长度(消息);
    int 接收套接字 = -1;
    int 发送套接字 = -1;
    有符号大小类型 接收字节数;

    if (消息字节长度 >= sizeof(收到的数据)) {
        写出文本("udp: message exceeds 95 bytes\n");
        return;
    }
    接收套接字 = 创建通信端点(互联网络地址族, 数据报端点, 用户数据报协议);
    发送套接字 = 创建通信端点(互联网络地址族, 数据报端点, 用户数据报协议);
    if (接收套接字 < 0 || 发送套接字 < 0) {
        报告错误("socket");
        goto 关闭套接字;
    }
    接收端点地址.互联地址族 = 互联网络地址族;
    接收端点地址.通信端口编号 = 转为网络次序16位(40404);
    接收端点地址.互联地址内容.地址值 = 转为网络次序32位(本机回环地址);
    if (绑定本地地址(接收套接字, (const struct 通信端点地址 *)&接收端点地址, sizeof(接收端点地址)) < 0) {
        报告错误("bind");
        goto 关闭套接字;
    }
    if (连接对端(发送套接字, (const struct 通信端点地址 *)&接收端点地址, sizeof(接收端点地址)) < 0) {
        报告错误("connect");
        goto 关闭套接字;
    }
    if (发送(发送套接字, 消息, 消息字节长度, 0) != (有符号大小类型)消息字节长度) {
        报告错误("send");
        goto 关闭套接字;
    }
    接收字节数 = 接收并取得来源地址(接收套接字, 收到的数据, sizeof(收到的数据) - 1U, 0,
                         (struct 通信端点地址 *)&发送端点地址, &发送地址长度);
    if (接收字节数 < 0) {
        报告错误("recvfrom");
        goto 关闭套接字;
    }
    收到的数据[接收字节数] = '\0';
    写出文本("udp-received: ");
    写出文本(收到的数据);
    写出文本("\n");

关闭套接字:
    if (发送套接字 >= 0)
        (void)关闭(发送套接字);
    if (接收套接字 >= 0)
        (void)关闭(接收套接字);
}

static int 解释输入(int 输入描述符)
{
    char 输入行[输入行容量];
    char *参数列表[最大参数个数];
    struct 输入流 输入 = {0};
    输入.输入描述符 = 输入描述符;

    for (;;) {
        int 参数个数;
        int 状态;
        if (输入描述符 == 标准输入编号)
            写出文本("worldos$ ");
        状态 = 读取输入行(&输入, 输入行, sizeof(输入行));
        if (状态 == -1)
            return 0;
        if (状态 == -2) {
            写出文本("input rejected: overlong or binary line\n");
            continue;
        }
        参数个数 = 拆分参数(输入行, 参数列表);
        if (参数个数 < 0) {
            写出文本("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (参数个数 == 0)
            continue;
        if (命令匹配(参数列表[0], "help"))
            显示帮助();
        else if (命令匹配(参数列表[0], "echo"))
            显示参数(参数个数, 参数列表);
        else if (命令匹配(参数列表[0], "pwd"))
            显示当前目录();
        else if (命令匹配(参数列表[0], "cd")) {
            if (参数个数 < 2)
                写出文本("usage: cd PATH\n");
            else if (切换工作目录(参数列表[1]) < 0)
                报告错误("cd");
        } else if (命令匹配(参数列表[0], "cat")) {
            if (参数个数 < 2)
                写出文本("usage: cat FILE\n");
            else
                显示文件内容(参数列表[1]);
        } else if (命令匹配(参数列表[0], "stat")) {
            if (参数个数 < 2)
                写出文本("usage: stat FILE\n");
            else
                显示文件信息(参数列表[1]);
        } else if (命令匹配(参数列表[0], "pid"))
            显示进程编号();
        else if (命令匹配(参数列表[0], "uname"))
            显示系统信息();
        else if (命令匹配(参数列表[0], "run"))
            运行程序(参数个数, 参数列表);
        else if (命令匹配(参数列表[0], "udp"))
            测试数据报回送(参数个数 >= 2 ? 参数列表[1] : "ping");
        else if (命令匹配(参数列表[0], "source")) {
            if (参数个数 < 2)
                写出文本("usage: source FILE\n");
            else if (解释命令文件(参数列表[1]))
                return 1;
        } else if (命令匹配(参数列表[0], "exit"))
            return 1;
        else
            写出文本("unknown command; type help\n");
    }
}

int main(void)
{
    写出文本("WORLDOS-SHELL:READY\n");
    (void)解释输入(标准输入编号);
    写出文本("WORLDOS-SHELL:EXIT\n");
    return 0;
}

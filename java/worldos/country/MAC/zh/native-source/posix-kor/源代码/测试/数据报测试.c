#include <文件ABI.h>
#include <网络ABI.h>
#include <string.h>
#include <stdio.h>

#define 验证(条件) do { if (!(条件)) { puts("POSIX UDP CHECK FAILED: " #条件); return 1; } } while (0)
int main(int 参数列个数, char **参数列表) {
    验证(参数列个数 == 2);
    int 端口编号 = 0;
    for (int 槽条目 = 0; 参数列表[1][槽条目]; 槽条目++) {
        验证(参数列表[1][槽条目] >= '0' && 参数列表[1][槽条目] <= '9');
        端口编号 = 端口编号 * 10 + 参数列表[1][槽条目] - '0';
        验证(端口编号 <= 65535);
    }
    int 端点值 = 创建端点(AF_INET, SOCK_DGRAM, 0);
    验证(端点值 == 3);
    struct sockaddr_in 局部作用域 = {0}, 对端值 = {0}, 已接收地址 = {0};
    局部作用域.sin_family = AF_INET;
    socklen_t 长度 = sizeof 局部作用域;
    验证(读取套接字地址(端点值, (struct sockaddr *)&局部作用域, &长度) == 0 && 局部作用域.sin_port == 0);
    验证(绑定地址(端点值, (struct sockaddr *)&局部作用域, sizeof 局部作用域) == 0);
    验证(读取套接字地址(端点值, (struct sockaddr *)&局部作用域, &长度) == 0 && ntohs(局部作用域.sin_port) >= 49152);
    验证(绑定地址(端点值, (struct sockaddr *)&局部作用域, sizeof 局部作用域) == -1 && errno == EINVAL);
    int 第二序数 = socket(AF_INET, SOCK_DGRAM, 0);
    验证(bind(第二序数, (struct sockaddr *)&局部作用域, sizeof 局部作用域) == -1 && errno == EADDRINUSE);
    验证(close(第二序数) == 0);
    第二序数 = dup(端点值);
    验证(close(端点值) == 0); 端点值 = 第二序数;
    对端值.sin_family = AF_INET; 对端值.sin_port = 网络短整数(端口编号);
    验证(解析网络地址(AF_INET, "10.0.2.2", &对端值.sin_addr) == 1);
    struct timeval 等待状态值 = {0, 200000};
    验证(更改网络设置(端点值, SOL_SOCKET, SO_RCVTIMEO, &等待状态值, sizeof 等待状态值) == 0);
    char 数据[32];
    验证(接收数据报数据(端点值, 数据, sizeof 数据, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    验证(发送数据报数据(端点值, "posix-udp", 9, 0, (struct sockaddr *)&对端值, sizeof 对端值) == 9);
    长度 = sizeof 已接收地址;
    验证(recvfrom(端点值, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    验证(接收数据报数据(端点值, 数据, sizeof 数据, 0, (struct sockaddr *)&已接收地址, &长度) == 9);
    验证(memcmp(数据, "posix-udp", 9) == 0 && 长度 == 16);
    验证(已接收地址.sin_port == 对端值.sin_port && 已接收地址.sin_addr.s_addr == 对端值.sin_addr.s_addr);
    验证(sendto(端点值, "truncate", 8, 0, (struct sockaddr *)&对端值, sizeof 对端值) == 8);
    验证(recvfrom(端点值, 数据, 3, 0, NULL, NULL) == 3 && memcmp(数据, "tru", 3) == 0);
    验证(recvfrom(端点值, 数据, sizeof 数据, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    验证(sendto(端点值, NULL, 0, 0, (struct sockaddr *)&对端值, sizeof 对端值) == 0);
    验证(recvfrom(端点值, NULL, 0, 0, NULL, NULL) == 0);
    验证(recvfrom(端点值, 数据, sizeof 数据, 0, NULL, NULL) == -1 && errno == EAGAIN);
    验证(close(端点值) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

#include <檔案ABI.h>
#include <網路ABI.h>
#include <string.h>
#include <stdio.h>

#define 驗證(條件) do { if (!(條件)) { puts("POSIX UDP CHECK FAILED: " #條件); return 1; } } while (0)
int main(int 參數列個數, char **實際參數列表) {
    驗證(參數列個數 == 2);
    int 埠編號 = 0;
    for (int 槽條目 = 0; 實際參數列表[1][槽條目]; 槽條目++) {
        驗證(實際參數列表[1][槽條目] >= '0' && 實際參數列表[1][槽條目] <= '9');
        埠編號 = 埠編號 * 10 + 實際參數列表[1][槽條目] - '0';
        驗證(埠編號 <= 65535);
    }
    int 端點值 = 創建端點(AF_INET, SOCK_DGRAM, 0);
    驗證(端點值 == 3);
    struct sockaddr_in 局部作用域 = {0}, 對端值 = {0}, 已接收地址 = {0};
    局部作用域.sin_family = AF_INET;
    socklen_t 長度 = sizeof 局部作用域;
    驗證(讀取通訊端地址(端點值, (struct sockaddr *)&局部作用域, &長度) == 0 && 局部作用域.sin_port == 0);
    驗證(綁定地址(端點值, (struct sockaddr *)&局部作用域, sizeof 局部作用域) == 0);
    驗證(讀取通訊端地址(端點值, (struct sockaddr *)&局部作用域, &長度) == 0 && ntohs(局部作用域.sin_port) >= 49152);
    驗證(綁定地址(端點值, (struct sockaddr *)&局部作用域, sizeof 局部作用域) == -1 && errno == EINVAL);
    int 第二序數 = socket(AF_INET, SOCK_DGRAM, 0);
    驗證(bind(第二序數, (struct sockaddr *)&局部作用域, sizeof 局部作用域) == -1 && errno == EADDRINUSE);
    驗證(close(第二序數) == 0);
    第二序數 = dup(端點值);
    驗證(close(端點值) == 0); 端點值 = 第二序數;
    對端值.sin_family = AF_INET; 對端值.sin_port = 網路短整數(埠編號);
    驗證(解析網路地址(AF_INET, "10.0.2.2", &對端值.sin_addr) == 1);
    struct timeval 等待狀態值 = {0, 200000};
    驗證(更改網路設置(端點值, SOL_SOCKET, SO_RCVTIMEO, &等待狀態值, sizeof 等待狀態值) == 0);
    char 資料[32];
    驗證(接收數據報資料(端點值, 資料, sizeof 資料, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    驗證(發送數據報資料(端點值, "posix-udp", 9, 0, (struct sockaddr *)&對端值, sizeof 對端值) == 9);
    長度 = sizeof 已接收地址;
    驗證(recvfrom(端點值, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    驗證(接收數據報資料(端點值, 資料, sizeof 資料, 0, (struct sockaddr *)&已接收地址, &長度) == 9);
    驗證(memcmp(資料, "posix-udp", 9) == 0 && 長度 == 16);
    驗證(已接收地址.sin_port == 對端值.sin_port && 已接收地址.sin_addr.s_addr == 對端值.sin_addr.s_addr);
    驗證(sendto(端點值, "truncate", 8, 0, (struct sockaddr *)&對端值, sizeof 對端值) == 8);
    驗證(recvfrom(端點值, 資料, 3, 0, NULL, NULL) == 3 && memcmp(資料, "tru", 3) == 0);
    驗證(recvfrom(端點值, 資料, sizeof 資料, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    驗證(sendto(端點值, NULL, 0, 0, (struct sockaddr *)&對端值, sizeof 對端值) == 0);
    驗證(recvfrom(端點值, NULL, 0, 0, NULL, NULL) == 0);
    驗證(recvfrom(端點值, 資料, sizeof 資料, 0, NULL, NULL) == -1 && errno == EAGAIN);
    驗證(close(端點值) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

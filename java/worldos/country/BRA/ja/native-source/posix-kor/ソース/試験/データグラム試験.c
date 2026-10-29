#include <ファイルABI.h>
#include <通信網ABI.h>
#include <string.h>
#include <stdio.h>

#define 検証(条件) do { if (!(条件)) { puts("POSIX UDP CHECK FAILED: " #条件); return 1; } } while (0)
int main(int 引数列個数, char **引数一覧) {
    検証(引数列個数 == 2);
    int ポート番号 = 0;
    for (int 槽入口 = 0; 引数一覧[1][槽入口]; 槽入口++) {
        検証(引数一覧[1][槽入口] >= '0' && 引数一覧[1][槽入口] <= '9');
        ポート番号 = ポート番号 * 10 + 引数一覧[1][槽入口] - '0';
        検証(ポート番号 <= 65535);
    }
    int 通信端点値 = 通信端点作成(AF_INET, SOCK_DGRAM, 0);
    検証(通信端点値 == 3);
    struct sockaddr_in 局所有効範囲 = {0}, 通信相手値 = {0}, 受信済み番地 = {0};
    局所有効範囲.sin_family = AF_INET;
    socklen_t 長さ = sizeof 局所有効範囲;
    検証(ソケット番地読取(通信端点値, (struct sockaddr *)&局所有効範囲, &長さ) == 0 && 局所有効範囲.sin_port == 0);
    検証(番地結合(通信端点値, (struct sockaddr *)&局所有効範囲, sizeof 局所有効範囲) == 0);
    検証(ソケット番地読取(通信端点値, (struct sockaddr *)&局所有効範囲, &長さ) == 0 && ntohs(局所有効範囲.sin_port) >= 49152);
    検証(番地結合(通信端点値, (struct sockaddr *)&局所有効範囲, sizeof 局所有効範囲) == -1 && errno == EINVAL);
    int 第二序数 = socket(AF_INET, SOCK_DGRAM, 0);
    検証(bind(第二序数, (struct sockaddr *)&局所有効範囲, sizeof 局所有効範囲) == -1 && errno == EADDRINUSE);
    検証(close(第二序数) == 0);
    第二序数 = dup(通信端点値);
    検証(close(通信端点値) == 0); 通信端点値 = 第二序数;
    通信相手値.sin_family = AF_INET; 通信相手値.sin_port = 通信網短整数(ポート番号);
    検証(通信網番地解析(AF_INET, "10.0.2.2", &通信相手値.sin_addr) == 1);
    struct timeval 値待合 = {0, 200000};
    検証(通信網設定値変更(通信端点値, SOL_SOCKET, SO_RCVTIMEO, &値待合, sizeof 値待合) == 0);
    char データ[32];
    検証(データグラムデータ受取(通信端点値, データ, sizeof データ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    検証(データグラムデータ送信(通信端点値, "posix-udp", 9, 0, (struct sockaddr *)&通信相手値, sizeof 通信相手値) == 9);
    長さ = sizeof 受信済み番地;
    検証(recvfrom(通信端点値, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    検証(データグラムデータ受取(通信端点値, データ, sizeof データ, 0, (struct sockaddr *)&受信済み番地, &長さ) == 9);
    検証(memcmp(データ, "posix-udp", 9) == 0 && 長さ == 16);
    検証(受信済み番地.sin_port == 通信相手値.sin_port && 受信済み番地.sin_addr.s_addr == 通信相手値.sin_addr.s_addr);
    検証(sendto(通信端点値, "truncate", 8, 0, (struct sockaddr *)&通信相手値, sizeof 通信相手値) == 8);
    検証(recvfrom(通信端点値, データ, 3, 0, NULL, NULL) == 3 && memcmp(データ, "tru", 3) == 0);
    検証(recvfrom(通信端点値, データ, sizeof データ, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    検証(sendto(通信端点値, NULL, 0, 0, (struct sockaddr *)&通信相手値, sizeof 通信相手値) == 0);
    検証(recvfrom(通信端点値, NULL, 0, 0, NULL, NULL) == 0);
    検証(recvfrom(通信端点値, データ, sizeof データ, 0, NULL, NULL) == -1 && errno == EAGAIN);
    検証(close(通信端点値) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}

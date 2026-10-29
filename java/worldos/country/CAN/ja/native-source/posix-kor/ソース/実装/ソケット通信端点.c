#include <通信網ABI.h>
#include <errno.h>
#include "呼出し境界位置.h"

int socket(int 番地方式体系, int 通信網種別, int 契約番号) {
    return 呼出状態結果(jkoros_syscall(41, 番地方式体系, 通信網種別, 契約番号, 0, 0));
}
int bind(int ファイル記述子, const struct sockaddr *番地, socklen_t 番地長さ) {
    return 呼出状態結果(jkoros_syscall(42, ファイル記述子, (int)番地, 番地長さ, 0, 0));
}
ssize_t sendto(int ファイル記述子, const void *データ, size_t バイト個数, int 設定値,
               const struct sockaddr *番地, socklen_t 番地長さ) {
    int 要求[2] = {(int)番地, 番地長さ};
    return 呼出状態結果(jkoros_syscall(43, ファイル記述子, (int)データ, バイト個数, 設定値, (int)要求));
}
ssize_t recvfrom(int ファイル記述子, void *データ, size_t バイト個数, int 設定値,
                 struct sockaddr *番地, socklen_t *番地長さ) {
    int 要求[2] = {(int)番地, (int)番地長さ};
    return 呼出状態結果(jkoros_syscall(44, ファイル記述子, (int)データ, バイト個数, 設定値, (int)要求));
}
int getsockname(int ファイル記述子, struct sockaddr *番地, socklen_t *番地長さ) {
    return 呼出状態結果(jkoros_syscall(45, ファイル記述子, (int)番地, (int)番地長さ, 0, 0));
}
int setsockopt(int ファイル記述子, int 階層値, int 設定値名前, const void *値, socklen_t 値長さ) {
    if (階層値 != SOL_SOCKET || 設定値名前 != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!値) { errno = EFAULT; return -1; }
    if (値長さ != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *時間値 = 値;
    if (時間値->tv_sec < 0 || 時間値->tv_sec > 2 || 時間値->tv_usec < 0 || 時間値->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int ミリ秒 = 時間値->tv_sec * 1000 + (時間値->tv_usec + 999) / 1000;
    return 呼出状態結果(jkoros_syscall(46, ファイル記述子, ミリ秒, 0, 0, 0));
}
uint16_t htons(uint16_t 値) { return (値 << 8) | (値 >> 8); }
uint16_t ntohs(uint16_t 値) { return htons(値); }
uint32_t htonl(uint32_t 値) {
    return (値 << 24) | ((値 << 8) & 0xff0000U) | ((値 >> 8) & 0xff00U) | (値 >> 24);
}
uint32_t ntohl(uint32_t 値) { return htonl(値); }
int inet_pton(int 番地方式体系, const char *文字列, void *番地) {
    if (番地方式体系 != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!文字列 || !番地) { errno = EFAULT; return -1; }
    unsigned char 一時値[4];
    for (int 槽入口 = 0; 槽入口 < 4; 槽入口++) {
        int 値 = 0, 桁数 = 0;
        const char *起動処理 = 文字列;
        while (*文字列 >= '0' && *文字列 <= '9') {
            if (++桁数 > 3) return 0;
            値 = 値 * 10 + *文字列++ - '0';
        }
        if (!桁数 || 値 > 255 || (桁数 > 1 && *起動処理 == '0')) return 0;
        一時値[槽入口] = 値;
        if (槽入口 < 3) { if (*文字列++ != '.') return 0; }
        else if (*文字列) return 0;
    }
    for (int 槽入口 = 0; 槽入口 < 4; 槽入口++) ((unsigned char *)番地)[槽入口] = 一時値[槽入口];
    return 1;
}
const char *inet_ntop(int 番地方式体系, const void *番地, char *文字列, socklen_t 容積値) {
    if (番地方式体系 != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!番地 || !文字列) { errno = EFAULT; return 0; }
    const unsigned char *数 = 番地;
    char 一時値[16]; unsigned int 長さ = 0;
    for (int 槽入口 = 0; 槽入口 < 4; 槽入口++) {
        unsigned int 値 = 数[槽入口];
        if (値 >= 100) 一時値[長さ++] = '0' + 値 / 100;
        if (値 >= 10) 一時値[長さ++] = '0' + 値 / 10 % 10;
        一時値[長さ++] = '0' + 値 % 10;
        if (槽入口 < 3) 一時値[長さ++] = '.';
    }
    一時値[長さ++] = 0;
    if (容積値 < 長さ) { errno = ENOSPC; return 0; }
    for (unsigned int 槽入口 = 0; 槽入口 < 長さ; 槽入口++) 文字列[槽入口] = 一時値[槽入口];
    return 文字列;
}

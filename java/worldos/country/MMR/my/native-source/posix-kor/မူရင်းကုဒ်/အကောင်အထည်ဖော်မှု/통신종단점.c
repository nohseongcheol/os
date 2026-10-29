#include <통신규약.h>
#include <errno.h>
#include "ခေါ်နယ်နိမိတ်.h"

int socket(int လိပ်စာအစီအစဉ်, int ကွန်ရက်အမျိုးအစား, int သဘောတူစည်းမျဉ်းကိန်း) {
    return 호출결과(jkoros_syscall(41, လိပ်စာအစီအစဉ်, ကွန်ရက်အမျိုးအစား, သဘောတူစည်းမျဉ်းကိန်း, 0, 0));
}
int bind(int ဖိုင်အညွှန်း, const struct sockaddr *လိပ်စာ, socklen_t လိပ်စာအလျား) {
    return 호출결과(jkoros_syscall(42, ဖိုင်အညွှန်း, (int)လိပ်စာ, လိပ်စာအလျား, 0, 0));
}
ssize_t sendto(int ဖိုင်အညွှန်း, const void *ဒေတာ, size_t ဘိုက်အရေအတွက်, int သတ်မှတ်ချက်,
               const struct sockaddr *လိပ်စာ, socklen_t လိပ်စာအလျား) {
    int တောင်းဆိုချက်[2] = {(int)လိပ်စာ, လိပ်စာအလျား};
    return 호출결과(jkoros_syscall(43, ဖိုင်အညွှန်း, (int)ဒေတာ, ဘိုက်အရေအတွက်, သတ်မှတ်ချက်, (int)တောင်းဆိုချက်));
}
ssize_t recvfrom(int ဖိုင်အညွှန်း, void *ဒေတာ, size_t ဘိုက်အရေအတွက်, int သတ်မှတ်ချက်,
                 struct sockaddr *လိပ်စာ, socklen_t *လိပ်စာအလျား) {
    int တောင်းဆိုချက်[2] = {(int)လိပ်စာ, (int)လိပ်စာအလျား};
    return 호출결과(jkoros_syscall(44, ဖိုင်အညွှန်း, (int)ဒေတာ, ဘိုက်အရေအတွက်, သတ်မှတ်ချက်, (int)တောင်းဆိုချက်));
}
int getsockname(int ဖိုင်အညွှန်း, struct sockaddr *လိပ်စာ, socklen_t *လိပ်စာအလျား) {
    return 호출결과(jkoros_syscall(45, ဖိုင်အညွှန်း, (int)လိပ်စာ, (int)လိပ်စာအလျား, 0, 0));
}
int setsockopt(int ဖိုင်အညွှန်း, int အလွှာတန်ဖိုး, int သတ်မှတ်ချက်အမည်, const void *တန်ဖိုး, socklen_t တန်ဖိုးအလျား) {
    if (အလွှာတန်ဖိုး != SOL_SOCKET || သတ်မှတ်ချက်အမည် != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!တန်ဖိုး) { errno = EFAULT; return -1; }
    if (တန်ဖိုးအလျား != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *အချိန်တန်ဖိုး = တန်ဖိုး;
    if (အချိန်တန်ဖိုး->tv_sec < 0 || အချိန်တန်ဖိုး->tv_sec > 2 || အချိန်တန်ဖိုး->tv_usec < 0 || အချိန်တန်ဖိုး->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int မီလီစက္ကန့် = အချိန်တန်ဖိုး->tv_sec * 1000 + (အချိန်တန်ဖိုး->tv_usec + 999) / 1000;
    return 호출결과(jkoros_syscall(46, ဖိုင်အညွှန်း, မီလီစက္ကန့်, 0, 0, 0));
}
uint16_t htons(uint16_t တန်ဖိုး) { return (တန်ဖိုး << 8) | (တန်ဖိုး >> 8); }
uint16_t ntohs(uint16_t တန်ဖိုး) { return htons(တန်ဖိုး); }
uint32_t htonl(uint32_t တန်ဖိုး) {
    return (တန်ဖိုး << 24) | ((တန်ဖိုး << 8) & 0xff0000U) | ((တန်ဖိုး >> 8) & 0xff00U) | (တန်ဖိုး >> 24);
}
uint32_t ntohl(uint32_t တန်ဖိုး) { return htonl(တန်ဖိုး); }
int inet_pton(int လိပ်စာအစီအစဉ်, const char *အက္ခရာစဉ်, void *လိပ်စာ) {
    if (လိပ်စာအစီအစဉ် != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!အက္ခရာစဉ် || !လိပ်စာ) { errno = EFAULT; return -1; }
    unsigned char ယာယီတန်ဖိုး[4];
    for (int နေရာကွက်အချက် = 0; နေရာကွက်အချက် < 4; နေရာကွက်အချက်++) {
        int တန်ဖိုး = 0, ဂဏန်းများ = 0;
        const char *လုပ်ဆောင် = အက္ခရာစဉ်;
        while (*အက္ခရာစဉ် >= '0' && *အက္ခရာစဉ် <= '9') {
            if (++ဂဏန်းများ > 3) return 0;
            တန်ဖိုး = တန်ဖိုး * 10 + *အက္ခရာစဉ်++ - '0';
        }
        if (!ဂဏန်းများ || တန်ဖိုး > 255 || (ဂဏန်းများ > 1 && *လုပ်ဆောင် == '0')) return 0;
        ယာယီတန်ဖိုး[နေရာကွက်အချက်] = တန်ဖိုး;
        if (နေရာကွက်အချက် < 3) { if (*အက္ခရာစဉ်++ != '.') return 0; }
        else if (*အက္ခရာစဉ်) return 0;
    }
    for (int နေရာကွက်အချက် = 0; နေရာကွက်အချက် < 4; နေရာကွက်အချက်++) ((unsigned char *)လိပ်စာ)[နေရာကွက်အချက်] = ယာယီတန်ဖိုး[နေရာကွက်အချက်];
    return 1;
}
const char *inet_ntop(int လိပ်စာအစီအစဉ်, const void *လိပ်စာ, char *အက္ခရာစဉ်, socklen_t ဆံ့ပမာဏ) {
    if (လိပ်စာအစီအစဉ် != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!လိပ်စာ || !အက္ခရာစဉ်) { errno = EFAULT; return 0; }
    const unsigned char *ကိန်းတန်ဖိုး = လိပ်စာ;
    char ယာယီတန်ဖိုး[16]; unsigned int အလျား = 0;
    for (int နေရာကွက်အချက် = 0; နေရာကွက်အချက် < 4; နေရာကွက်အချက်++) {
        unsigned int တန်ဖိုး = ကိန်းတန်ဖိုး[နေရာကွက်အချက်];
        if (တန်ဖိုး >= 100) ယာယီတန်ဖိုး[အလျား++] = '0' + တန်ဖိုး / 100;
        if (တန်ဖိုး >= 10) ယာယီတန်ဖိုး[အလျား++] = '0' + တန်ဖိုး / 10 % 10;
        ယာယီတန်ဖိုး[အလျား++] = '0' + တန်ဖိုး % 10;
        if (နေရာကွက်အချက် < 3) ယာယီတန်ဖိုး[အလျား++] = '.';
    }
    ယာယီတန်ဖိုး[အလျား++] = 0;
    if (ဆံ့ပမာဏ < အလျား) { errno = ENOSPC; return 0; }
    for (unsigned int နေရာကွက်အချက် = 0; နေရာကွက်အချက် < အလျား; နေရာကွက်အချက်++) အက္ခရာစဉ်[နေရာကွက်အချက်] = ယာယီတန်ဖိုး[နေရာကွက်အချက်];
    return အက္ခရာစဉ်;
}

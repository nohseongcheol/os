#ifndef JKOROS_SOCKET_H
#define JKOROS_SOCKET_H
#include <sys/types.h>
typedef unsigned int socklen_t;
typedef unsigned short sa_family_t;
struct sockaddr { sa_family_t sa_family; char sa_data[14]; };
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define MSG_DONTWAIT 64
#define SOL_SOCKET 1
#define SO_RCVTIMEO 20
int socket(int လိပ်စာအစီအစဉ်, int ကွန်ရက်အမျိုးအစား, int သဘောတူစည်းမျဉ်းကိန်း);
int bind(int ဖိုင်အညွှန်း, const struct sockaddr *လိပ်စာ, socklen_t လိပ်စာအလျား);
ssize_t sendto(int ဖိုင်အညွှန်း, const void *ဒေတာ, size_t ဘိုက်အရေအတွက်, int သတ်မှတ်ချက်,
               const struct sockaddr *လိပ်စာ, socklen_t လိပ်စာအလျား);
ssize_t recvfrom(int ဖိုင်အညွှန်း, void *ဒေတာ, size_t ဘိုက်အရေအတွက်, int သတ်မှတ်ချက်,
                 struct sockaddr *လိပ်စာ, socklen_t *လိပ်စာအလျား);
int getsockname(int ဖိုင်အညွှန်း, struct sockaddr *လိပ်စာ, socklen_t *လိပ်စာအလျား);
int setsockopt(int ဖိုင်အညွှန်း, int အလွှာတန်ဖိုး, int သတ်မှတ်ချက်အမည်, const void *တန်ဖိုး, socklen_t တန်ဖိုးအလျား);
#endif

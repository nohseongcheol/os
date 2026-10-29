#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "파일규약.h"
/* 표준 ABI는 기존 စက်ဖိုင်ဖိုင်·ပြင်ပတန်ဖိုး 코드와 연결할 때만 사용한다. */
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
#define IPPROTO_TCP 6
#define INADDR_LOOPBACK 0x7f000001u
typedef uint32_t pk_socklen_t;
struct pk_sockaddr { uint16_t sa_family; unsigned char sa_data[14]; };
struct pk_in_addr { uint32_t s_addr; };
struct pk_sockaddr_in { uint16_t sin_family, sin_port; struct pk_in_addr sin_addr; unsigned char sin_zero[8]; };

/* မြန်မာ 자료형은 매크로 별칭이 아닌 독립된 구조체다.
 * လိပ်စာ(住所)는 도착할 곳, 갈래는 လိပ်စာ လည်ပတ်မှုစနစ်တန်ဖိုး, ဒေတာစာ(電文)은 နယ်နိမိတ်တန်ဖိုး 있는 ဆက်သွယ်မှု 자료다. */
enum ကွန်ရက်ကိန်းသေ {
    အင်တာနက်မျိုးစု = 2, စီးကြောင်းဆက်သွယ်မှု = 1, ဒေတာစာကွန်ရက်ပေါက် = 2,
    흐름전송규약 = 6, ဒေတာစာဆက်သွယ်စည်းမျဉ်း = 17,
    ပြန်လှည့်မှုလိပ်စာ = 0x7f000001u, အားလုံးချိတ်ဆက်မှုလိပ်စာများ = 0, 다시시도오류 = 11
};
typedef uint32_t ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ;
struct ကွန်ရက်ပေါက်လိပ်စာ { uint16_t လိပ်စာမျိုးစု; unsigned char လိပ်စာဒေတာ[14]; };
struct အင်တာနက်လိပ်စာတန်ဖိုး { uint32_t လိပ်စာတန်ဖိုး; };
struct အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာ {
    uint16_t လိပ်စာမျိုးစု;
    uint16_t ဆက်သွယ်ပေါက်ကိန်း;
    struct အင်တာနက်လိပ်စာတန်ဖိုး အင်တာနက်လိပ်စာ;
    unsigned char 여백[8];
};
typedef struct ကွန်ရက်ပေါက်လိပ်စာ ကွန်ရက်ပေါက်လိပ်စာအမျိုးပုံစံ;
typedef struct အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာ အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာအမျိုးပုံစံ;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာအရွယ်စစ်[(sizeof(struct အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာ)==16)?1:-1];
typedef char အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာနေရာချပုံစစ်[(offsetof(struct အင်တာနက်ကွန်ရက်ပေါက်လိပ်စာ,အင်တာနက်လိပ်စာ)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int အဆုံးမှတ်ဖန်တီး(int လိပ်စာမျိုးစု, int ဆက်သွယ်မှုနည်းစနစ်, int လွှဲပြောင်းဆက်သွယ်စည်းမျဉ်း);
int လိပ်စာချည်နှောင်(int ဆုံးမှတ်, const struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ, ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ အလျား);
intptr_t ဒေတာစာဒေတာပို့(int ဆုံးမှတ်, const void *ဒေတာ, size_t အရေအတွက်, int ရွေးချယ်မှုတန်ဖိုး, const struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ, ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ အလျား);
intptr_t ဒေတာစာဒေတာလက်ခံရယူ(int ဆုံးမှတ်, void *ဒေတာ, size_t အရေအတွက်, int ရွေးချယ်မှုတန်ဖိုး, struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ, ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ *အလျား);
int ကွန်ရက်ပေါက်လိပ်စာဖတ်(int ဆုံးမှတ်, struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ, ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ *အလျား);
int ကွန်ရက်ချိတ်ဆက်(int ဆုံးမှတ်, const struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ, ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ အလျား);
int 통신연결기다리기(int ဆုံးမှတ်, int စောင့်နေအရေအတွက်);
int ကွန်ရက်ချိတ်ဆက်မှုလက်ခံ(int ဆုံးမှတ်, struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ, ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ *အလျား);

int pk_connect(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
int pk_listen(int fd, int backlog);
int pk_accept(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_socket(int domain, int type, int protocol);
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
#ifdef __cplusplus
}
#endif
static inline uint16_t ကွန်ရက်တို(uint16_t တန်ဖိုး) { return (uint16_t)((တန်ဖိုး >> 8) | (တန်ဖိုး << 8)); }
static inline uint32_t ကွန်ရက်ကိန်းပြည့်(uint32_t တန်ဖိုး) { return ((တန်ဖိုး & 255u) << 24) | ((တန်ဖိုး & 0xff00u) << 8) | ((တန်ဖိုး >> 8) & 0xff00u) | (တန်ဖိုး >> 24); }
static inline uint16_t ကိရိယာအစဉ်တို(uint16_t တန်ဖိုး) { return ကွန်ရက်တို(တန်ဖိုး); }
static inline uint32_t ကိရိယာအစဉ်ကိန်းပြည့်(uint32_t တန်ဖိုး) { return ကွန်ရက်ကိန်းပြည့်(တန်ဖိုး); }
static inline uint16_t pk_htons(uint16_t x) { return ကွန်ရက်တို(x); }
static inline uint32_t pk_htonl(uint32_t x) { return ကွန်ရက်ကိန်းပြည့်(x); }
#endif

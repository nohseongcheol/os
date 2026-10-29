// 동일 မြန်မာ 헤더를 사용하는 별도 EL0 စာကြည့်တိုက်. အူတိုင်တန်ဖိုး 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "ခေါ်လုပ်.h"
#include "통신규약.h"
static int အမှားကုဒ်;
int *pk_errno_location(void) { return &အမှားကုဒ်; }
static intptr_t 결과검사(intptr_t ရလဒ်) { if (ရလဒ် < 0) { အမှားကုဒ် = -ရလဒ်; return -1; } return ရလဒ်; }
int pk_open(const char *path, int flags, ...) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ pk_read(int fd, void *p, size_t n) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ pk_write(int fd, const void *p, size_t n) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(4, fd, 0, 0, 0, 0, 0)); }
ဖိုင်အရွေ့အမျိုးပုံစံ pk_lseek(int fd, ဖိုင်အရွေ့အမျိုးပုံစံ offset, int origin) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ဖိုင်အရွေ့အမျိုးပုံစံ size) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 결과검사(သုံးစွဲသူခေါ်လုပ်(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 결과검사(သုံးစွဲသူခေါ်လုပ်(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 결과검사(သုံးစွဲသူခေါ်လုပ်(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* မြန်မာ 공개 함수의 တကယ့်ဒေတာ EL0 အကောင်အထည်ဖော်မှု. 구조체는 SVC에서 တန်ဖိုးမိတ္တူကူး·검증한다. */
int အဆုံးမှတ်ဖန်တီး(int လိပ်စာမျိုးစု,int ဆက်သွယ်မှုနည်းစနစ်,int လွှဲပြောင်းဆက်သွယ်စည်းမျဉ်း) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(32,လိပ်စာမျိုးစု,ဆက်သွယ်မှုနည်းစနစ်,လွှဲပြောင်းဆက်သွယ်စည်းမျဉ်း,0,0,0));
}
int လိပ်စာချည်နှောင်(int ဆုံးမှတ်,const struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ,ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ အလျား) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(33,ဆုံးမှတ်,(uintptr_t)လိပ်စာ,အလျား,0,0,0));
}
intptr_t ဒေတာစာဒေတာပို့(int ဆုံးမှတ်,const void *ဒေတာ,size_t အရေအတွက်,int ရွေးချယ်မှုတန်ဖိုး,const struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ,ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ အလျား) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(34,ဆုံးမှတ်,(uintptr_t)ဒေတာ,အရေအတွက်,ရွေးချယ်မှုတန်ဖိုး,(uintptr_t)လိပ်စာ,အလျား));
}
intptr_t ဒေတာစာဒေတာလက်ခံရယူ(int ဆုံးမှတ်,void *ဒေတာ,size_t အရေအတွက်,int ရွေးချယ်မှုတန်ဖိုး,struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ,ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ *အလျား) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(35,ဆုံးမှတ်,(uintptr_t)ဒေတာ,အရေအတွက်,ရွေးချယ်မှုတန်ဖိုး,(uintptr_t)လိပ်စာ,(uintptr_t)အလျား));
}
int ကွန်ရက်ပေါက်လိပ်စာဖတ်(int ဆုံးမှတ်,struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ,ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ *အလျား) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(36,ဆုံးမှတ်,(uintptr_t)လိပ်စာ,(uintptr_t)အလျား,0,0,0));
}
int ကွန်ရက်ချိတ်ဆက်(int ဆုံးမှတ်,const struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ,ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ အလျား) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(37,ဆုံးမှတ်,(uintptr_t)လိပ်စာ,အလျား,0,0,0));
}
int 통신연결기다리기(int ဆုံးမှတ်,int စောင့်နေအရေအတွက်) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(38,ဆုံးမှတ်,စောင့်နေအရေအတွက်,0,0,0,0));
}
int ကွန်ရက်ချိတ်ဆက်မှုလက်ခံ(int ဆုံးမှတ်,struct ကွန်ရက်ပေါက်လိပ်စာ *လိပ်စာ,ကွန်ရက်ပေါက်လိပ်စာအလျားအမျိုးပုံစံ *အလျား) {
    return 결과검사(သုံးစွဲသူခေါ်လုပ်(39,ဆုံးမှတ်,(uintptr_t)လိပ်စာ,(uintptr_t)အလျား,0,0,0));
}

/* ဖိုင် 함수도 독립된 မြန်မာ လုပ်ဆောင်ချက် 심볼로 제공한다. */
int ဖိုင်ဖွင့်(const char *လမ်း,int နည်းလမ်းနည်းစနစ်,...) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(3,(uintptr_t)လမ်း,နည်းလမ်းနည်းစနစ်,0,0,0,0)); }
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ ဖိုင်ဒေတာဖတ်(int ဖိုင်,void *ဒေတာ,size_t အရေအတွက်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(2,ဖိုင်,(uintptr_t)ဒေတာ,အရေအတွက်,0,0,0)); }
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ ဖိုင်ဒေတာရေး(int ဖိုင်,const void *ဒေတာ,size_t အရေအတွက်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(1,ဖိုင်,(uintptr_t)ဒေတာ,အရေအတွက်,0,0,0)); }
int ဖိုင်ပိတ်(int ဖိုင်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(4,ဖိုင်,0,0,0,0,0)); }
ဖိုင်အရွေ့အမျိုးပုံစံ ဖိုင်နေရာရွှေ့(int ဖိုင်,ဖိုင်အရွေ့အမျိုးပုံစံ အကွာအဝေး,int စီမံကိန်းအမြစ်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(5,ဖိုင်,အကွာအဝေး,စီမံကိန်းအမြစ်,0,0,0)); }
int ဖိုင်အချက်အမည်ဖယ်ရှား(const char *လမ်း) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(11,(uintptr_t)လမ်း,0,0,0,0,0)); }
int ဖိုင်အလျားသတ်မှတ်(int ဖိုင်,ဖိုင်အရွေ့အမျိုးပုံစံ အရွယ်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(10,ဖိုင်,အရွယ်,0,0,0,0)); }
int ဖိုင်သိုလှောင်အတည်ပြု(int ဖိုင်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(12,ဖိုင်,0,0,0,0,0)); }
int ဖိုင်အရွယ်(int ဖိုင်) { return 결과검사(သုံးစွဲသူခေါ်လုပ်(9,ဖိုင်,0,0,0,0,0)); }

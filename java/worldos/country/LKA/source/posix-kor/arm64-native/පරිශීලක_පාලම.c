// 동일 한국어 헤더를 사용하는 별도 EL0 ලේඛාගාරය. කර්නලය_අගය 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int දොස්_කේතය;
int *pk_errno_location(void) { return &දොස්_කේතය; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { දොස්_කේතය = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න pk_lseek(int fd, ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 결과검사(사용자호출(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 결과검사(사용자호출(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 결과검사(사용자호출(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 결과검사(사용자호출(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 결과검사(사용자호출(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 결과검사(사용자호출(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* 한국어 공개 함수의 තථ්_ය_දත්ත EL0 구현. 구조체는 SVC에서 ප්_රස්තාව_අගය·검증한다. */
int 통신종단점만들기(int යොමුව_පවුල,int 통신방식,int මාරුව_ප්_රොටොකෝලය) {
    return 결과검사(사용자호출(32,යොමුව_පවුල,통신방식,මාරුව_ප්_රොටොකෝලය,0,0,0));
}
int බඳින්න_යොමුව(int 종단,const struct 통신주소 *යොමුව,통신주소길이형 දිග_අගය) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)යොමුව,දිග_අගය,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *දත්ත,size_t 개수,int තේරීම_අගය,const struct 통신주소 *යොමුව,통신주소길이형 දිග_අගය) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)දත්ත,개수,තේරීම_අගය,(uintptr_t)යොමුව,දිග_අගය));
}
intptr_t 자료전문받기(int 종단,void *දත්ත,size_t 개수,int තේරීම_අගය,struct 통신주소 *යොමුව,통신주소길이형 *දිග_අගය) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)දත්ත,개수,තේරීම_අගය,(uintptr_t)යොමුව,(uintptr_t)දිග_අගය));
}
int 통신주소읽기(int 종단,struct 통신주소 *යොමුව,통신주소길이형 *දිග_අගය) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)යොමුව,(uintptr_t)දිග_අගය,0,0,0));
}
int සබඳින්න_ජාලය(int 종단,const struct 통신주소 *යොමුව,통신주소길이형 දිග_අගය) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)යොමුව,දිග_අගය,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int පිළිගන්න_ජාල_සම්බන්ධතාව(int 종단,struct 통신주소 *යොමුව,통신주소길이형 *දිග_අගය) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)යොමුව,(uintptr_t)දිග_අගය,0,0,0));
}

/* ගොනු 함수도 독립된 한국어 ශ්_රිතය_අගය 심볼로 제공한다. */
int සාදන්න_ගොනුව(const char *මාර්_ගය,int ක්_රමය_ප්_රකාරය,...) { return 결과검사(사용자호출(3,(uintptr_t)මාර්_ගය,ක්_රමය_ප්_රකාරය,0,0,0,0)); }
입출력결과형 파일자료읽기(int ගොනු,void *දත්ත,size_t 개수) { return 결과검사(사용자호출(2,ගොනු,(uintptr_t)දත්ත,개수,0,0,0)); }
입출력결과형 ලියන්න_ගොනුව_දත්ත(int ගොනු,const void *දත්ත,size_t 개수) { return 결과검사(사용자호출(1,ගොනු,(uintptr_t)දත්ත,개수,0,0,0)); }
int වසන්න_ගොනුව(int ගොනු) { return 결과검사(사용자호출(4,ගොනු,0,0,0,0,0)); }
ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න සොයන්න_ගොනුව(int ගොනු,ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න 거리,int 기준) { return 결과검사(사용자호출(5,ගොනු,거리,기준,0,0,0)); }
int ඉවත්_කරන්න_ගොනුව_පිවිසුම_නම(const char *මාර්_ගය) { return 결과검사(사용자호출(11,(uintptr_t)මාර්_ගය,0,0,0,0,0)); }
int කට්ටලය_ගොනුව_දිග(int ගොනු,ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න ප්_රමාණය) { return 결과검사(사용자호출(10,ගොනු,ප්_රමාණය,0,0,0,0)); }
int 파일저장확정(int ගොනු) { return 결과검사(사용자호출(12,ගොනු,0,0,0,0,0)); }
int ගොනුව_ප්_රමාණනය(int ගොනු) { return 결과검사(사용자호출(9,ගොනු,0,0,0,0,0)); }

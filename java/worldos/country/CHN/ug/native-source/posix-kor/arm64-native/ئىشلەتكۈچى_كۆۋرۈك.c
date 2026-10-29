// 동일 한국어 헤더를 사용하는 별도 EL0 ئامبار. يادرو_قىممىتى 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int 오류값;
int *pk_errno_location(void) { return &오류값; }
static intptr_t 결과검사(intptr_t ئۆلچەم) { if (ئۆلچەم < 0) { 오류값 = -ئۆلچەم; return -1; } return ئۆلچەم; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ھۆججەت_ئاغما_تىپ pk_lseek(int fd, ھۆججەت_ئاغما_تىپ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ھۆججەت_ئاغما_تىپ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ھەقىقىي_مەلۇمات EL0 구현. 구조체는 SVC에서 مىسال_قىممىتى·검증한다. */
int 통신종단점만들기(int ئادرېس_ئائىلە,int 통신방식,int يوللاش_كېلىشىم) {
    return 결과검사(사용자호출(32,ئادرېس_ئائىلە,통신방식,يوللاش_كېلىشىم,0,0,0));
}
int باغلاش_ئادرېس(int 종단,const struct 통신주소 *ئادرېس,통신주소길이형 ئۇزۇنلۇق_قىممىتى) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ئادرېس,ئۇزۇنلۇق_قىممىتى,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *مەلۇمات,size_t 개수,int تاللاش_قىممىتى,const struct 통신주소 *ئادرېس,통신주소길이형 ئۇزۇنلۇق_قىممىتى) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)مەلۇمات,개수,تاللاش_قىممىتى,(uintptr_t)ئادرېس,ئۇزۇنلۇق_قىممىتى));
}
intptr_t 자료전문받기(int 종단,void *مەلۇمات,size_t 개수,int تاللاش_قىممىتى,struct 통신주소 *ئادرېس,통신주소길이형 *ئۇزۇنلۇق_قىممىتى) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)مەلۇمات,개수,تاللاش_قىممىتى,(uintptr_t)ئادرېس,(uintptr_t)ئۇزۇنلۇق_قىممىتى));
}
int 통신주소읽기(int 종단,struct 통신주소 *ئادرېس,통신주소길이형 *ئۇزۇنلۇق_قىممىتى) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ئادرېس,(uintptr_t)ئۇزۇنلۇق_قىممىتى,0,0,0));
}
int ئۇلاش_تور(int 종단,const struct 통신주소 *ئادرېس,통신주소길이형 ئۇزۇنلۇق_قىممىتى) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ئادرېس,ئۇزۇنلۇق_قىممىتى,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int قوبۇللاش_تور_ئۇلىنىشى(int 종단,struct 통신주소 *ئادرېس,통신주소길이형 *ئۇزۇنلۇق_قىممىتى) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ئادرېس,(uintptr_t)ئۇزۇنلۇق_قىممىتى,0,0,0));
}

/* ھۆججەت 함수도 독립된 한국어 فۇنكسىيە_قىممىتى 심볼로 제공한다. */
int قۇرۇش_ھۆججەت(const char *يول,int ئۇسۇل_ھالەت,...) { return 결과검사(사용자호출(3,(uintptr_t)يول,ئۇسۇل_ھالەت,0,0,0,0)); }
입출력결과형 파일자료읽기(int ھۆججەت,void *مەلۇمات,size_t 개수) { return 결과검사(사용자호출(2,ھۆججەت,(uintptr_t)مەلۇمات,개수,0,0,0)); }
입출력결과형 يازماق_ھۆججەت_مەلۇمات(int ھۆججەت,const void *مەلۇمات,size_t 개수) { return 결과검사(사용자호출(1,ھۆججەت,(uintptr_t)مەلۇمات,개수,0,0,0)); }
int ئاياغ_ھۆججەت(int ھۆججەت) { return 결과검사(사용자호출(4,ھۆججەت,0,0,0,0,0)); }
ھۆججەت_ئاغما_تىپ ئىزدەش_ھۆججەت(int ھۆججەت,ھۆججەت_ئاغما_تىپ 거리,int كۆرسىتىش_يىلتىز) { return 결과검사(사용자호출(5,ھۆججەت,거리,كۆرسىتىش_يىلتىز,0,0,0)); }
int چىقىرىۋەتمەك_ھۆججەت_كىرگۈزۈش_نامى(const char *يول) { return 결과검사(사용자호출(11,(uintptr_t)يول,0,0,0,0,0)); }
int توپ_ھۆججەت_ئۇزۇنلۇق(int ھۆججەت,ھۆججەت_ئاغما_تىپ چوڭلۇقى) { return 결과검사(사용자호출(10,ھۆججەت,چوڭلۇقى,0,0,0,0)); }
int 파일저장확정(int ھۆججەت) { return 결과검사(사용자호출(12,ھۆججەت,0,0,0,0,0)); }
int ھۆججەت_ئۆزگەرتمەك(int ھۆججەت) { return 결과검사(사용자호출(9,ھۆججەت,0,0,0,0,0)); }

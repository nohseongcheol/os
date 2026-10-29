// 동일 Македонски 헤더를 사용하는 별도 EL0 библиотека. јадро_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int идентификатор_на_грешката;
int *pk_errno_location(void) { return &идентификатор_на_грешката; }
static intptr_t 결과검사(intptr_t мерка) { if (мерка < 0) { идентификатор_на_грешката = -мерка; return -1; } return мерка; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
датотека_OFFSET_TYPE pk_lseek(int fd, датотека_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, датотека_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Македонски 공개 함수의 реален_податоци EL0 구현. 구조체는 SVC에서 копирај_VALUE·검증한다. */
int 통신종단점만들기(int адреса_семејни,int 통신방식,int пренос_протокол) {
    return 결과검사(사용자호출(32,адреса_семејни,통신방식,пренос_протокол,0,0,0));
}
int БИНД_адреса(int 종단,const struct 통신주소 *адреса,통신주소길이형 должина_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)адреса,должина_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *податоци,size_t ставка_COUNT,int селекција_VALUE,const struct 통신주소 *адреса,통신주소길이형 должина_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)податоци,ставка_COUNT,селекција_VALUE,(uintptr_t)адреса,должина_VALUE));
}
intptr_t 자료전문받기(int 종단,void *податоци,size_t ставка_COUNT,int селекција_VALUE,struct 통신주소 *адреса,통신주소길이형 *должина_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)податоци,ставка_COUNT,селекција_VALUE,(uintptr_t)адреса,(uintptr_t)должина_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *адреса,통신주소길이형 *должина_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)адреса,(uintptr_t)должина_VALUE,0,0,0));
}
int ПОВРЗИ_Мрежа(int 종단,const struct 통신주소 *адреса,통신주소길이형 должина_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)адреса,должина_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Чекам_COUNT) {
    return 결과검사(사용자호출(38,종단,Чекам_COUNT,0,0,0,0));
}
int прифати_мрежна_врска(int 종단,struct 통신주소 *адреса,통신주소길이형 *должина_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)адреса,(uintptr_t)должина_VALUE,0,0,0));
}

/* Датотека 함수도 독립된 Македонски ФУНКЦИЈА_VALUE 심볼로 제공한다. */
int отвори_датотека(const char *ПАТЕКА,int метод_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)ПАТЕКА,метод_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Датотека,void *податоци,size_t ставка_COUNT) { return 결과검사(사용자호출(2,Датотека,(uintptr_t)податоци,ставка_COUNT,0,0,0)); }
입출력결과형 запиши_датотека_податоци(int Датотека,const void *податоци,size_t ставка_COUNT) { return 결과검사(사용자호출(1,Датотека,(uintptr_t)податоци,ставка_COUNT,0,0,0)); }
int затвори_датотека(int Датотека) { return 결과검사(사용자호출(4,Датотека,0,0,0,0,0)); }
датотека_OFFSET_TYPE пребарај_датотека(int Датотека,датотека_OFFSET_TYPE 거리,int Project_корен) { return 결과검사(사용자호출(5,Датотека,거리,Project_корен,0,0,0)); }
int отстрани_датотека_внес_име(const char *ПАТЕКА) { return 결과검사(사용자호출(11,(uintptr_t)ПАТЕКА,0,0,0,0,0)); }
int збир_датотека_должина(int Датотека,датотека_OFFSET_TYPE Големина) { return 결과검사(사용자호출(10,Датотека,Големина,0,0,0,0)); }
int 파일저장확정(int Датотека) { return 결과검사(사용자호출(12,Датотека,0,0,0,0,0)); }
int датотека_големина(int Датотека) { return 결과검사(사용자호출(9,Датотека,0,0,0,0,0)); }

// 동일 한국어 헤더를 사용하는 별도 EL0 библиотека. језгро_вриједност 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int кôд_грешке;
int *pk_errno_location(void) { return &кôд_грешке; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { кôд_грешке = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
파일위치형 pk_lseek(int fd, 파일위치형 offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, 파일위치형 size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 стваран_подаци EL0 구현. 구조체는 SVC에서 инстанца_вриједност·검증한다. */
int 통신종단점만들기(int адреса_породица,int 통신방식,int пријенос_протокол) {
    return 결과검사(사용자호출(32,адреса_породица,통신방식,пријенос_протокол,0,0,0));
}
int повезати_адреса(int крајња_тачка,const struct 통신주소 *адреса,통신주소길이형 дужина_вриједност) {
    return 결과검사(사용자호출(33,крајња_тачка,(uintptr_t)адреса,дужина_вриједност,0,0,0));
}
intptr_t 자료전문보내기(int крајња_тачка,const void *подаци,size_t 개수,int избор_вриједност,const struct 통신주소 *адреса,통신주소길이형 дужина_вриједност) {
    return 결과검사(사용자호출(34,крајња_тачка,(uintptr_t)подаци,개수,избор_вриједност,(uintptr_t)адреса,дужина_вриједност));
}
intptr_t 자료전문받기(int крајња_тачка,void *подаци,size_t 개수,int избор_вриједност,struct 통신주소 *адреса,통신주소길이형 *дужина_вриједност) {
    return 결과검사(사용자호출(35,крајња_тачка,(uintptr_t)подаци,개수,избор_вриједност,(uintptr_t)адреса,(uintptr_t)дужина_вриједност));
}
int 통신주소읽기(int крајња_тачка,struct 통신주소 *адреса,통신주소길이형 *дужина_вриједност) {
    return 결과검사(사용자호출(36,крајња_тачка,(uintptr_t)адреса,(uintptr_t)дужина_вриједност,0,0,0));
}
int повезати_Мрежа(int крајња_тачка,const struct 통신주소 *адреса,통신주소길이형 дужина_вриједност) {
    return 결과검사(사용자호출(37,крајња_тачка,(uintptr_t)адреса,дужина_вриједност,0,0,0));
}
int 통신연결기다리기(int крајња_тачка,int 대기수) {
    return 결과검사(사용자호출(38,крајња_тачка,대기수,0,0,0,0));
}
int 통신연결받기(int крајња_тачка,struct 통신주소 *адреса,통신주소길이형 *дужина_вриједност) {
    return 결과검사(사용자호출(39,крајња_тачка,(uintptr_t)адреса,(uintptr_t)дужина_вриједност,0,0,0));
}

/* фајл 함수도 독립된 한국어 функција_вриједност 심볼로 제공한다. */
int отворити_фајл(const char *пут,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)пут,방식,0,0,0,0)); }
입출력결과형 파일자료읽기(int фајл,void *подаци,size_t 개수) { return 결과검사(사용자호출(2,фајл,(uintptr_t)подаци,개수,0,0,0)); }
입출력결과형 писати_фајл_подаци(int фајл,const void *подаци,size_t 개수) { return 결과검사(사용자호출(1,фајл,(uintptr_t)подаци,개수,0,0,0)); }
int затворити_фајл(int фајл) { return 결과검사(사용자호출(4,фајл,0,0,0,0,0)); }
파일위치형 претражити_фајл(int фајл,파일위치형 거리,int 기준) { return 결과검사(사용자호출(5,фајл,거리,기준,0,0,0)); }
int уклонити_фајл_унос_назив(const char *пут) { return 결과검사(사용자호출(11,(uintptr_t)пут,0,0,0,0,0)); }
int именовани_скуп_фајл_дужина(int фајл,파일위치형 подесити_величину) { return 결과검사(사용자호출(10,фајл,подесити_величину,0,0,0,0)); }
int 파일저장확정(int фајл) { return 결과검사(사용자호출(12,фајл,0,0,0,0,0)); }
int фајл_подесити_величину(int фајл) { return 결과검사(사용자호출(9,фајл,0,0,0,0,0)); }

// 동일 한국어 헤더를 사용하는 별도 EL0 کتابتون. نوغی_ارزښت 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int تېروت_کوډ;
int *pk_errno_location(void) { return &تېروت_کوډ; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { تېروت_کوډ = -결과; return -1; } return 결과; }
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

/* 한국어 공개 함수의 실제 EL0 구현. 구조체는 SVC에서 بېلګه_ارزښت_37b3d3b1·검증한다. */
int 통신종단점만들기(int 주소갈래,int 통신방식,int لېږدول_باندره) {
    return 결과검사(사용자호출(32,주소갈래,통신방식,لېږدول_باندره,0,0,0));
}
int اړه_لري_پته(int 종단,const struct 통신주소 *پته,통신주소길이형 اوږدوالى_ارزښت) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)پته,اوږدوالى_ارزښت,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *اومتوک,size_t 개수,int 선택,const struct 통신주소 *پته,통신주소길이형 اوږدوالى_ارزښت) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)اومتوک,개수,선택,(uintptr_t)پته,اوږدوالى_ارزښت));
}
intptr_t 자료전문받기(int 종단,void *اومتوک,size_t 개수,int 선택,struct 통신주소 *پته,통신주소길이형 *اوږدوالى_ارزښت) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)اومتوک,개수,선택,(uintptr_t)پته,(uintptr_t)اوږدوالى_ارزښت));
}
int 통신주소읽기(int 종단,struct 통신주소 *پته,통신주소길이형 *اوږدوالى_ارزښت) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)پته,(uintptr_t)اوږدوالى_ارزښت,0,0,0));
}
int پيوستول_جال(int 종단,const struct 통신주소 *پته,통신주소길이형 اوږدوالى_ارزښت) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)پته,اوږدوالى_ارزښت,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int 통신연결받기(int 종단,struct 통신주소 *پته,통신주소길이형 *اوږدوالى_ارزښت) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)پته,(uintptr_t)اوږدوالى_ارزښت,0,0,0));
}

/* دوتنه 함수도 독립된 한국어 함수 심볼로 제공한다. */
int 파일열기(const char *يونلور,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)يونلور,방식,0,0,0,0)); }
입출력결과형 파일자료읽기(int دوتنه,void *اومتوک,size_t 개수) { return 결과검사(사용자호출(2,دوتنه,(uintptr_t)اومتوک,개수,0,0,0)); }
입출력결과형 ليکل_دوتنه_اومتوک(int دوتنه,const void *اومتوک,size_t 개수) { return 결과검사(사용자호출(1,دوتنه,(uintptr_t)اومتوک,개수,0,0,0)); }
int بندول_دوتنه(int دوتنه) { return 결과검사(사용자호출(4,دوتنه,0,0,0,0,0)); }
파일위치형 파일위치옮기기(int دوتنه,파일위치형 거리,int 기준) { return 결과검사(사용자호출(5,دوتنه,거리,기준,0,0,0)); }
int 파일이름지우기(const char *يونلور) { return 결과검사(사용자호출(11,(uintptr_t)يونلور,0,0,0,0,0)); }
int 파일길이정하기(int دوتنه,파일위치형 کچ) { return 결과검사(사용자호출(10,دوتنه,کچ,0,0,0,0)); }
int 파일저장확정(int دوتنه) { return 결과검사(사용자호출(12,دوتنه,0,0,0,0,0)); }
int 파일크기(int دوتنه) { return 결과검사(사용자호출(9,دوتنه,0,0,0,0,0)); }

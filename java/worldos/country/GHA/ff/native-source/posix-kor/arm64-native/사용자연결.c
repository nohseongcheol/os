// 동일 한국어 헤더를 사용하는 별도 EL0 defterdu. aaluude_njaru 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int 오류값;
int *pk_errno_location(void) { return &오류값; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { 오류값 = -결과; return -1; } return 결과; }
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

/* 한국어 공개 함수의 laatii_keɓe EL0 구현. 구조체는 SVC에서 waanjitaade_njaru·검증한다. */
int 통신종단점만들기(int 주소갈래,int 통신방식,int egginde_porotokol) {
    return 결과검사(사용자호출(32,주소갈래,통신방식,egginde_porotokol,0,0,0));
}
int seŋondir_ñiiɓirde(int 종단,const struct 통신주소 *ñiiɓirde,통신주소길이형 njuuteendi_njaru) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ñiiɓirde,njuuteendi_njaru,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *keɓe,size_t 개수,int cuɓal_njaru,const struct 통신주소 *ñiiɓirde,통신주소길이형 njuuteendi_njaru) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)keɓe,개수,cuɓal_njaru,(uintptr_t)ñiiɓirde,njuuteendi_njaru));
}
intptr_t 자료전문받기(int 종단,void *keɓe,size_t 개수,int cuɓal_njaru,struct 통신주소 *ñiiɓirde,통신주소길이형 *njuuteendi_njaru) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)keɓe,개수,cuɓal_njaru,(uintptr_t)ñiiɓirde,(uintptr_t)njuuteendi_njaru));
}
int 통신주소읽기(int 종단,struct 통신주소 *ñiiɓirde,통신주소길이형 *njuuteendi_njaru) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ñiiɓirde,(uintptr_t)njuuteendi_njaru,0,0,0));
}
int seŋaade_laylaytol(int 종단,const struct 통신주소 *ñiiɓirde,통신주소길이형 njuuteendi_njaru) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ñiiɓirde,njuuteendi_njaru,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int 통신연결받기(int 종단,struct 통신주소 *ñiiɓirde,통신주소길이형 *njuuteendi_njaru) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ñiiɓirde,(uintptr_t)njuuteendi_njaru,0,0,0));
}

/* fiilde 함수도 독립된 한국어 juɓɓol_njaru 심볼로 제공한다. */
int udditde_fiilde(const char *laawol,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)laawol,방식,0,0,0,0)); }
입출력결과형 파일자료읽기(int fiilde,void *keɓe,size_t 개수) { return 결과검사(사용자호출(2,fiilde,(uintptr_t)keɓe,개수,0,0,0)); }
입출력결과형 winndude_fiilde_keɓe(int fiilde,const void *keɓe,size_t 개수) { return 결과검사(사용자호출(1,fiilde,(uintptr_t)keɓe,개수,0,0,0)); }
int uddude_fiilde(int fiilde) { return 결과검사(사용자호출(4,fiilde,0,0,0,0,0)); }
파일위치형 파일위치옮기기(int fiilde,파일위치형 거리,int 기준) { return 결과검사(사용자호출(5,fiilde,거리,기준,0,0,0)); }
int ittude_fiilde_naatnugol_innde(const char *laawol) { return 결과검사(사용자호출(11,(uintptr_t)laawol,0,0,0,0,0)); }
int 파일길이정하기(int fiilde,파일위치형 waylude_etannde) { return 결과검사(사용자호출(10,fiilde,waylude_etannde,0,0,0,0)); }
int 파일저장확정(int fiilde) { return 결과검사(사용자호출(12,fiilde,0,0,0,0,0)); }
int fiilde_waylude_etannde(int fiilde) { return 결과검사(사용자호출(9,fiilde,0,0,0,0,0)); }

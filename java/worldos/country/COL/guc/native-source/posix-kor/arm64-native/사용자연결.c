// 동일 한국어 헤더를 사용하는 별도 EL0 anaajaalee. keetnerü_ajutuu 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int anüliaa_mojukua_ipatsü;
int *pk_errno_location(void) { return &anüliaa_mojukua_ipatsü; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { anüliaa_mojukua_ipatsü = -결과; return -1; } return 결과; }
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

/* 한국어 공개 함수의 실제 EL0 구현. 구조체는 SVC에서 ashataa_ajutuu·검증한다. */
int 통신종단점만들기(int 주소갈래,int 통신방식,int alate_eraa_pürotokoola) {
    return 결과검사(사용자호출(32,주소갈래,통신방식,alate_eraa_pürotokoola,0,0,0));
}
int alaasajaa_ejepüsee(int 종단,const struct 통신주소 *ejepüsee,통신주소길이형 akaliaa_ajutuu) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ejepüsee,akaliaa_ajutuu,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *atijaaya,size_t 개수,int 선택,const struct 통신주소 *ejepüsee,통신주소길이형 akaliaa_ajutuu) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)atijaaya,개수,선택,(uintptr_t)ejepüsee,akaliaa_ajutuu));
}
intptr_t 자료전문받기(int 종단,void *atijaaya,size_t 개수,int 선택,struct 통신주소 *ejepüsee,통신주소길이형 *akaliaa_ajutuu) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)atijaaya,개수,선택,(uintptr_t)ejepüsee,(uintptr_t)akaliaa_ajutuu));
}
int 통신주소읽기(int 종단,struct 통신주소 *ejepüsee,통신주소길이형 *akaliaa_ajutuu) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ejepüsee,(uintptr_t)akaliaa_ajutuu,0,0,0));
}
int a_ataa_kusu(int 종단,const struct 통신주소 *ejepüsee,통신주소길이형 akaliaa_ajutuu) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ejepüsee,akaliaa_ajutuu,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int 통신연결받기(int 종단,struct 통신주소 *ejepüsee,통신주소길이형 *akaliaa_ajutuu) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ejepüsee,(uintptr_t)akaliaa_ajutuu,0,0,0));
}

/* anaajaalaa 함수도 독립된 한국어 함수 심볼로 제공한다. */
int 파일열기(const char *wopu_a_ttaaleemüin,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)wopu_a_ttaaleemüin,방식,0,0,0,0)); }
입출력결과형 파일자료읽기(int anaajaalaa,void *atijaaya,size_t 개수) { return 결과검사(사용자호출(2,anaajaalaa,(uintptr_t)atijaaya,개수,0,0,0)); }
입출력결과형 ashajaa_anaajaalaa_atijaaya(int anaajaalaa,const void *atijaaya,size_t 개수) { return 결과검사(사용자호출(1,anaajaalaa,(uintptr_t)atijaaya,개수,0,0,0)); }
int asürülaa_anaajaalaa(int anaajaalaa) { return 결과검사(사용자호출(4,anaajaalaa,0,0,0,0,0)); }
파일위치형 파일위치옮기기(int anaajaalaa,파일위치형 거리,int 기준) { return 결과검사(사용자호출(5,anaajaalaa,거리,기준,0,0,0)); }
int 파일이름지우기(const char *wopu_a_ttaaleemüin) { return 결과검사(사용자호출(11,(uintptr_t)wopu_a_ttaaleemüin,0,0,0,0,0)); }
int 파일길이정하기(int anaajaalaa,파일위치형 크기) { return 결과검사(사용자호출(10,anaajaalaa,크기,0,0,0,0)); }
int 파일저장확정(int anaajaalaa) { return 결과검사(사용자호출(12,anaajaalaa,0,0,0,0,0)); }
int 파일크기(int anaajaalaa) { return 결과검사(사용자호출(9,anaajaalaa,0,0,0,0,0)); }

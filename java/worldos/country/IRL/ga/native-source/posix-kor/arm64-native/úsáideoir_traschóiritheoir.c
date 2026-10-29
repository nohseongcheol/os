// 동일 Gaeilge 헤더를 사용하는 별도 EL0 leabharlann. eithne_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int cód_earráide;
int *pk_errno_location(void) { return &cód_earráide; }
static intptr_t 결과검사(intptr_t tomhas) { if (tomhas < 0) { cód_earráide = -tomhas; return -1; } return tomhas; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
comhad_OFFSET_TYPE pk_lseek(int fd, comhad_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, comhad_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Gaeilge 공개 함수의 iarbhír_sonraí EL0 구현. 구조체는 SVC에서 ásc_VALUE·검증한다. */
int 통신종단점만들기(int ADDRESS_Teaghlach,int 통신방식,int traschur_prótacal) {
    return 결과검사(사용자호출(32,ADDRESS_Teaghlach,통신방식,traschur_prótacal,0,0,0));
}
int BIND_ADDRESS(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 fad_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ADDRESS,fad_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *sonraí,size_t mír_COUNT,int roghnú_VALUE,const struct 통신주소 *ADDRESS,통신주소길이형 fad_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)sonraí,mír_COUNT,roghnú_VALUE,(uintptr_t)ADDRESS,fad_VALUE));
}
intptr_t 자료전문받기(int 종단,void *sonraí,size_t mír_COUNT,int roghnú_VALUE,struct 통신주소 *ADDRESS,통신주소길이형 *fad_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)sonraí,mír_COUNT,roghnú_VALUE,(uintptr_t)ADDRESS,(uintptr_t)fad_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *fad_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ADDRESS,(uintptr_t)fad_VALUE,0,0,0));
}
int nasc_Líonra(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 fad_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ADDRESS,fad_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int glac_le_nasc_líonra(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *fad_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ADDRESS,(uintptr_t)fad_VALUE,0,0,0));
}

/* Comhad 함수도 독립된 Gaeilge feidhm_VALUE 심볼로 제공한다. */
int oscail_comhad(const char *CONAIR,int modh_mód,...) { return 결과검사(사용자호출(3,(uintptr_t)CONAIR,modh_mód,0,0,0,0)); }
입출력결과형 파일자료읽기(int Comhad,void *sonraí,size_t mír_COUNT) { return 결과검사(사용자호출(2,Comhad,(uintptr_t)sonraí,mír_COUNT,0,0,0)); }
입출력결과형 scríobh_comhad_sonraí(int Comhad,const void *sonraí,size_t mír_COUNT) { return 결과검사(사용자호출(1,Comhad,(uintptr_t)sonraí,mír_COUNT,0,0,0)); }
int dún_comhad(int Comhad) { return 결과검사(사용자호출(4,Comhad,0,0,0,0,0)); }
comhad_OFFSET_TYPE lorg_comhad(int Comhad,comhad_OFFSET_TYPE 거리,int teilgean_fréamh) { return 결과검사(사용자호출(5,Comhad,거리,teilgean_fréamh,0,0,0)); }
int bain_comhad_iontráil_ainm(const char *CONAIR) { return 결과검사(사용자호출(11,(uintptr_t)CONAIR,0,0,0,0,0)); }
int tacar_comhad_fad(int Comhad,comhad_OFFSET_TYPE Méid) { return 결과검사(사용자호출(10,Comhad,Méid,0,0,0,0)); }
int 파일저장확정(int Comhad) { return 결과검사(사용자호출(12,Comhad,0,0,0,0,0)); }
int comhad_socraigh_méid(int Comhad) { return 결과검사(사용자호출(9,Comhad,0,0,0,0,0)); }

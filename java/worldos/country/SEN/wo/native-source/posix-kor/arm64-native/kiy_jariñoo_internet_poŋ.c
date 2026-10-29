// 동일 한국어 헤더를 사용하는 별도 EL0 daaray_téere. xoox_xëyma 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int pasu_njumte;
int *pk_errno_location(void) { return &pasu_njumte; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { pasu_njumte = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
bara_denc_Randal_xeet pk_lseek(int fd, bara_denc_Randal_xeet offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, bara_denc_Randal_xeet size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 liteew_mbir EL0 구현. 구조체는 SVC에서 mbokk_xëyma·검증한다. */
int 통신종단점만들기(int dëkkuwaay_Njaboot,int 통신방식,int toxal_protocol) {
    return 결과검사(사용자호출(32,dëkkuwaay_Njaboot,통신방식,toxal_protocol,0,0,0));
}
int BIND_dëkkuwaay(int 종단,const struct 통신주소 *dëkkuwaay,통신주소길이형 diir_xëyma) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)dëkkuwaay,diir_xëyma,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *mbir,size_t 개수,int tanneef_xëyma,const struct 통신주소 *dëkkuwaay,통신주소길이형 diir_xëyma) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)mbir,개수,tanneef_xëyma,(uintptr_t)dëkkuwaay,diir_xëyma));
}
intptr_t 자료전문받기(int 종단,void *mbir,size_t 개수,int tanneef_xëyma,struct 통신주소 *dëkkuwaay,통신주소길이형 *diir_xëyma) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)mbir,개수,tanneef_xëyma,(uintptr_t)dëkkuwaay,(uintptr_t)diir_xëyma));
}
int 통신주소읽기(int 종단,struct 통신주소 *dëkkuwaay,통신주소길이형 *diir_xëyma) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)dëkkuwaay,(uintptr_t)diir_xëyma,0,0,0));
}
int JOKKOO_mbaal(int 종단,const struct 통신주소 *dëkkuwaay,통신주소길이형 diir_xëyma) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)dëkkuwaay,diir_xëyma,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int nangu_Lonkug_Mbaal(int 종단,struct 통신주소 *dëkkuwaay,통신주소길이형 *diir_xëyma) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)dëkkuwaay,(uintptr_t)diir_xëyma,0,0,0));
}

/* bara_denc 함수도 독립된 한국어 liëey_xëyma 심볼로 제공한다. */
int sos_bara_denc(const char *Yoonu_jëmale,int doxalin_anam,...) { return 결과검사(사용자호출(3,(uintptr_t)Yoonu_jëmale,doxalin_anam,0,0,0,0)); }
입출력결과형 파일자료읽기(int bara_denc,void *mbir,size_t 개수) { return 결과검사(사용자호출(2,bara_denc,(uintptr_t)mbir,개수,0,0,0)); }
입출력결과형 biir_bara_denc_mbir(int bara_denc,const void *mbir,size_t 개수) { return 결과검사(사용자호출(1,bara_denc,(uintptr_t)mbir,개수,0,0,0)); }
int Tej_bara_denc(int bara_denc) { return 결과검사(사용자호출(4,bara_denc,0,0,0,0,0)); }
bara_denc_Randal_xeet seet_bara_denc(int bara_denc,bara_denc_Randal_xeet 거리,int 기준) { return 결과검사(사용자호출(5,bara_denc,거리,기준,0,0,0)); }
int dandal_bara_denc_dugal_xabaar_tur(const char *Yoonu_jëmale) { return 결과검사(사용자호출(11,(uintptr_t)Yoonu_jëmale,0,0,0,0,0)); }
int Boole_gi_bara_denc_diir(int bara_denc,bara_denc_Randal_xeet tolluwaay) { return 결과검사(사용자호출(10,bara_denc,tolluwaay,0,0,0,0)); }
int 파일저장확정(int bara_denc) { return 결과검사(사용자호출(12,bara_denc,0,0,0,0,0)); }
int bara_denc_tolluwaay(int bara_denc) { return 결과검사(사용자호출(9,bara_denc,0,0,0,0,0)); }

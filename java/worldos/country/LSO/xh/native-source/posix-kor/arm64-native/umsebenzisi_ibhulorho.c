// 동일 isiXhosa 헤더를 사용하는 별도 EL0 ilayibhrari. ikheneli_ixabiso 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ikhowudi_yengxaki_engalungisekanga;
int *pk_errno_location(void) { return &ikhowudi_yengxaki_engalungisekanga; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { ikhowudi_yengxaki_engalungisekanga = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ifayile_Ukulinganisa_uhlobo pk_lseek(int fd, ifayile_Ukulinganisa_uhlobo offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ifayile_Ukulinganisa_uhlobo size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* isiXhosa 공개 함수의 eyona_yenzekileyo_iingcombolo EL0 구현. 구조체는 SVC에서 kopa_ixabiso·검증한다. */
int 통신종단점만들기(int idilesi_Usapho,int 통신방식,int gqithisela_iprothokhol) {
    return 결과검사(사용자호출(32,idilesi_Usapho,통신방식,gqithisela_iprothokhol,0,0,0));
}
int BOPHELELA_idilesi(int 종단,const struct 통신주소 *idilesi,통신주소길이형 ubude_ixabiso) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)idilesi,ubude_ixabiso,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *iingcombolo,size_t 개수,int ukukhetha_ixabiso,const struct 통신주소 *idilesi,통신주소길이형 ubude_ixabiso) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)iingcombolo,개수,ukukhetha_ixabiso,(uintptr_t)idilesi,ubude_ixabiso));
}
intptr_t 자료전문받기(int 종단,void *iingcombolo,size_t 개수,int ukukhetha_ixabiso,struct 통신주소 *idilesi,통신주소길이형 *ubude_ixabiso) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)iingcombolo,개수,ukukhetha_ixabiso,(uintptr_t)idilesi,(uintptr_t)ubude_ixabiso));
}
int 통신주소읽기(int 종단,struct 통신주소 *idilesi,통신주소길이형 *ubude_ixabiso) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)idilesi,(uintptr_t)ubude_ixabiso,0,0,0));
}
int I_Connect_Inethiwekhi(int 종단,const struct 통신주소 *idilesi,통신주소길이형 ubude_ixabiso) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)idilesi,ubude_ixabiso,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int yamkela_uqhagamshelo_lwenethiwekhi(int 종단,struct 통신주소 *idilesi,통신주소길이형 *ubude_ixabiso) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)idilesi,(uintptr_t)ubude_ixabiso,0,0,0));
}

/* iFayili 함수도 독립된 isiXhosa INKQUBO_ixabiso 심볼로 제공한다. */
int vula_ifayile(const char *INDLELA,int imethodi_imo,...) { return 결과검사(사용자호출(3,(uintptr_t)INDLELA,imethodi_imo,0,0,0,0)); }
입출력결과형 파일자료읽기(int iFayili,void *iingcombolo,size_t 개수) { return 결과검사(사용자호출(2,iFayili,(uintptr_t)iingcombolo,개수,0,0,0)); }
입출력결과형 bhala_ifayile_iingcombolo(int iFayili,const void *iingcombolo,size_t 개수) { return 결과검사(사용자호출(1,iFayili,(uintptr_t)iingcombolo,개수,0,0,0)); }
int vala_ifayile(int iFayili) { return 결과검사(사용자호출(4,iFayili,0,0,0,0,0)); }
ifayile_Ukulinganisa_uhlobo khangela_ifayile(int iFayili,ifayile_Ukulinganisa_uhlobo 거리,int 기준) { return 결과검사(사용자호출(5,iFayili,거리,기준,0,0,0)); }
int shenxisa_ifayile_ufako_nkcukacha_igama(const char *INDLELA) { return 결과검사(사용자호출(11,(uintptr_t)INDLELA,0,0,0,0,0)); }
int isethi_ifayile_ubude(int iFayili,ifayile_Ukulinganisa_uhlobo Ubukhulu) { return 결과검사(사용자호출(10,iFayili,Ubukhulu,0,0,0,0)); }
int 파일저장확정(int iFayili) { return 결과검사(사용자호출(12,iFayili,0,0,0,0,0)); }
int ifayile_isayizi(int iFayili) { return 결과검사(사용자호출(9,iFayili,0,0,0,0,0)); }

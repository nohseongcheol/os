// 동일 Cymraeg 헤더를 사용하는 별도 EL0 llyfrgell. cnewyllyn_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int cod_gwall;
int *pk_errno_location(void) { return &cod_gwall; }
static intptr_t 결과검사(intptr_t mesur) { if (mesur < 0) { cod_gwall = -mesur; return -1; } return mesur; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ffeil_OFFSET_TYPE pk_lseek(int fd, ffeil_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ffeil_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Cymraeg 공개 함수의 go_iawn_data EL0 구현. 구조체는 SVC에서 copïo_VALUE·검증한다. */
int 통신종단점만들기(int ADDRESS_Teulu,int 통신방식,int trosglwyddo_protocol) {
    return 결과검사(사용자호출(32,ADDRESS_Teulu,통신방식,trosglwyddo_protocol,0,0,0));
}
int BIND_ADDRESS(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 hyd_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ADDRESS,hyd_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *data,size_t eitem_COUNT,int dewisiad_VALUE,const struct 통신주소 *ADDRESS,통신주소길이형 hyd_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)data,eitem_COUNT,dewisiad_VALUE,(uintptr_t)ADDRESS,hyd_VALUE));
}
intptr_t 자료전문받기(int 종단,void *data,size_t eitem_COUNT,int dewisiad_VALUE,struct 통신주소 *ADDRESS,통신주소길이형 *hyd_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)data,eitem_COUNT,dewisiad_VALUE,(uintptr_t)ADDRESS,(uintptr_t)hyd_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *hyd_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ADDRESS,(uintptr_t)hyd_VALUE,0,0,0));
}
int Cysylltu_Rhwydwaith(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 hyd_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ADDRESS,hyd_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Wrthi_n_aros_COUNT) {
    return 결과검사(사용자호출(38,종단,Wrthi_n_aros_COUNT,0,0,0,0));
}
int derbyn_cysylltiad_rhwydwaith(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *hyd_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ADDRESS,(uintptr_t)hyd_VALUE,0,0,0));
}

/* Ffeil 함수도 독립된 Cymraeg SWYDDOGAETH_VALUE 심볼로 제공한다. */
int agor_ffeil(const char *LLWYBR,int dull_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)LLWYBR,dull_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Ffeil,void *data,size_t eitem_COUNT) { return 결과검사(사용자호출(2,Ffeil,(uintptr_t)data,eitem_COUNT,0,0,0)); }
입출력결과형 ysgrifennu_ffeil_data(int Ffeil,const void *data,size_t eitem_COUNT) { return 결과검사(사용자호출(1,Ffeil,(uintptr_t)data,eitem_COUNT,0,0,0)); }
int cau_ffeil(int Ffeil) { return 결과검사(사용자호출(4,Ffeil,0,0,0,0,0)); }
ffeil_OFFSET_TYPE chwilio_ffeil(int Ffeil,ffeil_OFFSET_TYPE 거리,int prosiect_gwraidd) { return 결과검사(사용자호출(5,Ffeil,거리,prosiect_gwraidd,0,0,0)); }
int tynnu_ffeil_cofnod_enw(const char *LLWYBR) { return 결과검사(사용자호출(11,(uintptr_t)LLWYBR,0,0,0,0,0)); }
int set_ffeil_hyd(int Ffeil,ffeil_OFFSET_TYPE Maint) { return 결과검사(사용자호출(10,Ffeil,Maint,0,0,0,0)); }
int 파일저장확정(int Ffeil) { return 결과검사(사용자호출(12,Ffeil,0,0,0,0,0)); }
int ffeil_newid_maint(int Ffeil) { return 결과검사(사용자호출(9,Ffeil,0,0,0,0,0)); }

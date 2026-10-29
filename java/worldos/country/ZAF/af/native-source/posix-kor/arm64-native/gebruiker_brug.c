// 동일 한국어 헤더를 사용하는 별도 EL0 biblioteek. kern_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int foutkode;
int *pk_errno_location(void) { return &foutkode; }
static intptr_t 결과검사(intptr_t maatreël) { if (maatreël < 0) { foutkode = -maatreël; return -1; } return maatreël; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
lêer_OFFSET_TYPE pk_lseek(int fd, lêer_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, lêer_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 werklik_data EL0 구현. 구조체는 SVC에서 geval_VALUE·검증한다. */
int 통신종단점만들기(int adres_Gesin,int 통신방식,int oordra_protokol) {
    return 결과검사(사용자호출(32,adres_Gesin,통신방식,oordra_protokol,0,0,0));
}
int BIND_adres(int 종단,const struct 통신주소 *adres,통신주소길이형 lengte_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)adres,lengte_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *data,size_t item_COUNT,int seleksie_VALUE,const struct 통신주소 *adres,통신주소길이형 lengte_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)data,item_COUNT,seleksie_VALUE,(uintptr_t)adres,lengte_VALUE));
}
intptr_t 자료전문받기(int 종단,void *data,size_t item_COUNT,int seleksie_VALUE,struct 통신주소 *adres,통신주소길이형 *lengte_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)data,item_COUNT,seleksie_VALUE,(uintptr_t)adres,(uintptr_t)lengte_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *adres,통신주소길이형 *lengte_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)adres,(uintptr_t)lengte_VALUE,0,0,0));
}
int KOPPEL_Netwerk(int 종단,const struct 통신주소 *adres,통신주소길이형 lengte_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)adres,lengte_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Besig_om_te_wag_COUNT) {
    return 결과검사(사용자호출(38,종단,Besig_om_te_wag_COUNT,0,0,0,0));
}
int aanvaar_netwerkverbinding(int 종단,struct 통신주소 *adres,통신주소길이형 *lengte_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)adres,(uintptr_t)lengte_VALUE,0,0,0));
}

/* Lêer 함수도 독립된 한국어 funksie_VALUE 심볼로 제공한다. */
int skep_lêer(const char *Pad,int metode_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)Pad,metode_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Lêer,void *data,size_t item_COUNT) { return 결과검사(사용자호출(2,Lêer,(uintptr_t)data,item_COUNT,0,0,0)); }
입출력결과형 skryf_lêer_data(int Lêer,const void *data,size_t item_COUNT) { return 결과검사(사용자호출(1,Lêer,(uintptr_t)data,item_COUNT,0,0,0)); }
int sluit_lêer(int Lêer) { return 결과검사(사용자호출(4,Lêer,0,0,0,0,0)); }
lêer_OFFSET_TYPE soek_lêer(int Lêer,lêer_OFFSET_TYPE 거리,int Project_wortel) { return 결과검사(사용자호출(5,Lêer,거리,Project_wortel,0,0,0)); }
int verwyder_lêer_inskrywing_naam(const char *Pad) { return 결과검사(사용자호출(11,(uintptr_t)Pad,0,0,0,0,0)); }
int stel_lêer_lengte(int Lêer,lêer_OFFSET_TYPE Grootte) { return 결과검사(사용자호출(10,Lêer,Grootte,0,0,0,0)); }
int 파일저장확정(int Lêer) { return 결과검사(사용자호출(12,Lêer,0,0,0,0,0)); }
int lêer_verstel(int Lêer) { return 결과검사(사용자호출(9,Lêer,0,0,0,0,0)); }

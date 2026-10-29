// 동일 Malti 헤더를 사용하는 별도 EL0 librerija. kernel_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kodiċi_tal_iżball;
int *pk_errno_location(void) { return &kodiċi_tal_iżball; }
static intptr_t 결과검사(intptr_t miżura) { if (miżura < 0) { kodiċi_tal_iżball = -miżura; return -1; } return miżura; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fajl_OFFSET_TYPE pk_lseek(int fd, fajl_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fajl_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Malti 공개 함수의 attwali_data EL0 구현. 구조체는 SVC에서 kkopja_VALUE·검증한다. */
int 통신종단점만들기(int ADDRESS_Familja,int 통신방식,int trasferiment_protokoll) {
    return 결과검사(사용자호출(32,ADDRESS_Familja,통신방식,trasferiment_protokoll,0,0,0));
}
int BIND_ADDRESS(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 tul_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ADDRESS,tul_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *data,size_t element_COUNT,int għażla_VALUE,const struct 통신주소 *ADDRESS,통신주소길이형 tul_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)data,element_COUNT,għażla_VALUE,(uintptr_t)ADDRESS,tul_VALUE));
}
intptr_t 자료전문받기(int 종단,void *data,size_t element_COUNT,int għażla_VALUE,struct 통신주소 *ADDRESS,통신주소길이형 *tul_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)data,element_COUNT,għażla_VALUE,(uintptr_t)ADDRESS,(uintptr_t)tul_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *tul_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ADDRESS,(uintptr_t)tul_VALUE,0,0,0));
}
int AQBAD_netwerk(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 tul_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ADDRESS,tul_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int aċċetta_kumnikazzjoni_tan_netwerk(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *tul_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ADDRESS,(uintptr_t)tul_VALUE,0,0,0));
}

/* fajl 함수도 독립된 Malti FUNCTION_VALUE 심볼로 제공한다. */
int fetaħ_fajl(const char *mogħdija,int metodu_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)mogħdija,metodu_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int fajl,void *data,size_t element_COUNT) { return 결과검사(사용자호출(2,fajl,(uintptr_t)data,element_COUNT,0,0,0)); }
입출력결과형 kiteb_fajl_data(int fajl,const void *data,size_t element_COUNT) { return 결과검사(사용자호출(1,fajl,(uintptr_t)data,element_COUNT,0,0,0)); }
int agħlaq_fajl(int fajl) { return 결과검사(사용자호출(4,fajl,0,0,0,0,0)); }
fajl_OFFSET_TYPE fittex_fajl(int fajl,fajl_OFFSET_TYPE 거리,int pprojetta_għerq) { return 결과검사(사용자호출(5,fajl,거리,pprojetta_għerq,0,0,0)); }
int neħħa_fajl_entrata_isem(const char *mogħdija) { return 결과검사(사용자호출(11,(uintptr_t)mogħdija,0,0,0,0,0)); }
int sett_fajl_tul(int fajl,fajl_OFFSET_TYPE daqqas) { return 결과검사(사용자호출(10,fajl,daqqas,0,0,0,0)); }
int 파일저장확정(int fajl) { return 결과검사(사용자호출(12,fajl,0,0,0,0,0)); }
int fajl_daqqas(int fajl) { return 결과검사(사용자호출(9,fajl,0,0,0,0,0)); }

// 동일 한국어 헤더를 사용하는 별도 EL0 bibliotekë. bërthamë_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kodi_i_gabimit;
int *pk_errno_location(void) { return &kodi_i_gabimit; }
static intptr_t 결과검사(intptr_t llogaritje) { if (llogaritje < 0) { kodi_i_gabimit = -llogaritje; return -1; } return llogaritje; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
skedar_OFFSET_TYPE pk_lseek(int fd, skedar_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, skedar_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 aktual_të_dhëna EL0 구현. 구조체는 SVC에서 kopjoj_VALUE·검증한다. */
int 통신종단점만들기(int email_Familja,int 통신방식,int transferim_protokoll) {
    return 결과검사(사용자호출(32,email_Familja,통신방식,transferim_protokoll,0,0,0));
}
int BIND_email(int 종단,const struct 통신주소 *email,통신주소길이형 gjatësi_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)email,gjatësi_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *të_dhëna,size_t njësi_COUNT,int përzgjedhje_VALUE,const struct 통신주소 *email,통신주소길이형 gjatësi_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)të_dhëna,njësi_COUNT,përzgjedhje_VALUE,(uintptr_t)email,gjatësi_VALUE));
}
intptr_t 자료전문받기(int 종단,void *të_dhëna,size_t njësi_COUNT,int përzgjedhje_VALUE,struct 통신주소 *email,통신주소길이형 *gjatësi_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)të_dhëna,njësi_COUNT,përzgjedhje_VALUE,(uintptr_t)email,(uintptr_t)gjatësi_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *email,통신주소길이형 *gjatësi_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)email,(uintptr_t)gjatësi_VALUE,0,0,0));
}
int Lidh_rrjet(int 종단,const struct 통신주소 *email,통신주소길이형 gjatësi_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)email,gjatësi_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Po_pres_COUNT) {
    return 결과검사(사용자호출(38,종단,Po_pres_COUNT,0,0,0,0));
}
int prano_lidhje_e_rrjetit(int 종단,struct 통신주소 *email,통신주소길이형 *gjatësi_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)email,(uintptr_t)gjatësi_VALUE,0,0,0));
}

/* Kartelë 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int hap_skedar(const char *POZICIONI,int metoda_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)POZICIONI,metoda_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Kartelë,void *të_dhëna,size_t njësi_COUNT) { return 결과검사(사용자호출(2,Kartelë,(uintptr_t)të_dhëna,njësi_COUNT,0,0,0)); }
입출력결과형 shkruaj_skedar_të_dhëna(int Kartelë,const void *të_dhëna,size_t njësi_COUNT) { return 결과검사(사용자호출(1,Kartelë,(uintptr_t)të_dhëna,njësi_COUNT,0,0,0)); }
int mbyll_skedar(int Kartelë) { return 결과검사(사용자호출(4,Kartelë,0,0,0,0,0)); }
skedar_OFFSET_TYPE kërko_skedar(int Kartelë,skedar_OFFSET_TYPE 거리,int Project_rrënjë) { return 결과검사(사용자호출(5,Kartelë,거리,Project_rrënjë,0,0,0)); }
int heq_skedar_futje_emër(const char *POZICIONI) { return 결과검사(사용자호출(11,(uintptr_t)POZICIONI,0,0,0,0,0)); }
int bashkësi_skedar_gjatësi(int Kartelë,skedar_OFFSET_TYPE Madhësi) { return 결과검사(사용자호출(10,Kartelë,Madhësi,0,0,0,0)); }
int 파일저장확정(int Kartelë) { return 결과검사(사용자호출(12,Kartelë,0,0,0,0,0)); }
int skedar_ndryshoj_përmasat(int Kartelë) { return 결과검사(사용자호출(9,Kartelë,0,0,0,0,0)); }

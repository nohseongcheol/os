// 동일 Reo_Māori 헤더를 사용하는 별도 EL0 puna. kākano_uara_0611a8a8 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int waehere_hapa;
int *pk_errno_location(void) { return &waehere_hapa; }
static intptr_t 결과검사(intptr_t mēhua) { if (mēhua < 0) { waehere_hapa = -mēhua; return -1; } return mēhua; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
kōnae_OFFSET_TYPE pk_lseek(int fd, kōnae_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, kōnae_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Reo_Māori 공개 함수의 tūturu_raraunga EL0 구현. 구조체는 SVC에서 tārua_uara·검증한다. */
int 통신종단점만들기(int ADDRESS_Whānau,int 통신방식,int whakawhiti_kawa) {
    return 결과검사(사용자호출(32,ADDRESS_Whānau,통신방식,whakawhiti_kawa,0,0,0));
}
int BIND_ADDRESS(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 roa_uara) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ADDRESS,roa_uara,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *raraunga,size_t tuemi_COUNT,int tīpakonga_uara,const struct 통신주소 *ADDRESS,통신주소길이형 roa_uara) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)raraunga,tuemi_COUNT,tīpakonga_uara,(uintptr_t)ADDRESS,roa_uara));
}
intptr_t 자료전문받기(int 종단,void *raraunga,size_t tuemi_COUNT,int tīpakonga_uara,struct 통신주소 *ADDRESS,통신주소길이형 *roa_uara) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)raraunga,tuemi_COUNT,tīpakonga_uara,(uintptr_t)ADDRESS,(uintptr_t)roa_uara));
}
int 통신주소읽기(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *roa_uara) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ADDRESS,(uintptr_t)roa_uara,0,0,0));
}
int TŪHONO_whatunga(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 roa_uara) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ADDRESS,roa_uara,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int whakaae_tūhononga_whatunga(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *roa_uara) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ADDRESS,(uintptr_t)roa_uara,0,0,0));
}

/* Kōnae 함수도 독립된 Reo_Māori TAUMAHI_uara 심볼로 제공한다. */
int tiwhikete_kōnae(const char *ara,int aratuka_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)ara,aratuka_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Kōnae,void *raraunga,size_t tuemi_COUNT) { return 결과검사(사용자호출(2,Kōnae,(uintptr_t)raraunga,tuemi_COUNT,0,0,0)); }
입출력결과형 tuhi_kōnae_raraunga(int Kōnae,const void *raraunga,size_t tuemi_COUNT) { return 결과검사(사용자호출(1,Kōnae,(uintptr_t)raraunga,tuemi_COUNT,0,0,0)); }
int kati_kōnae(int Kōnae) { return 결과검사(사용자호출(4,Kōnae,0,0,0,0,0)); }
kōnae_OFFSET_TYPE kimi_kōnae(int Kōnae,kōnae_OFFSET_TYPE 거리,int whakaatu_pūtake) { return 결과검사(사용자호출(5,Kōnae,거리,whakaatu_pūtake,0,0,0)); }
int tango_kōnae_tāurunga_ingoa(const char *ara) { return 결과검사(사용자호출(11,(uintptr_t)ara,0,0,0,0,0)); }
int huinga_kōnae_roa(int Kōnae,kōnae_OFFSET_TYPE rahi) { return 결과검사(사용자호출(10,Kōnae,rahi,0,0,0,0)); }
int 파일저장확정(int Kōnae) { return 결과검사(사용자호출(12,Kōnae,0,0,0,0,0)); }
int kōnae_rahi(int Kōnae) { return 결과검사(사용자호출(9,Kōnae,0,0,0,0,0)); }

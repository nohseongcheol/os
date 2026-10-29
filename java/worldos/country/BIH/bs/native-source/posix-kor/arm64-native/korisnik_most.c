// 동일 한국어 헤더를 사용하는 별도 EL0 biblioteka. jezgro_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kôd_greške;
int *pk_errno_location(void) { return &kôd_greške; }
static intptr_t 결과검사(intptr_t mjera) { if (mjera < 0) { kôd_greške = -mjera; return -1; } return mjera; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fajl_Pomak_TYPE pk_lseek(int fd, fajl_Pomak_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fajl_Pomak_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 stvaran_podaci EL0 구현. 구조체는 SVC에서 instanca_VALUE·검증한다. */
int Create_završna_tačka(int adresa_Porodica,int 통신방식,int prijenos_protokol) {
    return 결과검사(사용자호출(32,adresa_Porodica,통신방식,prijenos_protokol,0,0,0));
}
int BIND_adresa(int završna_tačka,const struct 통신주소 *adresa,통신주소길이형 dužina_VALUE) {
    return 결과검사(사용자호출(33,završna_tačka,(uintptr_t)adresa,dužina_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int završna_tačka,const void *podaci,size_t stavka_COUNT,int izbor_VALUE,const struct 통신주소 *adresa,통신주소길이형 dužina_VALUE) {
    return 결과검사(사용자호출(34,završna_tačka,(uintptr_t)podaci,stavka_COUNT,izbor_VALUE,(uintptr_t)adresa,dužina_VALUE));
}
intptr_t 자료전문받기(int završna_tačka,void *podaci,size_t stavka_COUNT,int izbor_VALUE,struct 통신주소 *adresa,통신주소길이형 *dužina_VALUE) {
    return 결과검사(사용자호출(35,završna_tačka,(uintptr_t)podaci,stavka_COUNT,izbor_VALUE,(uintptr_t)adresa,(uintptr_t)dužina_VALUE));
}
int 통신주소읽기(int završna_tačka,struct 통신주소 *adresa,통신주소길이형 *dužina_VALUE) {
    return 결과검사(사용자호출(36,završna_tačka,(uintptr_t)adresa,(uintptr_t)dužina_VALUE,0,0,0));
}
int povezati_Mreža(int završna_tačka,const struct 통신주소 *adresa,통신주소길이형 dužina_VALUE) {
    return 결과검사(사용자호출(37,završna_tačka,(uintptr_t)adresa,dužina_VALUE,0,0,0));
}
int 통신연결기다리기(int završna_tačka,int Čekanje_COUNT) {
    return 결과검사(사용자호출(38,završna_tačka,Čekanje_COUNT,0,0,0,0));
}
int prihvatiti_mrežna_veza(int završna_tačka,struct 통신주소 *adresa,통신주소길이형 *dužina_VALUE) {
    return 결과검사(사용자호출(39,završna_tačka,(uintptr_t)adresa,(uintptr_t)dužina_VALUE,0,0,0));
}

/* Fajl 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int kreirati_fajl(const char *Putanja,int metoda_mod,...) { return 결과검사(사용자호출(3,(uintptr_t)Putanja,metoda_mod,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fajl,void *podaci,size_t stavka_COUNT) { return 결과검사(사용자호출(2,Fajl,(uintptr_t)podaci,stavka_COUNT,0,0,0)); }
입출력결과형 pisati_fajl_podaci(int Fajl,const void *podaci,size_t stavka_COUNT) { return 결과검사(사용자호출(1,Fajl,(uintptr_t)podaci,stavka_COUNT,0,0,0)); }
int zatvoriti_fajl(int Fajl) { return 결과검사(사용자호출(4,Fajl,0,0,0,0,0)); }
fajl_Pomak_TYPE tražiti_fajl(int Fajl,fajl_Pomak_TYPE 거리,int projicirati_koijen) { return 결과검사(사용자호출(5,Fajl,거리,projicirati_koijen,0,0,0)); }
int ukloniti_fajl_unos_naziv(const char *Putanja) { return 결과검사(사용자호출(11,(uintptr_t)Putanja,0,0,0,0,0)); }
int skup_fajl_dužina(int Fajl,fajl_Pomak_TYPE Veličina) { return 결과검사(사용자호출(10,Fajl,Veličina,0,0,0,0)); }
int 파일저장확정(int Fajl) { return 결과검사(사용자호출(12,Fajl,0,0,0,0,0)); }
int fajl_podesiti_veličinu(int Fajl) { return 결과검사(사용자호출(9,Fajl,0,0,0,0,0)); }

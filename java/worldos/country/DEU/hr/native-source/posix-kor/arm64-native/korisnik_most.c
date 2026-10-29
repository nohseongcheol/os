// 동일 hrvatski 헤더를 사용하는 별도 EL0 biblioteka. jezgra_sustava_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kôd_pogreške;
int *pk_errno_location(void) { return &kôd_pogreške; }
static intptr_t 결과검사(intptr_t REZULTAT) { if (REZULTAT < 0) { kôd_pogreške = -REZULTAT; return -1; } return REZULTAT; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Datoteka_pomak_TYPE pk_lseek(int fd, Datoteka_pomak_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Datoteka_pomak_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* hrvatski 공개 함수의 stvaran_podaci EL0 구현. 구조체는 SVC에서 instanca_VALUE·검증한다. */
int Create_sudionik(int adresa_linija,int 통신방식,int Prijenos_protokol) {
    return 결과검사(사용자호출(32,adresa_linija,통신방식,Prijenos_protokol,0,0,0));
}
int BIND_adresa(int sudionik,const struct 통신주소 *adresa,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,sudionik,(uintptr_t)adresa,길이,0,0,0));
}
intptr_t slati_datogram_podaci(int sudionik,const void *podaci,size_t artikl_COUNT,int odabir_VALUE,const struct 통신주소 *adresa,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,sudionik,(uintptr_t)podaci,artikl_COUNT,odabir_VALUE,(uintptr_t)adresa,길이));
}
intptr_t primiti_datogram_podaci(int sudionik,void *podaci,size_t artikl_COUNT,int odabir_VALUE,struct 통신주소 *adresa,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,sudionik,(uintptr_t)podaci,artikl_COUNT,odabir_VALUE,(uintptr_t)adresa,(uintptr_t)길이));
}
int 통신주소읽기(int sudionik,struct 통신주소 *adresa,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,sudionik,(uintptr_t)adresa,(uintptr_t)길이,0,0,0));
}
int CONNECT_mreža(int sudionik,const struct 통신주소 *adresa,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,sudionik,(uintptr_t)adresa,길이,0,0,0));
}
int 통신연결기다리기(int sudionik,int Čekanje_COUNT) {
    return 결과검사(사용자호출(38,sudionik,Čekanje_COUNT,0,0,0,0));
}
int prihvatiti_mrežna_veza(int sudionik,struct 통신주소 *adresa,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,sudionik,(uintptr_t)adresa,(uintptr_t)길이,0,0,0));
}

/* Datoteka 함수도 독립된 hrvatski FUNCTION_VALUE 심볼로 제공한다. */
int otvoreno_Datoteka(const char *PUTANJA,int postupak_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)PUTANJA,postupak_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Datoteka,void *podaci,size_t artikl_COUNT) { return 결과검사(사용자호출(2,Datoteka,(uintptr_t)podaci,artikl_COUNT,0,0,0)); }
입출력결과형 zapisivanje_Datoteka_podaci(int Datoteka,const void *podaci,size_t artikl_COUNT) { return 결과검사(사용자호출(1,Datoteka,(uintptr_t)podaci,artikl_COUNT,0,0,0)); }
int Zatvori_Datoteka(int Datoteka) { return 결과검사(사용자호출(4,Datoteka,0,0,0,0,0)); }
Datoteka_pomak_TYPE tražiti_Datoteka(int Datoteka,Datoteka_pomak_TYPE 거리,int akcija_korijen) { return 결과검사(사용자호출(5,Datoteka,거리,akcija_korijen,0,0,0)); }
int ukloniti_Datoteka_unos_naziv(const char *PUTANJA) { return 결과검사(사용자호출(11,(uintptr_t)PUTANJA,0,0,0,0,0)); }
int 파일길이정하기(int Datoteka,Datoteka_pomak_TYPE Veličina) { return 결과검사(사용자호출(10,Datoteka,Veličina,0,0,0,0)); }
int izvršavanje_pohrana_datoteka(int Datoteka) { return 결과검사(사용자호출(12,Datoteka,0,0,0,0,0)); }
int veličina_datoteke(int Datoteka) { return 결과검사(사용자호출(9,Datoteka,0,0,0,0,0)); }

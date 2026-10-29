// 동일 slovenščina 헤더를 사용하는 별도 EL0 knjižnica. jedro_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int koda_napake;
int *pk_errno_location(void) { return &koda_napake; }
static intptr_t 결과검사(intptr_t REZULTAT) { if (REZULTAT < 0) { koda_napake = -REZULTAT; return -1; } return REZULTAT; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Datoteka_odmik_Tip pk_lseek(int fd, Datoteka_odmik_Tip offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Datoteka_odmik_Tip size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* slovenščina 공개 함수의 dejanski_podatki EL0 구현. 구조체는 SVC에서 kopirati_VALUE·검증한다. */
int Ustvari_končna_točka(int naslov_Družina,int 통신방식,int Prenos_protokol) {
    return 결과검사(사용자호출(32,naslov_Družina,통신방식,Prenos_protokol,0,0,0));
}
int BIND_naslov(int končna_točka,const struct vtičnica_naslov *naslov,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,končna_točka,(uintptr_t)naslov,길이,0,0,0));
}
intptr_t poslati_datagram_podatki(int končna_točka,const void *podatki,size_t element_COUNT,int izbor_VALUE,const struct vtičnica_naslov *naslov,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,končna_točka,(uintptr_t)podatki,element_COUNT,izbor_VALUE,(uintptr_t)naslov,길이));
}
intptr_t sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(int končna_točka,void *podatki,size_t element_COUNT,int izbor_VALUE,struct vtičnica_naslov *naslov,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,končna_točka,(uintptr_t)podatki,element_COUNT,izbor_VALUE,(uintptr_t)naslov,(uintptr_t)길이));
}
int 통신주소읽기(int končna_točka,struct vtičnica_naslov *naslov,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,končna_točka,(uintptr_t)naslov,(uintptr_t)길이,0,0,0));
}
int POVEŽI_mreža(int končna_točka,const struct vtičnica_naslov *naslov,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,končna_točka,(uintptr_t)naslov,길이,0,0,0));
}
int 통신연결기다리기(int končna_točka,int Čakanje_COUNT) {
    return 결과검사(사용자호출(38,končna_točka,Čakanje_COUNT,0,0,0,0));
}
int sprejeti_omrežna_povezava(int končna_točka,struct vtičnica_naslov *naslov,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,končna_točka,(uintptr_t)naslov,(uintptr_t)길이,0,0,0));
}

/* Datoteka 함수도 독립된 slovenščina FUNCTION_VALUE 심볼로 제공한다. */
int odprto_Datoteka(const char *POT,int metoda_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)POT,metoda_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Datoteka,void *podatki,size_t element_COUNT) { return 결과검사(사용자호출(2,Datoteka,(uintptr_t)podatki,element_COUNT,0,0,0)); }
입출력결과형 pisati_Datoteka_podatki(int Datoteka,const void *podatki,size_t element_COUNT) { return 결과검사(사용자호출(1,Datoteka,(uintptr_t)podatki,element_COUNT,0,0,0)); }
int Zapri_Datoteka(int Datoteka) { return 결과검사(사용자호출(4,Datoteka,0,0,0,0,0)); }
Datoteka_odmik_Tip iskati_Datoteka(int Datoteka,Datoteka_odmik_Tip 거리,int pobuda_koren) { return 결과검사(사용자호출(5,Datoteka,거리,pobuda_koren,0,0,0)); }
int odstraniti_Datoteka_vnos_ime(const char *POT) { return 결과검사(사용자호출(11,(uintptr_t)POT,0,0,0,0,0)); }
int 파일길이정하기(int Datoteka,Datoteka_odmik_Tip Velikost) { return 결과검사(사용자호출(10,Datoteka,Velikost,0,0,0,0)); }
int potrjevanje_datotečna_shramba(int Datoteka) { return 결과검사(사용자호출(12,Datoteka,0,0,0,0,0)); }
int velikost_datoteke(int Datoteka) { return 결과검사(사용자호출(9,Datoteka,0,0,0,0,0)); }

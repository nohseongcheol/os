// 동일 Slovenský 헤더를 사용하는 별도 EL0 knižnica. jadro_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kód_chyby;
int *pk_errno_location(void) { return &kód_chyby; }
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) { kód_chyby = -KR; return -1; } return KR; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Súbor_Posun_Typ pk_lseek(int fd, Súbor_Posun_Typ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Súbor_Posun_Typ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Slovenský 공개 함수의 skutočný_údaje EL0 구현. 구조체는 SVC에서 inštancia_VALUE·검증한다. */
int Create_účastník(int adresa_séria,int 통신방식,int prenos_protokol) {
    return 결과검사(사용자호출(32,adresa_séria,통신방식,prenos_protokol,0,0,0));
}
int BIND_adresa(int účastník,const struct soket_adresa *adresa,soket_adresa_dĺžka_Typ dĺžka_VALUE) {
    return 결과검사(사용자호출(33,účastník,(uintptr_t)adresa,dĺžka_VALUE,0,0,0));
}
intptr_t odoslať_datagram_údaje(int účastník,const void *údaje,size_t položka_COUNT,int výber_VALUE,const struct soket_adresa *adresa,soket_adresa_dĺžka_Typ dĺžka_VALUE) {
    return 결과검사(사용자호출(34,účastník,(uintptr_t)údaje,položka_COUNT,výber_VALUE,(uintptr_t)adresa,dĺžka_VALUE));
}
intptr_t dostať_datagram_údaje(int účastník,void *údaje,size_t položka_COUNT,int výber_VALUE,struct soket_adresa *adresa,soket_adresa_dĺžka_Typ *dĺžka_VALUE) {
    return 결과검사(사용자호출(35,účastník,(uintptr_t)údaje,položka_COUNT,výber_VALUE,(uintptr_t)adresa,(uintptr_t)dĺžka_VALUE));
}
int 통신주소읽기(int účastník,struct soket_adresa *adresa,soket_adresa_dĺžka_Typ *dĺžka_VALUE) {
    return 결과검사(사용자호출(36,účastník,(uintptr_t)adresa,(uintptr_t)dĺžka_VALUE,0,0,0));
}
int spojiť_sieť(int účastník,const struct soket_adresa *adresa,soket_adresa_dĺžka_Typ dĺžka_VALUE) {
    return 결과검사(사용자호출(37,účastník,(uintptr_t)adresa,dĺžka_VALUE,0,0,0));
}
int 통신연결기다리기(int účastník,int Čakám_COUNT) {
    return 결과검사(사용자호출(38,účastník,Čakám_COUNT,0,0,0,0));
}
int prijať_sieťové_pripojenie(int účastník,struct soket_adresa *adresa,soket_adresa_dĺžka_Typ *dĺžka_VALUE) {
    return 결과검사(사용자호출(39,účastník,(uintptr_t)adresa,(uintptr_t)dĺžka_VALUE,0,0,0));
}

/* Súbor 함수도 독립된 Slovenský funkcia_VALUE 심볼로 제공한다. */
int otvoriť_Súbor(const char *Cesta,int metóda_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)Cesta,metóda_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Súbor,void *údaje,size_t položka_COUNT) { return 결과검사(사용자호출(2,Súbor,(uintptr_t)údaje,položka_COUNT,0,0,0)); }
입출력결과형 zapísať_Súbor_údaje(int Súbor,const void *údaje,size_t položka_COUNT) { return 결과검사(사용자호출(1,Súbor,(uintptr_t)údaje,položka_COUNT,0,0,0)); }
int Zavrieť_Súbor(int Súbor) { return 결과검사(사용자호출(4,Súbor,0,0,0,0,0)); }
Súbor_Posun_Typ hľadať_Súbor(int Súbor,Súbor_Posun_Typ 거리,int akcia_koreň) { return 결과검사(사용자호출(5,Súbor,거리,akcia_koreň,0,0,0)); }
int odobrať_Súbor_položka_názov(const char *Cesta) { return 결과검사(사용자호출(11,(uintptr_t)Cesta,0,0,0,0,0)); }
int množina_Súbor_dĺžka(int Súbor,Súbor_Posun_Typ Veľkosť) { return 결과검사(사용자호출(10,Súbor,Veľkosť,0,0,0,0)); }
int potvrdenie_ukladací_priestor_súborov(int Súbor) { return 결과검사(사용자호출(12,Súbor,0,0,0,0,0)); }
int veľkosť_súboru(int Súbor) { return 결과검사(사용자호출(9,Súbor,0,0,0,0,0)); }

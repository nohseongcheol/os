// 동일 magyar 헤더를 사용하는 별도 EL0 kódtár. kernel_ÉRTÉK 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int hibakód;
int *pk_errno_location(void) { return &hibakód; }
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) { hibakód = -KR; return -1; } return KR; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fájl_Ofszet_beír pk_lseek(int fd, Fájl_Ofszet_beír offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fájl_Ofszet_beír size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* magyar 공개 함수의 tényleges_adat EL0 구현. 구조체는 SVC에서 másol_ÉRTÉK·검증한다. */
int készít_végpont(int CÍM_Család,int kommunikáció_mód,int átvisz_protokoll) {
    return 결과검사(사용자호출(32,CÍM_Család,kommunikáció_mód,átvisz_protokoll,0,0,0));
}
int BIND_CÍM(int végpont,const struct szoftvercsatorna_CÍM *CÍM,szoftvercsatorna_CÍM_hossz_beír hossz_ÉRTÉK) {
    return 결과검사(사용자호출(33,végpont,(uintptr_t)CÍM,hossz_ÉRTÉK,0,0,0));
}
intptr_t küld_datagram_adat(int végpont,const void *adat,size_t cikk_DARAB,int kijelölés_ÉRTÉK,const struct szoftvercsatorna_CÍM *CÍM,szoftvercsatorna_CÍM_hossz_beír hossz_ÉRTÉK) {
    return 결과검사(사용자호출(34,végpont,(uintptr_t)adat,cikk_DARAB,kijelölés_ÉRTÉK,(uintptr_t)CÍM,hossz_ÉRTÉK));
}
intptr_t fogad_datagram_adat(int végpont,void *adat,size_t cikk_DARAB,int kijelölés_ÉRTÉK,struct szoftvercsatorna_CÍM *CÍM,szoftvercsatorna_CÍM_hossz_beír *hossz_ÉRTÉK) {
    return 결과검사(사용자호출(35,végpont,(uintptr_t)adat,cikk_DARAB,kijelölés_ÉRTÉK,(uintptr_t)CÍM,(uintptr_t)hossz_ÉRTÉK));
}
int 통신주소읽기(int végpont,struct szoftvercsatorna_CÍM *CÍM,szoftvercsatorna_CÍM_hossz_beír *hossz_ÉRTÉK) {
    return 결과검사(사용자호출(36,végpont,(uintptr_t)CÍM,(uintptr_t)hossz_ÉRTÉK,0,0,0));
}
int KAPCSOLAT_hálózat(int végpont,const struct szoftvercsatorna_CÍM *CÍM,szoftvercsatorna_CÍM_hossz_beír hossz_ÉRTÉK) {
    return 결과검사(사용자호출(37,végpont,(uintptr_t)CÍM,hossz_ÉRTÉK,0,0,0));
}
int 통신연결기다리기(int végpont,int Várok_DARAB) {
    return 결과검사(사용자호출(38,végpont,Várok_DARAB,0,0,0,0));
}
int elfogad_hálózati_kapcsolat(int végpont,struct szoftvercsatorna_CÍM *CÍM,szoftvercsatorna_CÍM_hossz_beír *hossz_ÉRTÉK) {
    return 결과검사(사용자호출(39,végpont,(uintptr_t)CÍM,(uintptr_t)hossz_ÉRTÉK,0,0,0));
}

/* Fájl 함수도 독립된 magyar FÜGGVÉNY_ÉRTÉK 심볼로 제공한다. */
int készít_Fájl(const char *ÚTVONAL,int metódus_mód,...) { return 결과검사(사용자호출(3,(uintptr_t)ÚTVONAL,metódus_mód,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fájl,void *adat,size_t cikk_DARAB) { return 결과검사(사용자호출(2,Fájl,(uintptr_t)adat,cikk_DARAB,0,0,0)); }
입출력결과형 ír_Fájl_adat(int Fájl,const void *adat,size_t cikk_DARAB) { return 결과검사(사용자호출(1,Fájl,(uintptr_t)adat,cikk_DARAB,0,0,0)); }
int bezár_Fájl(int Fájl) { return 결과검사(사용자호출(4,Fájl,0,0,0,0,0)); }
Fájl_Ofszet_beír keres_Fájl(int Fájl,Fájl_Ofszet_beír 거리,int teendő_gyök) { return 결과검사(사용자호출(5,Fájl,거리,teendő_gyök,0,0,0)); }
int eltávolít_Fájl_bejegyzés_név(const char *ÚTVONAL) { return 결과검사(사용자호출(11,(uintptr_t)ÚTVONAL,0,0,0,0,0)); }
int halmaz_Fájl_hossz(int Fájl,Fájl_Ofszet_beír Méret) { return 결과검사(사용자호출(10,Fájl,Méret,0,0,0,0)); }
int véglegesít_Files(int Fájl) { return 결과검사(사용자호출(12,Fájl,0,0,0,0,0)); }
int fájlméret(int Fájl) { return 결과검사(사용자호출(9,Fájl,0,0,0,0,0)); }

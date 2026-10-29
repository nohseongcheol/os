// 동일 čeština 헤더를 사용하는 별도 EL0 knihovna. jádro_HODNOTA 직접 호출판과 혼합 금지.
#include "Soubor_ABI.h"
#include "호출.h"
#include "síť_ABI.h"
static int kód_chyby;
int *pk_errno_location(void) { return &kód_chyby; }
static intptr_t 결과검사(intptr_t VÝSLEDEK) { if (VÝSLEDEK < 0) { kód_chyby = -VÝSLEDEK; return -1; } return VÝSLEDEK; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Soubor_POSUN_TYP pk_lseek(int fd, Soubor_POSUN_TYP offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Soubor_POSUN_TYP size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* čeština 공개 함수의 skutečný_data EL0 implementace. 구조체는 SVC에서 instance_HODNOTA·검증한다. */
int Create_účastník(int ODKAZ_řada,int komunikace_MODE,int přenos_protokol) {
    return 결과검사(사용자호출(32,ODKAZ_řada,komunikace_MODE,přenos_protokol,0,0,0));
}
int vázat_ODKAZ(int účastník,const struct soket_ODKAZ *Adresa,soket_ODKAZ_délka_TYP délka_HODNOTA) {
    return 결과검사(사용자호출(33,účastník,(uintptr_t)Adresa,délka_HODNOTA,0,0,0));
}
intptr_t poslat_datagram_data(int účastník,const void *data,size_t zboží_POČET,int výběr_HODNOTA,const struct soket_ODKAZ *Adresa,soket_ODKAZ_délka_TYP délka_HODNOTA) {
    return 결과검사(사용자호출(34,účastník,(uintptr_t)data,zboží_POČET,výběr_HODNOTA,(uintptr_t)Adresa,délka_HODNOTA));
}
intptr_t dostat_datagram_data(int účastník,void *data,size_t zboží_POČET,int výběr_HODNOTA,struct soket_ODKAZ *Adresa,soket_ODKAZ_délka_TYP *délka_HODNOTA) {
    return 결과검사(사용자호출(35,účastník,(uintptr_t)data,zboží_POČET,výběr_HODNOTA,(uintptr_t)Adresa,(uintptr_t)délka_HODNOTA));
}
int 통신주소읽기(int účastník,struct soket_ODKAZ *Adresa,soket_ODKAZ_délka_TYP *délka_HODNOTA) {
    return 결과검사(사용자호출(36,účastník,(uintptr_t)Adresa,(uintptr_t)délka_HODNOTA,0,0,0));
}
int spojit_síť(int účastník,const struct soket_ODKAZ *Adresa,soket_ODKAZ_délka_TYP délka_HODNOTA) {
    return 결과검사(사용자호출(37,účastník,(uintptr_t)Adresa,délka_HODNOTA,0,0,0));
}
int 통신연결기다리기(int účastník,int Čekám_POČET) {
    return 결과검사(사용자호출(38,účastník,Čekám_POČET,0,0,0,0));
}
int přijmout_síťové_připojení(int účastník,struct soket_ODKAZ *Adresa,soket_ODKAZ_délka_TYP *délka_HODNOTA) {
    return 결과검사(사용자호출(39,účastník,(uintptr_t)Adresa,(uintptr_t)délka_HODNOTA,0,0,0));
}

/* název_souboru 함수도 독립된 čeština funkce_HODNOTA 심볼로 제공한다. */
int otevřít_Soubor(const char *cesta_2,int metoda_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)cesta_2,metoda_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int název_souboru,void *data,size_t zboží_POČET) { return 결과검사(사용자호출(2,název_souboru,(uintptr_t)data,zboží_POČET,0,0,0)); }
입출력결과형 zápis_Soubor_data(int název_souboru,const void *data,size_t zboží_POČET) { return 결과검사(사용자호출(1,název_souboru,(uintptr_t)data,zboží_POČET,0,0,0)); }
int Zavřít_Soubor(int název_souboru) { return 결과검사(사용자호출(4,název_souboru,0,0,0,0,0)); }
Soubor_POSUN_TYP hledat_Soubor(int název_souboru,Soubor_POSUN_TYP 거리,int akce_kořen) { return 결과검사(사용자호출(5,název_souboru,거리,akce_kořen,0,0,0)); }
int odebrat_Soubor_položka_název(const char *cesta_2) { return 결과검사(사용자호출(11,(uintptr_t)cesta_2,0,0,0,0,0)); }
int sada_Soubor_délka(int název_souboru,Soubor_POSUN_TYP Velikost) { return 결과검사(사용자호출(10,název_souboru,Velikost,0,0,0,0)); }
int zápis_Files(int název_souboru) { return 결과검사(사용자호출(12,název_souboru,0,0,0,0,0)); }
int velikost_souboru(int název_souboru) { return 결과검사(사용자호출(9,název_souboru,0,0,0,0,0)); }

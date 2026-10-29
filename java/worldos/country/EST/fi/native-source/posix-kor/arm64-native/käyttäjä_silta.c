// 동일 suomi 헤더를 사용하는 별도 EL0 kirjasto. ydin_ARVO 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int virhekoodi;
int *pk_errno_location(void) { return &virhekoodi; }
static intptr_t 결과검사(intptr_t TULOS) { if (TULOS < 0) { virhekoodi = -TULOS; return -1; } return TULOS; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Tiedosto_SIIRTYMÄ_TYYPPI pk_lseek(int fd, Tiedosto_SIIRTYMÄ_TYYPPI offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Tiedosto_SIIRTYMÄ_TYYPPI size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* suomi 공개 함수의 todellinen_data EL0 toteutus. 구조체는 SVC에서 kopioida_ARVO·검증한다. */
int Luo_päätepiste(int OSOITE_Perhe,int 통신방식,int Siirrä_protokolla) {
    return 결과검사(사용자호출(32,OSOITE_Perhe,통신방식,Siirrä_protokolla,0,0,0));
}
int BIND_OSOITE(int päätepiste,const struct vastake_OSOITE *OSOITE,vastake_OSOITE_kesto_TYYPPI kesto_ARVO) {
    return 결과검사(사용자호출(33,päätepiste,(uintptr_t)OSOITE,kesto_ARVO,0,0,0));
}
intptr_t lähettää_datagrammi_data(int päätepiste,const void *data,size_t kohde_LASKE,int valinta_ARVO,const struct vastake_OSOITE *OSOITE,vastake_OSOITE_kesto_TYYPPI kesto_ARVO) {
    return 결과검사(사용자호출(34,päätepiste,(uintptr_t)data,kohde_LASKE,valinta_ARVO,(uintptr_t)OSOITE,kesto_ARVO));
}
intptr_t saada_datagrammi_data(int päätepiste,void *data,size_t kohde_LASKE,int valinta_ARVO,struct vastake_OSOITE *OSOITE,vastake_OSOITE_kesto_TYYPPI *kesto_ARVO) {
    return 결과검사(사용자호출(35,päätepiste,(uintptr_t)data,kohde_LASKE,valinta_ARVO,(uintptr_t)OSOITE,(uintptr_t)kesto_ARVO));
}
int lukea_vastake_OSOITE(int päätepiste,struct vastake_OSOITE *OSOITE,vastake_OSOITE_kesto_TYYPPI *kesto_ARVO) {
    return 결과검사(사용자호출(36,päätepiste,(uintptr_t)OSOITE,(uintptr_t)kesto_ARVO,0,0,0));
}
int YHDISTÄ_verkko(int päätepiste,const struct vastake_OSOITE *OSOITE,vastake_OSOITE_kesto_TYYPPI kesto_ARVO) {
    return 결과검사(사용자호출(37,päätepiste,(uintptr_t)OSOITE,kesto_ARVO,0,0,0));
}
int 통신연결기다리기(int päätepiste,int Odotetaan_LASKE) {
    return 결과검사(사용자호출(38,päätepiste,Odotetaan_LASKE,0,0,0,0));
}
int hyväksyä_verkkoyhteys(int päätepiste,struct vastake_OSOITE *OSOITE,vastake_OSOITE_kesto_TYYPPI *kesto_ARVO) {
    return 결과검사(사용자호출(39,päätepiste,(uintptr_t)OSOITE,(uintptr_t)kesto_ARVO,0,0,0));
}

/* tiedoston_nimi 함수도 독립된 suomi funktio_ARVO 심볼로 제공한다. */
int avata_Tiedosto(const char *polku_2,int menetelmä_tila,...) { return 결과검사(사용자호출(3,(uintptr_t)polku_2,menetelmä_tila,0,0,0,0)); }
입출력결과형 lukea_Tiedosto_data(int tiedoston_nimi,void *data,size_t kohde_LASKE) { return 결과검사(사용자호출(2,tiedoston_nimi,(uintptr_t)data,kohde_LASKE,0,0,0)); }
입출력결과형 kirjoitus_Tiedosto_data(int tiedoston_nimi,const void *data,size_t kohde_LASKE) { return 결과검사(사용자호출(1,tiedoston_nimi,(uintptr_t)data,kohde_LASKE,0,0,0)); }
int Sulje_Tiedosto(int tiedoston_nimi) { return 결과검사(사용자호출(4,tiedoston_nimi,0,0,0,0,0)); }
Tiedosto_SIIRTYMÄ_TYYPPI hae_Tiedosto(int tiedoston_nimi,Tiedosto_SIIRTYMÄ_TYYPPI 거리,int aloite_juuri) { return 결과검사(사용자호출(5,tiedoston_nimi,거리,aloite_juuri,0,0,0)); }
int poistaa_Tiedosto_merkintä_nimi(const char *polku_2) { return 결과검사(사용자호출(11,(uintptr_t)polku_2,0,0,0,0,0)); }
int ryhmä_Tiedosto_kesto(int tiedoston_nimi,Tiedosto_SIIRTYMÄ_TYYPPI Koko) { return 결과검사(사용자호출(10,tiedoston_nimi,Koko,0,0,0,0)); }
int vahvistaa_muutokset_Files(int tiedoston_nimi) { return 결과검사(사용자호출(12,tiedoston_nimi,0,0,0,0,0)); }
int tiedostokoko(int tiedoston_nimi) { return 결과검사(사용자호출(9,tiedoston_nimi,0,0,0,0,0)); }

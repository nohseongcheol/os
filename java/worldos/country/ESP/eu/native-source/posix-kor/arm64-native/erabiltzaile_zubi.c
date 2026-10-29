// 동일 Euskara 헤더를 사용하는 별도 EL0 liburutegi. nukleo_balio 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int errore_kode;
int *pk_errno_location(void) { return &errore_kode; }
static intptr_t 결과검사(intptr_t EMAITZA) { if (EMAITZA < 0) { errore_kode = -EMAITZA; return -1; } return EMAITZA; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fitxategi_Geruzak_MOTA pk_lseek(int fd, fitxategi_Geruzak_MOTA offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fitxategi_Geruzak_MOTA size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Euskara 공개 함수의 benetako_datuak EL0 구현. 구조체는 SVC에서 kopiatu_balio·검증한다. */
int sortu_amaiera_puntu(int helbide_sorta,int 통신방식,int transferitu_protokolo) {
    return 결과검사(사용자호출(32,helbide_sorta,통신방식,transferitu_protokolo,0,0,0));
}
int lotu_helbide(int amaiera_puntu,const struct 통신주소 *helbide,통신주소길이형 luzera_balio) {
    return 결과검사(사용자호출(33,amaiera_puntu,(uintptr_t)helbide,luzera_balio,0,0,0));
}
intptr_t 자료전문보내기(int amaiera_puntu,const void *datuak,size_t elementu_ZENBATU,int hautapen_balio,const struct 통신주소 *helbide,통신주소길이형 luzera_balio) {
    return 결과검사(사용자호출(34,amaiera_puntu,(uintptr_t)datuak,elementu_ZENBATU,hautapen_balio,(uintptr_t)helbide,luzera_balio));
}
intptr_t 자료전문받기(int amaiera_puntu,void *datuak,size_t elementu_ZENBATU,int hautapen_balio,struct 통신주소 *helbide,통신주소길이형 *luzera_balio) {
    return 결과검사(사용자호출(35,amaiera_puntu,(uintptr_t)datuak,elementu_ZENBATU,hautapen_balio,(uintptr_t)helbide,(uintptr_t)luzera_balio));
}
int 통신주소읽기(int amaiera_puntu,struct 통신주소 *helbide,통신주소길이형 *luzera_balio) {
    return 결과검사(사용자호출(36,amaiera_puntu,(uintptr_t)helbide,(uintptr_t)luzera_balio,0,0,0));
}
int KONEKTATU_sare(int amaiera_puntu,const struct 통신주소 *helbide,통신주소길이형 luzera_balio) {
    return 결과검사(사용자호출(37,amaiera_puntu,(uintptr_t)helbide,luzera_balio,0,0,0));
}
int 통신연결기다리기(int amaiera_puntu,int Zain_ZENBATU) {
    return 결과검사(사용자호출(38,amaiera_puntu,Zain_ZENBATU,0,0,0,0));
}
int onartu_sare_konexio(int amaiera_puntu,struct 통신주소 *helbide,통신주소길이형 *luzera_balio) {
    return 결과검사(사용자호출(39,amaiera_puntu,(uintptr_t)helbide,(uintptr_t)luzera_balio,0,0,0));
}

/* Fitxategia 함수도 독립된 Euskara FUNTZIOA_balio 심볼로 제공한다. */
int ireki_fitxategi(const char *Bide_izena,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)Bide_izena,방식,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fitxategia,void *datuak,size_t elementu_ZENBATU) { return 결과검사(사용자호출(2,Fitxategia,(uintptr_t)datuak,elementu_ZENBATU,0,0,0)); }
입출력결과형 idatzi_fitxategi_datuak(int Fitxategia,const void *datuak,size_t elementu_ZENBATU) { return 결과검사(사용자호출(1,Fitxategia,(uintptr_t)datuak,elementu_ZENBATU,0,0,0)); }
int itxi_fitxategi(int Fitxategia) { return 결과검사(사용자호출(4,Fitxategia,0,0,0,0,0)); }
fitxategi_Geruzak_MOTA bilatu_fitxategi(int Fitxategia,fitxategi_Geruzak_MOTA 거리,int Project_erro) { return 결과검사(사용자호출(5,Fitxategia,거리,Project_erro,0,0,0)); }
int kendu_fitxategi_sarrera_izen(const char *Bide_izena) { return 결과검사(사용자호출(11,(uintptr_t)Bide_izena,0,0,0,0,0)); }
int sorta_fitxategi_luzera(int Fitxategia,fitxategi_Geruzak_MOTA Tamaina) { return 결과검사(사용자호출(10,Fitxategia,Tamaina,0,0,0,0)); }
int 파일저장확정(int Fitxategia) { return 결과검사(사용자호출(12,Fitxategia,0,0,0,0,0)); }
int 파일크기(int Fitxategia) { return 결과검사(사용자호출(9,Fitxategia,0,0,0,0,0)); }

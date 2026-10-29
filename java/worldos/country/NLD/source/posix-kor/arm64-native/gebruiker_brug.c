// 동일 Nederlands 헤더를 사용하는 별도 EL0 bibliotheek. kernel_WAARDE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int foutcode;
int *pk_errno_location(void) { return &foutcode; }
static intptr_t 결과검사(intptr_t resultaat) { if (resultaat < 0) { foutcode = -resultaat; return -1; } return resultaat; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Bestand_VERSCHUIVING_TYPE pk_lseek(int fd, Bestand_VERSCHUIVING_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Bestand_VERSCHUIVING_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Nederlands 공개 함수의 werkelijk_gegevens EL0 implementatie. 구조체는 SVC에서 kopiëren_WAARDE·검증한다. */
int maken_eindpunt(int ADRES_Gezin,int communicatie_MODUS,int transfer_protocol) {
    return 결과검사(사용자호출(32,ADRES_Gezin,communicatie_MODUS,transfer_protocol,0,0,0));
}
int BIND_ADRES(int eindpunt,const struct socket_ADRES *ADRES,socket_ADRES_tijdsduur_TYPE tijdsduur_WAARDE) {
    return 결과검사(사용자호출(33,eindpunt,(uintptr_t)ADRES,tijdsduur_WAARDE,0,0,0));
}
intptr_t e_mailen_datagram_gegevens(int eindpunt,const void *gegevens,size_t item_AANTAL,int selectie_WAARDE,const struct socket_ADRES *ADRES,socket_ADRES_tijdsduur_TYPE tijdsduur_WAARDE) {
    return 결과검사(사용자호출(34,eindpunt,(uintptr_t)gegevens,item_AANTAL,selectie_WAARDE,(uintptr_t)ADRES,tijdsduur_WAARDE));
}
intptr_t ontvangen_datagram_gegevens(int eindpunt,void *gegevens,size_t item_AANTAL,int selectie_WAARDE,struct socket_ADRES *ADRES,socket_ADRES_tijdsduur_TYPE *tijdsduur_WAARDE) {
    return 결과검사(사용자호출(35,eindpunt,(uintptr_t)gegevens,item_AANTAL,selectie_WAARDE,(uintptr_t)ADRES,(uintptr_t)tijdsduur_WAARDE));
}
int 통신주소읽기(int eindpunt,struct socket_ADRES *ADRES,socket_ADRES_tijdsduur_TYPE *tijdsduur_WAARDE) {
    return 결과검사(사용자호출(36,eindpunt,(uintptr_t)ADRES,(uintptr_t)tijdsduur_WAARDE,0,0,0));
}
int VERBINDEN_net(int eindpunt,const struct socket_ADRES *ADRES,socket_ADRES_tijdsduur_TYPE tijdsduur_WAARDE) {
    return 결과검사(사용자호출(37,eindpunt,(uintptr_t)ADRES,tijdsduur_WAARDE,0,0,0));
}
int 통신연결기다리기(int eindpunt,int Wachten_AANTAL) {
    return 결과검사(사용자호출(38,eindpunt,Wachten_AANTAL,0,0,0,0));
}
int accepteren_netwerkverbinding(int eindpunt,struct socket_ADRES *ADRES,socket_ADRES_tijdsduur_TYPE *tijdsduur_WAARDE) {
    return 결과검사(사용자호출(39,eindpunt,(uintptr_t)ADRES,(uintptr_t)tijdsduur_WAARDE,0,0,0));
}

/* bestand 함수도 독립된 Nederlands FUNCTIE_WAARDE 심볼로 제공한다. */
int open_Bestand(const char *pad,int methode_MODUS,...) { return 결과검사(사용자호출(3,(uintptr_t)pad,methode_MODUS,0,0,0,0)); }
입출력결과형 파일자료읽기(int bestand,void *gegevens,size_t item_AANTAL) { return 결과검사(사용자호출(2,bestand,(uintptr_t)gegevens,item_AANTAL,0,0,0)); }
입출력결과형 schrijven_Bestand_gegevens(int bestand,const void *gegevens,size_t item_AANTAL) { return 결과검사(사용자호출(1,bestand,(uintptr_t)gegevens,item_AANTAL,0,0,0)); }
int Sluiten_Bestand(int bestand) { return 결과검사(사용자호출(4,bestand,0,0,0,0,0)); }
Bestand_VERSCHUIVING_TYPE zoeken_Bestand(int bestand,Bestand_VERSCHUIVING_TYPE 거리,int Taken_wortel) { return 결과검사(사용자호출(5,bestand,거리,Taken_wortel,0,0,0)); }
int verwijderen_Bestand_invoer_naam(const char *pad) { return 결과검사(사용자호출(11,(uintptr_t)pad,0,0,0,0,0)); }
int set_Bestand_tijdsduur(int bestand,Bestand_VERSCHUIVING_TYPE Grootte) { return 결과검사(사용자호출(10,bestand,Grootte,0,0,0,0)); }
int doorvoeren_Files(int bestand) { return 결과검사(사용자호출(12,bestand,0,0,0,0,0)); }
int bestandsgrootte(int bestand) { return 결과검사(사용자호출(9,bestand,0,0,0,0,0)); }

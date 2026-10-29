// 동일 Svenska 헤더를 사용하는 별도 EL0 bibliotek. kärna_värde 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int felkod;
int *pk_errno_location(void) { return &felkod; }
static intptr_t 결과검사(intptr_t RESULTAT) { if (RESULTAT < 0) { felkod = -RESULTAT; return -1; } return RESULTAT; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fil_FÖRSKJUTNING_Typ pk_lseek(int fd, fil_FÖRSKJUTNING_Typ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fil_FÖRSKJUTNING_Typ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Svenska 공개 함수의 verklig_data EL0 implementation. 구조체는 SVC에서 kopia_värde·검증한다. */
int Skapa_deltagare(int ADRESS_serie,int kommunikation_läge,int Överför_protokoll) {
    return 결과검사(사용자호출(32,ADRESS_serie,kommunikation_läge,Överför_protokoll,0,0,0));
}
int BIND_ADRESS(int deltagare,const struct socket_ADRESS *Adress,socket_ADRESS_längd_Typ längd_värde) {
    return 결과검사(사용자호출(33,deltagare,(uintptr_t)Adress,längd_värde,0,0,0));
}
intptr_t skicka_datagram_data(int deltagare,const void *data,size_t objekt_ANTAL,int markering_värde,const struct socket_ADRESS *Adress,socket_ADRESS_längd_Typ längd_värde) {
    return 결과검사(사용자호출(34,deltagare,(uintptr_t)data,objekt_ANTAL,markering_värde,(uintptr_t)Adress,längd_värde));
}
intptr_t få_datagram_data(int deltagare,void *data,size_t objekt_ANTAL,int markering_värde,struct socket_ADRESS *Adress,socket_ADRESS_längd_Typ *längd_värde) {
    return 결과검사(사용자호출(35,deltagare,(uintptr_t)data,objekt_ANTAL,markering_värde,(uintptr_t)Adress,(uintptr_t)längd_värde));
}
int läsa_socket_ADRESS(int deltagare,struct socket_ADRESS *Adress,socket_ADRESS_längd_Typ *längd_värde) {
    return 결과검사(사용자호출(36,deltagare,(uintptr_t)Adress,(uintptr_t)längd_värde,0,0,0));
}
int ANSLUT_nätverk(int deltagare,const struct socket_ADRESS *Adress,socket_ADRESS_längd_Typ längd_värde) {
    return 결과검사(사용자호출(37,deltagare,(uintptr_t)Adress,längd_värde,0,0,0));
}
int 통신연결기다리기(int deltagare,int 대기수) {
    return 결과검사(사용자호출(38,deltagare,대기수,0,0,0,0));
}
int acceptera_nätverksanslutning(int deltagare,struct socket_ADRESS *Adress,socket_ADRESS_längd_Typ *längd_värde) {
    return 결과검사(사용자호출(39,deltagare,(uintptr_t)Adress,(uintptr_t)längd_värde,0,0,0));
}

/* filnamn 함수도 독립된 Svenska FUNKTION_värde 심볼로 제공한다. */
int skapa_fil(const char *sökväg_2,int metod_läge,...) { return 결과검사(사용자호출(3,(uintptr_t)sökväg_2,metod_läge,0,0,0,0)); }
입출력결과형 läsa_fil_data(int filnamn,void *data,size_t objekt_ANTAL) { return 결과검사(사용자호출(2,filnamn,(uintptr_t)data,objekt_ANTAL,0,0,0)); }
입출력결과형 skriva_fil_data(int filnamn,const void *data,size_t objekt_ANTAL) { return 결과검사(사용자호출(1,filnamn,(uintptr_t)data,objekt_ANTAL,0,0,0)); }
int Stäng_fil(int filnamn) { return 결과검사(사용자호출(4,filnamn,0,0,0,0,0)); }
fil_FÖRSKJUTNING_Typ söka_fil(int filnamn,fil_FÖRSKJUTNING_Typ 거리,int åtgärd_rot) { return 결과검사(사용자호출(5,filnamn,거리,åtgärd_rot,0,0,0)); }
int ta_bort_fil_post_namn(const char *sökväg_2) { return 결과검사(사용자호출(11,(uintptr_t)sökväg_2,0,0,0,0,0)); }
int uppsättning_fil_längd(int filnamn,fil_FÖRSKJUTNING_Typ Storlek) { return 결과검사(사용자호출(10,filnamn,Storlek,0,0,0,0)); }
int incheckning_Files(int filnamn) { return 결과검사(사용자호출(12,filnamn,0,0,0,0,0)); }
int filstorlek(int filnamn) { return 결과검사(사용자호출(9,filnamn,0,0,0,0,0)); }

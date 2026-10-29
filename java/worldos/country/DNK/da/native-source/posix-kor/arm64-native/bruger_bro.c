// 동일 Dansk 헤더를 사용하는 별도 EL0 bibliotek. kerne_VÆRDI 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int fejlkode;
int *pk_errno_location(void) { return &fejlkode; }
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) { fejlkode = -KR; return -1; } return KR; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fil_FORSKYDNING_Type pk_lseek(int fd, fil_FORSKYDNING_Type offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fil_FORSKYDNING_Type size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Dansk 공개 함수의 faktisk_data EL0 구현. 구조체는 SVC에서 kopiere_VÆRDI·검증한다. */
int åbne_slutpunkt(int mail_serie,int 통신방식,int overføre_protokol) {
    return 결과검사(사용자호출(32,mail_serie,통신방식,overføre_protokol,0,0,0));
}
int BIND_mail(int slutpunkt,const struct socket_mail *mail,socket_mail_varighed_Type varighed_VÆRDI) {
    return 결과검사(사용자호출(33,slutpunkt,(uintptr_t)mail,varighed_VÆRDI,0,0,0));
}
intptr_t maile_datagram_data(int slutpunkt,const void *data,size_t vare_TÆL,int markering_VÆRDI,const struct socket_mail *mail,socket_mail_varighed_Type varighed_VÆRDI) {
    return 결과검사(사용자호출(34,slutpunkt,(uintptr_t)data,vare_TÆL,markering_VÆRDI,(uintptr_t)mail,varighed_VÆRDI));
}
intptr_t modtage_datagram_data(int slutpunkt,void *data,size_t vare_TÆL,int markering_VÆRDI,struct socket_mail *mail,socket_mail_varighed_Type *varighed_VÆRDI) {
    return 결과검사(사용자호출(35,slutpunkt,(uintptr_t)data,vare_TÆL,markering_VÆRDI,(uintptr_t)mail,(uintptr_t)varighed_VÆRDI));
}
int 통신주소읽기(int slutpunkt,struct socket_mail *mail,socket_mail_varighed_Type *varighed_VÆRDI) {
    return 결과검사(사용자호출(36,slutpunkt,(uintptr_t)mail,(uintptr_t)varighed_VÆRDI,0,0,0));
}
int Forbind_netværk(int slutpunkt,const struct socket_mail *mail,socket_mail_varighed_Type varighed_VÆRDI) {
    return 결과검사(사용자호출(37,slutpunkt,(uintptr_t)mail,varighed_VÆRDI,0,0,0));
}
int 통신연결기다리기(int slutpunkt,int Venter_TÆL) {
    return 결과검사(사용자호출(38,slutpunkt,Venter_TÆL,0,0,0,0));
}
int acceptere_netværksforbindelse(int slutpunkt,struct socket_mail *mail,socket_mail_varighed_Type *varighed_VÆRDI) {
    return 결과검사(사용자호출(39,slutpunkt,(uintptr_t)mail,(uintptr_t)varighed_VÆRDI,0,0,0));
}

/* Fil 함수도 독립된 Dansk FUNKTION_VÆRDI 심볼로 제공한다. */
int åben_fil(const char *Sti,int metode_HYPPIGST,...) { return 결과검사(사용자호출(3,(uintptr_t)Sti,metode_HYPPIGST,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fil,void *data,size_t vare_TÆL) { return 결과검사(사용자호출(2,Fil,(uintptr_t)data,vare_TÆL,0,0,0)); }
입출력결과형 skrive_fil_data(int Fil,const void *data,size_t vare_TÆL) { return 결과검사(사용자호출(1,Fil,(uintptr_t)data,vare_TÆL,0,0,0)); }
int Luk_fil(int Fil) { return 결과검사(사용자호출(4,Fil,0,0,0,0,0)); }
fil_FORSKYDNING_Type søge_fil(int Fil,fil_FORSKYDNING_Type 거리,int To_do_rod) { return 결과검사(사용자호출(5,Fil,거리,To_do_rod,0,0,0)); }
int fjerne_fil_post_navn(const char *Sti) { return 결과검사(사용자호출(11,(uintptr_t)Sti,0,0,0,0,0)); }
int sæt_fil_varighed(int Fil,fil_FORSKYDNING_Type Størrelse) { return 결과검사(사용자호출(10,Fil,Størrelse,0,0,0,0)); }
int udføre_Files(int Fil) { return 결과검사(사용자호출(12,Fil,0,0,0,0,0)); }
int filstørrelse(int Fil) { return 결과검사(사용자호출(9,Fil,0,0,0,0,0)); }

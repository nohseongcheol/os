// 동일 norsk 헤더를 사용하는 별도 EL0 bibliotek. kjerne_VERDI 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int feil_KODE;
int *pk_errno_location(void) { return &feil_KODE; }
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) { feil_KODE = -KR; return -1; } return KR; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fil_FORSKYVNING_Type pk_lseek(int fd, Fil_FORSKYVNING_Type offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fil_FORSKYVNING_Type size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* norsk 공개 함수의 faktisk_data EL0 구현. 구조체는 SVC에서 kopiere_VERDI·검증한다. */
int åpne_deltaker(int e_post_serie,int 통신방식,int overføre_protokoll) {
    return 결과검사(사용자호출(32,e_post_serie,통신방식,overføre_protokoll,0,0,0));
}
int BIND_e_post(int deltaker,const struct socket_e_post *e_post,socket_e_post_lengde_Type lengde_VERDI) {
    return 결과검사(사용자호출(33,deltaker,(uintptr_t)e_post,lengde_VERDI,0,0,0));
}
intptr_t sende_datagram_data(int deltaker,const void *data,size_t vare_ANTALL,int merket_område_VERDI,const struct socket_e_post *e_post,socket_e_post_lengde_Type lengde_VERDI) {
    return 결과검사(사용자호출(34,deltaker,(uintptr_t)data,vare_ANTALL,merket_område_VERDI,(uintptr_t)e_post,lengde_VERDI));
}
intptr_t motta_datagram_data(int deltaker,void *data,size_t vare_ANTALL,int merket_område_VERDI,struct socket_e_post *e_post,socket_e_post_lengde_Type *lengde_VERDI) {
    return 결과검사(사용자호출(35,deltaker,(uintptr_t)data,vare_ANTALL,merket_område_VERDI,(uintptr_t)e_post,(uintptr_t)lengde_VERDI));
}
int 통신주소읽기(int deltaker,struct socket_e_post *e_post,socket_e_post_lengde_Type *lengde_VERDI) {
    return 결과검사(사용자호출(36,deltaker,(uintptr_t)e_post,(uintptr_t)lengde_VERDI,0,0,0));
}
int KOBLE_TIL_nettverk(int deltaker,const struct socket_e_post *e_post,socket_e_post_lengde_Type lengde_VERDI) {
    return 결과검사(사용자호출(37,deltaker,(uintptr_t)e_post,lengde_VERDI,0,0,0));
}
int 통신연결기다리기(int deltaker,int Venter_ANTALL) {
    return 결과검사(사용자호출(38,deltaker,Venter_ANTALL,0,0,0,0));
}
int godta_nettverkstilkobling(int deltaker,struct socket_e_post *e_post,socket_e_post_lengde_Type *lengde_VERDI) {
    return 결과검사(사용자호출(39,deltaker,(uintptr_t)e_post,(uintptr_t)lengde_VERDI,0,0,0));
}

/* Fil 함수도 독립된 norsk FUNKSJON_VERDI 심볼로 제공한다. */
int åpen_Fil(const char *Sti,int metode_MODUS,...) { return 결과검사(사용자호출(3,(uintptr_t)Sti,metode_MODUS,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fil,void *data,size_t vare_ANTALL) { return 결과검사(사용자호출(2,Fil,(uintptr_t)data,vare_ANTALL,0,0,0)); }
입출력결과형 skrive_Fil_data(int Fil,const void *data,size_t vare_ANTALL) { return 결과검사(사용자호출(1,Fil,(uintptr_t)data,vare_ANTALL,0,0,0)); }
int Lukk_Fil(int Fil) { return 결과검사(사용자호출(4,Fil,0,0,0,0,0)); }
Fil_FORSKYVNING_Type søk_Fil(int Fil,Fil_FORSKYVNING_Type 거리,int speile_rot) { return 결과검사(사용자호출(5,Fil,거리,speile_rot,0,0,0)); }
int fjerne_Fil_oppføring_navn(const char *Sti) { return 결과검사(사용자호출(11,(uintptr_t)Sti,0,0,0,0,0)); }
int sett_Fil_lengde(int Fil,Fil_FORSKYVNING_Type Størrelse) { return 결과검사(사용자호출(10,Fil,Størrelse,0,0,0,0)); }
int 파일저장확정(int Fil) { return 결과검사(사용자호출(12,Fil,0,0,0,0,0)); }
int filstørrelse(int Fil) { return 결과검사(사용자호출(9,Fil,0,0,0,0,0)); }

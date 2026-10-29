// 동일 한국어 헤더를 사용하는 별도 EL0 Kitaphana. ýadro_baha 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int säwlik_kody;
int *pk_errno_location(void) { return &säwlik_kody; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { säwlik_kody = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
faýl_Süýşüriş_ýaz pk_lseek(int fd, faýl_Süýşüriş_ýaz offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, faýl_Süýşüriş_ýaz size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 hakyky_maglumat EL0 구현. 구조체는 SVC에서 synp_baha·검증한다. */
int 통신종단점만들기(int salgy_Maşgala,int 통신방식,int geçir_protokol) {
    return 결과검사(사용자호출(32,salgy_Maşgala,통신방식,geçir_protokol,0,0,0));
}
int BIND_salgy(int 종단,const struct 통신주소 *salgy,통신주소길이형 dowamlylyk_baha) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)salgy,dowamlylyk_baha,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *maglumat,size_t 개수,int saýlama_baha,const struct 통신주소 *salgy,통신주소길이형 dowamlylyk_baha) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)maglumat,개수,saýlama_baha,(uintptr_t)salgy,dowamlylyk_baha));
}
intptr_t 자료전문받기(int 종단,void *maglumat,size_t 개수,int saýlama_baha,struct 통신주소 *salgy,통신주소길이형 *dowamlylyk_baha) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)maglumat,개수,saýlama_baha,(uintptr_t)salgy,(uintptr_t)dowamlylyk_baha));
}
int 통신주소읽기(int 종단,struct 통신주소 *salgy,통신주소길이형 *dowamlylyk_baha) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)salgy,(uintptr_t)dowamlylyk_baha,0,0,0));
}
int Birikme_Tor(int 종단,const struct 통신주소 *salgy,통신주소길이형 dowamlylyk_baha) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)salgy,dowamlylyk_baha,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int kabul_et_tor_birikmesi(int 종단,struct 통신주소 *salgy,통신주소길이형 *dowamlylyk_baha) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)salgy,(uintptr_t)dowamlylyk_baha,0,0,0));
}

/* Faýl 함수도 독립된 한국어 FUNCTION_baha 심볼로 제공한다. */
int aç_faýl(const char *Ýol,int usul_reje,...) { return 결과검사(사용자호출(3,(uintptr_t)Ýol,usul_reje,0,0,0,0)); }
입출력결과형 파일자료읽기(int Faýl,void *maglumat,size_t 개수) { return 결과검사(사용자호출(2,Faýl,(uintptr_t)maglumat,개수,0,0,0)); }
입출력결과형 ýaz_faýl_maglumat(int Faýl,const void *maglumat,size_t 개수) { return 결과검사(사용자호출(1,Faýl,(uintptr_t)maglumat,개수,0,0,0)); }
int ýap_faýl(int Faýl) { return 결과검사(사용자호출(4,Faýl,0,0,0,0,0)); }
faýl_Süýşüriş_ýaz gözle_faýl(int Faýl,faýl_Süýşüriş_ýaz 거리,int 기준) { return 결과검사(사용자호출(5,Faýl,거리,기준,0,0,0)); }
int aýyr_faýl_girizmeklik_at(const char *Ýol) { return 결과검사(사용자호출(11,(uintptr_t)Ýol,0,0,0,0,0)); }
int köplük_faýl_dowamlylyk(int Faýl,faýl_Süýşüriş_ýaz Ululyk) { return 결과검사(사용자호출(10,Faýl,Ululyk,0,0,0,0)); }
int 파일저장확정(int Faýl) { return 결과검사(사용자호출(12,Faýl,0,0,0,0,0)); }
int faýl_ölçegi_üýtget(int Faýl) { return 결과검사(사용자호출(9,Faýl,0,0,0,0,0)); }

// 동일 한국어 헤더를 사용하는 별도 EL0 Bokgobadata. khenele_boleng 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int khoutu_ya_diphošo;
int *pk_errno_location(void) { return &khoutu_ya_diphošo; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { khoutu_ya_diphošo = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
faele_E_Šetšego_thaepa pk_lseek(int fd, faele_E_Šetšego_thaepa offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, faele_E_Šetšego_thaepa size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 kgonthe_data EL0 구현. 구조체는 SVC에서 kopiša_boleng·검증한다. */
int 통신종단점만들기(int atrese_Lapa,int 통신방식,int fetišetša_lenaneotshepedišo) {
    return 결과검사(사용자호출(32,atrese_Lapa,통신방식,fetišetša_lenaneotshepedišo,0,0,0));
}
int tlama_atrese(int 종단,const struct 통신주소 *atrese,통신주소길이형 botelele_boleng) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)atrese,botelele_boleng,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *data,size_t 개수,int kgetho_boleng,const struct 통신주소 *atrese,통신주소길이형 botelele_boleng) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)data,개수,kgetho_boleng,(uintptr_t)atrese,botelele_boleng));
}
intptr_t 자료전문받기(int 종단,void *data,size_t 개수,int kgetho_boleng,struct 통신주소 *atrese,통신주소길이형 *botelele_boleng) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)data,개수,kgetho_boleng,(uintptr_t)atrese,(uintptr_t)botelele_boleng));
}
int 통신주소읽기(int 종단,struct 통신주소 *atrese,통신주소길이형 *botelele_boleng) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)atrese,(uintptr_t)botelele_boleng,0,0,0));
}
int KGOKAGANYA_Netweke(int 종단,const struct 통신주소 *atrese,통신주소길이형 botelele_boleng) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)atrese,botelele_boleng,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int amogela_kgokaganyo_ya_dinetweke(int 종단,struct 통신주소 *atrese,통신주소길이형 *botelele_boleng) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)atrese,(uintptr_t)botelele_boleng,0,0,0));
}

/* Faele 함수도 독립된 한국어 TIRO_boleng 심볼로 제공한다. */
int bula_faele(const char *Tsejana,int mokgwa_mokgwa,...) { return 결과검사(사용자호출(3,(uintptr_t)Tsejana,mokgwa_mokgwa,0,0,0,0)); }
입출력결과형 파일자료읽기(int Faele,void *data,size_t 개수) { return 결과검사(사용자호출(2,Faele,(uintptr_t)data,개수,0,0,0)); }
입출력결과형 ngwala_faele_data(int Faele,const void *data,size_t 개수) { return 결과검사(사용자호출(1,Faele,(uintptr_t)data,개수,0,0,0)); }
int tswalela_faele(int Faele) { return 결과검사(사용자호출(4,Faele,0,0,0,0,0)); }
faele_E_Šetšego_thaepa nyaka_faele(int Faele,faele_E_Šetšego_thaepa 거리,int 기준) { return 결과검사(사용자호출(5,Faele,거리,기준,0,0,0)); }
int tloša_faele_go_tsenya_tshedimošo_leina(const char *Tsejana) { return 결과검사(사용자호출(11,(uintptr_t)Tsejana,0,0,0,0,0)); }
int sehlopha_faele_botelele(int Faele,faele_E_Šetšego_thaepa Bogolo) { return 결과검사(사용자호출(10,Faele,Bogolo,0,0,0,0)); }
int 파일저장확정(int Faele) { return 결과검사(사용자호출(12,Faele,0,0,0,0,0)); }
int faele_bogolo(int Faele) { return 결과검사(사용자호출(9,Faele,0,0,0,0,0)); }

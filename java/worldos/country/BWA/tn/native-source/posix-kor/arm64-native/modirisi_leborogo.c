// 동일 한국어 헤더를 사용하는 별도 EL0 laeborari. Khenele_Boleng 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int khouto_ya_phoso;
int *pk_errno_location(void) { return &khouto_ya_phoso; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { khouto_ya_phoso = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
faele_Baya_ka_Tekatekanyo_tlanya pk_lseek(int fd, faele_Baya_ka_Tekatekanyo_tlanya offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, faele_Baya_ka_Tekatekanyo_tlanya size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 tota_tshedimosetso EL0 구현. 구조체는 SVC에서 leloko_Boleng·검증한다. */
int 통신종단점만들기(int aterese_Lelapa,int 통신방식,int fudusa_Porotokholo) {
    return 결과검사(사용자호출(32,aterese_Lelapa,통신방식,fudusa_Porotokholo,0,0,0));
}
int BIND_aterese(int 종단,const struct 통신주소 *aterese,통신주소길이형 boleele_Boleng) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)aterese,boleele_Boleng,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *tshedimosetso,size_t 개수,int tlhopho_Boleng,const struct 통신주소 *aterese,통신주소길이형 boleele_Boleng) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)tshedimosetso,개수,tlhopho_Boleng,(uintptr_t)aterese,boleele_Boleng));
}
intptr_t 자료전문받기(int 종단,void *tshedimosetso,size_t 개수,int tlhopho_Boleng,struct 통신주소 *aterese,통신주소길이형 *boleele_Boleng) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)tshedimosetso,개수,tlhopho_Boleng,(uintptr_t)aterese,(uintptr_t)boleele_Boleng));
}
int 통신주소읽기(int 종단,struct 통신주소 *aterese,통신주소길이형 *boleele_Boleng) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)aterese,(uintptr_t)boleele_Boleng,0,0,0));
}
int Golaganya_Neteweke(int 종단,const struct 통신주소 *aterese,통신주소길이형 boleele_Boleng) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)aterese,boleele_Boleng,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int amogela_kgolagano_ya_neteweke(int 종단,struct 통신주소 *aterese,통신주소길이형 *boleele_Boleng) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)aterese,(uintptr_t)boleele_Boleng,0,0,0));
}

/* faele 함수도 독립된 한국어 TIRISO_Boleng 심볼로 제공한다. */
int bula_faele(const char *tsela,int mokgwa_mokgwa,...) { return 결과검사(사용자호출(3,(uintptr_t)tsela,mokgwa_mokgwa,0,0,0,0)); }
입출력결과형 파일자료읽기(int faele,void *tshedimosetso,size_t 개수) { return 결과검사(사용자호출(2,faele,(uintptr_t)tshedimosetso,개수,0,0,0)); }
입출력결과형 kwala_faele_tshedimosetso(int faele,const void *tshedimosetso,size_t 개수) { return 결과검사(사용자호출(1,faele,(uintptr_t)tshedimosetso,개수,0,0,0)); }
int tswala_faele(int faele) { return 결과검사(사용자호출(4,faele,0,0,0,0,0)); }
faele_Baya_ka_Tekatekanyo_tlanya batla_faele(int faele,faele_Baya_ka_Tekatekanyo_tlanya 거리,int 기준) { return 결과검사(사용자호출(5,faele,거리,기준,0,0,0)); }
int tlosa_faele_tsenyo_leina(const char *tsela) { return 결과검사(사용자호출(11,(uintptr_t)tsela,0,0,0,0,0)); }
int sete_faele_boleele(int faele,faele_Baya_ka_Tekatekanyo_tlanya lekanya) { return 결과검사(사용자호출(10,faele,lekanya,0,0,0,0)); }
int 파일저장확정(int faele) { return 결과검사(사용자호출(12,faele,0,0,0,0,0)); }
int faele_lekanya(int faele) { return 결과검사(사용자호출(9,faele,0,0,0,0,0)); }

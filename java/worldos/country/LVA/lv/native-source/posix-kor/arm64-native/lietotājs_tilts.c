// 동일 Latviešu 헤더를 사용하는 별도 EL0 bibliotēka. kodols_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kļūdas_kods;
int *pk_errno_location(void) { return &kļūdas_kods; }
static intptr_t 결과검사(intptr_t mērs) { if (mērs < 0) { kļūdas_kods = -mērs; return -1; } return mērs; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fails_Nobīde_TYPE pk_lseek(int fd, Fails_Nobīde_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fails_Nobīde_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Latviešu 공개 함수의 faktisks_dati EL0 구현. 구조체는 SVC에서 kopēt_VALUE·검증한다. */
int atvērt_dalībnieks(int adrese_saime,int 통신방식,int nodot_protokols) {
    return 결과검사(사용자호출(32,adrese_saime,통신방식,nodot_protokols,0,0,0));
}
int BIND_adrese(int dalībnieks,const struct 통신주소 *adrese,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,dalībnieks,(uintptr_t)adrese,길이,0,0,0));
}
intptr_t sūtīt_datogramma_dati(int dalībnieks,const void *dati,size_t krājums_COUNT,int atlase_VALUE,const struct 통신주소 *adrese,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,dalībnieks,(uintptr_t)dati,krājums_COUNT,atlase_VALUE,(uintptr_t)adrese,길이));
}
intptr_t saņemt_datogramma_dati(int dalībnieks,void *dati,size_t krājums_COUNT,int atlase_VALUE,struct 통신주소 *adrese,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,dalībnieks,(uintptr_t)dati,krājums_COUNT,atlase_VALUE,(uintptr_t)adrese,(uintptr_t)길이));
}
int 통신주소읽기(int dalībnieks,struct 통신주소 *adrese,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,dalībnieks,(uintptr_t)adrese,(uintptr_t)길이,0,0,0));
}
int saziņa_tīkls(int dalībnieks,const struct 통신주소 *adrese,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,dalībnieks,(uintptr_t)adrese,길이,0,0,0));
}
int 통신연결기다리기(int dalībnieks,int Gaidu_COUNT) {
    return 결과검사(사용자호출(38,dalībnieks,Gaidu_COUNT,0,0,0,0));
}
int akceptēt_tīkla_savienojums(int dalībnieks,struct 통신주소 *adrese,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,dalībnieks,(uintptr_t)adrese,(uintptr_t)길이,0,0,0));
}

/* Fails 함수도 독립된 Latviešu FUNCTION_VALUE 심볼로 제공한다. */
int atvērt_Fails(const char *CEĻŠ,int metode_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)CEĻŠ,metode_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fails,void *dati,size_t krājums_COUNT) { return 결과검사(사용자호출(2,Fails,(uintptr_t)dati,krājums_COUNT,0,0,0)); }
입출력결과형 rakstīšana_Fails_dati(int Fails,const void *dati,size_t krājums_COUNT) { return 결과검사(사용자호출(1,Fails,(uintptr_t)dati,krājums_COUNT,0,0,0)); }
int Aizvērt_Fails(int Fails) { return 결과검사(사용자호출(4,Fails,0,0,0,0,0)); }
Fails_Nobīde_TYPE meklēt_Fails(int Fails,Fails_Nobīde_TYPE 거리,int Project_sakne) { return 결과검사(사용자호출(5,Fails,거리,Project_sakne,0,0,0)); }
int noņemt_Fails_ievade_nosaukums(const char *CEĻŠ) { return 결과검사(사용자호출(11,(uintptr_t)CEĻŠ,0,0,0,0,0)); }
int 파일길이정하기(int Fails,Fails_Nobīde_TYPE Izmērs) { return 결과검사(사용자호출(10,Fails,Izmērs,0,0,0,0)); }
int izpilde_failu_krātuve(int Fails) { return 결과검사(사용자호출(12,Fails,0,0,0,0,0)); }
int faila_lielums(int Fails) { return 결과검사(사용자호출(9,Fails,0,0,0,0,0)); }

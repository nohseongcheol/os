// 동일 Eesti 헤더를 사용하는 별도 EL0 teek. tuum_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int tõrkekood;
int *pk_errno_location(void) { return &tõrkekood; }
static intptr_t 결과검사(intptr_t TULEMUS) { if (TULEMUS < 0) { tõrkekood = -TULEMUS; return -1; } return TULEMUS; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fail_nihe_TYPE pk_lseek(int fd, Fail_nihe_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fail_nihe_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Eesti 공개 함수의 tegelik_andmed EL0 구현. 구조체는 SVC에서 eksemplar_VALUE·검증한다. */
int avama_osaleja(int ADDRESS_Pere,int 통신방식,int Edasta_protokoll) {
    return 결과검사(사용자호출(32,ADDRESS_Pere,통신방식,Edasta_protokoll,0,0,0));
}
int BIND_ADDRESS(int osaleja,const struct 통신주소 *ADDRESS,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,osaleja,(uintptr_t)ADDRESS,길이,0,0,0));
}
intptr_t saatma_datagramm_andmed(int osaleja,const void *andmed,size_t kaup_COUNT,int valim_VALUE,const struct 통신주소 *ADDRESS,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,osaleja,(uintptr_t)andmed,kaup_COUNT,valim_VALUE,(uintptr_t)ADDRESS,길이));
}
intptr_t saama_datagramm_andmed(int osaleja,void *andmed,size_t kaup_COUNT,int valim_VALUE,struct 통신주소 *ADDRESS,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,osaleja,(uintptr_t)andmed,kaup_COUNT,valim_VALUE,(uintptr_t)ADDRESS,(uintptr_t)길이));
}
int 통신주소읽기(int osaleja,struct 통신주소 *ADDRESS,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,osaleja,(uintptr_t)ADDRESS,(uintptr_t)길이,0,0,0));
}
int Ühenda_võrk(int osaleja,const struct 통신주소 *ADDRESS,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,osaleja,(uintptr_t)ADDRESS,길이,0,0,0));
}
int 통신연결기다리기(int osaleja,int Ootamine_COUNT) {
    return 결과검사(사용자호출(38,osaleja,Ootamine_COUNT,0,0,0,0));
}
int aktsepteerima_võrguühendus(int osaleja,struct 통신주소 *ADDRESS,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,osaleja,(uintptr_t)ADDRESS,(uintptr_t)길이,0,0,0));
}

/* Fail 함수도 독립된 Eesti FUNCTION_VALUE 심볼로 제공한다. */
int avama_Fail(const char *RADA,int meetod_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)RADA,meetod_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fail,void *andmed,size_t kaup_COUNT) { return 결과검사(사용자호출(2,Fail,(uintptr_t)andmed,kaup_COUNT,0,0,0)); }
입출력결과형 kirjutamine_Fail_andmed(int Fail,const void *andmed,size_t kaup_COUNT) { return 결과검사(사용자호출(1,Fail,(uintptr_t)andmed,kaup_COUNT,0,0,0)); }
int Sule_Fail(int Fail) { return 결과검사(사용자호출(4,Fail,0,0,0,0,0)); }
Fail_nihe_TYPE otsima_Fail(int Fail,Fail_nihe_TYPE 거리,int Project_juur) { return 결과검사(사용자호출(5,Fail,거리,Project_juur,0,0,0)); }
int eemaldama_Fail_kirje_nimetus(const char *RADA) { return 결과검사(사용자호출(11,(uintptr_t)RADA,0,0,0,0,0)); }
int 파일길이정하기(int Fail,Fail_nihe_TYPE Suurus) { return 결과검사(사용자호출(10,Fail,Suurus,0,0,0,0)); }
int kinnitamine_failisalvestusruum(int Fail) { return 결과검사(사용자호출(12,Fail,0,0,0,0,0)); }
int faili_maht(int Fail) { return 결과검사(사용자호출(9,Fail,0,0,0,0,0)); }

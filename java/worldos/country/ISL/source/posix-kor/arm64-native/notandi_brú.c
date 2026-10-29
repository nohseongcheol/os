// 동일 Íslenska 헤더를 사용하는 별도 EL0 safn. kjarni_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int villukóði;
int *pk_errno_location(void) { return &villukóði; }
static intptr_t 결과검사(intptr_t NIÐURSTAÐA) { if (NIÐURSTAÐA < 0) { villukóði = -NIÐURSTAÐA; return -1; } return NIÐURSTAÐA; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
skrá_OFFSET_TYPE pk_lseek(int fd, skrá_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, skrá_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Íslenska 공개 함수의 raun_gögn EL0 구현. 구조체는 SVC에서 afrita_VALUE·검증한다. */
int stofna_endastöð(int slóð_Fjölskylda,int 통신방식,int flytja_samskiptaregla) {
    return 결과검사(사용자호출(32,slóð_Fjölskylda,통신방식,flytja_samskiptaregla,0,0,0));
}
int BIND_slóð(int endastöð,const struct 통신주소 *slóð,통신주소길이형 lengd_VALUE) {
    return 결과검사(사용자호출(33,endastöð,(uintptr_t)slóð,lengd_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int endastöð,const void *gögn,size_t vara_COUNT,int val_VALUE,const struct 통신주소 *slóð,통신주소길이형 lengd_VALUE) {
    return 결과검사(사용자호출(34,endastöð,(uintptr_t)gögn,vara_COUNT,val_VALUE,(uintptr_t)slóð,lengd_VALUE));
}
intptr_t 자료전문받기(int endastöð,void *gögn,size_t vara_COUNT,int val_VALUE,struct 통신주소 *slóð,통신주소길이형 *lengd_VALUE) {
    return 결과검사(사용자호출(35,endastöð,(uintptr_t)gögn,vara_COUNT,val_VALUE,(uintptr_t)slóð,(uintptr_t)lengd_VALUE));
}
int 통신주소읽기(int endastöð,struct 통신주소 *slóð,통신주소길이형 *lengd_VALUE) {
    return 결과검사(사용자호출(36,endastöð,(uintptr_t)slóð,(uintptr_t)lengd_VALUE,0,0,0));
}
int TENGJA_Net(int endastöð,const struct 통신주소 *slóð,통신주소길이형 lengd_VALUE) {
    return 결과검사(사용자호출(37,endastöð,(uintptr_t)slóð,lengd_VALUE,0,0,0));
}
int 통신연결기다리기(int endastöð,int Bíður_COUNT) {
    return 결과검사(사용자호출(38,endastöð,Bíður_COUNT,0,0,0,0));
}
int samþykkja_nettenging(int endastöð,struct 통신주소 *slóð,통신주소길이형 *lengd_VALUE) {
    return 결과검사(사용자호출(39,endastöð,(uintptr_t)slóð,(uintptr_t)lengd_VALUE,0,0,0));
}

/* Skrá 함수도 독립된 Íslenska fall_VALUE 심볼로 제공한다. */
int opið_skrá(const char *SLÓÐ,int aðferð_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)SLÓÐ,aðferð_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Skrá,void *gögn,size_t vara_COUNT) { return 결과검사(사용자호출(2,Skrá,(uintptr_t)gögn,vara_COUNT,0,0,0)); }
입출력결과형 skrifa_skrá_gögn(int Skrá,const void *gögn,size_t vara_COUNT) { return 결과검사(사용자호출(1,Skrá,(uintptr_t)gögn,vara_COUNT,0,0,0)); }
int loka_skrá(int Skrá) { return 결과검사(사용자호출(4,Skrá,0,0,0,0,0)); }
skrá_OFFSET_TYPE leita_skrá(int Skrá,skrá_OFFSET_TYPE 거리,int verk_rót) { return 결과검사(사용자호출(5,Skrá,거리,verk_rót,0,0,0)); }
int fjarlægja_skrá_færsla_heiti(const char *SLÓÐ) { return 결과검사(사용자호출(11,(uintptr_t)SLÓÐ,0,0,0,0,0)); }
int sett_skrá_lengd(int Skrá,skrá_OFFSET_TYPE Stærð) { return 결과검사(사용자호출(10,Skrá,Stærð,0,0,0,0)); }
int 파일저장확정(int Skrá) { return 결과검사(사용자호출(12,Skrá,0,0,0,0,0)); }
int skrá_breyta_stærð(int Skrá) { return 결과검사(사용자호출(9,Skrá,0,0,0,0,0)); }

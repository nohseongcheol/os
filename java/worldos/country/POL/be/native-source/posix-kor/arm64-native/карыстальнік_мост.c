// 동일 한국어 헤더를 사용하는 별도 EL0 бібліятэка. ядро_значэнне 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int памылка_код;
int *pk_errno_location(void) { return &памылка_код; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { памылка_код = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
файл_Зрух_друкаваць pk_lseek(int fd, файл_Зрух_друкаваць offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, файл_Зрух_друкаваць size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 фактычны_дадзеныя EL0 구현. 구조체는 SVC에서 капіяваць_значэнне·검증한다. */
int 통신종단점만들기(int адрас_Сям_я,int 통신방식,int перанос_пратакол) {
    return 결과검사(사용자호출(32,адрас_Сям_я,통신방식,перанос_пратакол,0,0,0));
}
int прывязаць_адрас(int 종단,const struct 통신주소 *адрас,통신주소길이형 даўжыня_значэнне) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)адрас,даўжыня_значэнне,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *дадзеныя,size_t 개수,int вылучанае_значэнне,const struct 통신주소 *адрас,통신주소길이형 даўжыня_значэнне) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)дадзеныя,개수,вылучанае_значэнне,(uintptr_t)адрас,даўжыня_значэнне));
}
intptr_t 자료전문받기(int 종단,void *дадзеныя,size_t 개수,int вылучанае_значэнне,struct 통신주소 *адрас,통신주소길이형 *даўжыня_значэнне) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)дадзеныя,개수,вылучанае_значэнне,(uintptr_t)адрас,(uintptr_t)даўжыня_значэнне));
}
int 통신주소읽기(int 종단,struct 통신주소 *адрас,통신주소길이형 *даўжыня_значэнне) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)адрас,(uintptr_t)даўжыня_значэнне,0,0,0));
}
int злучаць_Сетка(int 종단,const struct 통신주소 *адрас,통신주소길이형 даўжыня_значэнне) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)адрас,даўжыня_значэнне,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int прыняць_сеткавае_злучэнне(int 종단,struct 통신주소 *адрас,통신주소길이형 *даўжыня_значэнне) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)адрас,(uintptr_t)даўжыня_значэнне,0,0,0));
}

/* Файл 함수도 독립된 한국어 функцыя_значэнне 심볼로 제공한다. */
int адкрыць_файл(const char *ШЛЯХ,int спосаб_рэжым,...) { return 결과검사(사용자호출(3,(uintptr_t)ШЛЯХ,спосаб_рэжым,0,0,0,0)); }
입출력결과형 파일자료읽기(int Файл,void *дадзеныя,size_t 개수) { return 결과검사(사용자호출(2,Файл,(uintptr_t)дадзеныя,개수,0,0,0)); }
입출력결과형 напісаць_файл_дадзеныя(int Файл,const void *дадзеныя,size_t 개수) { return 결과검사(사용자호출(1,Файл,(uintptr_t)дадзеныя,개수,0,0,0)); }
int закрыць_файл(int Файл) { return 결과검사(사용자호출(4,Файл,0,0,0,0,0)); }
файл_Зрух_друкаваць шукаць_файл(int Файл,файл_Зрух_друкаваць 거리,int 기준) { return 결과검사(사용자호출(5,Файл,거리,기준,0,0,0)); }
int выдаліць_файл_увядзенне_імя(const char *ШЛЯХ) { return 결과검사(사용자호출(11,(uintptr_t)ШЛЯХ,0,0,0,0,0)); }
int набор_файл_даўжыня(int Файл,файл_Зрух_друкаваць Памер) { return 결과검사(사용자호출(10,Файл,Памер,0,0,0,0)); }
int 파일저장확정(int Файл) { return 결과검사(사용자호출(12,Файл,0,0,0,0,0)); }
int файл_памер(int Файл) { return 결과검사(사용자호출(9,Файл,0,0,0,0,0)); }

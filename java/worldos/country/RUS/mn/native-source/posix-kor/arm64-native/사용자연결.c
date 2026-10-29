// 동일 Монгол 헤더를 사용하는 별도 EL0 сан. кернел_утга 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int алдааны_код;
int *pk_errno_location(void) { return &алдааны_код; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { алдааны_код = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
файл_Оффсет_бичих pk_lseek(int fd, файл_Оффсет_бичих offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, файл_Оффсет_бичих size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Монгол 공개 함수의 бодит_өгөгдөл EL0 구현. 구조체는 SVC에서 хуулах_утга·검증한다. */
int 통신종단점만들기(int хаяг_Гэр_бүл,int 통신방식,int дамжуулах_протокол) {
    return 결과검사(사용자호출(32,хаяг_Гэр_бүл,통신방식,дамжуулах_протокол,0,0,0));
}
int холбох_хаяг(int 종단,const struct 통신주소 *хаяг,통신주소길이형 урт_утга) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)хаяг,урт_утга,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *өгөгдөл,size_t 개수,int сонгосон_хэсэг_утга,const struct 통신주소 *хаяг,통신주소길이형 урт_утга) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)өгөгдөл,개수,сонгосон_хэсэг_утга,(uintptr_t)хаяг,урт_утга));
}
intptr_t 자료전문받기(int 종단,void *өгөгдөл,size_t 개수,int сонгосон_хэсэг_утга,struct 통신주소 *хаяг,통신주소길이형 *урт_утга) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)өгөгдөл,개수,сонгосон_хэсэг_утга,(uintptr_t)хаяг,(uintptr_t)урт_утга));
}
int 통신주소읽기(int 종단,struct 통신주소 *хаяг,통신주소길이형 *урт_утга) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)хаяг,(uintptr_t)урт_утга,0,0,0));
}
int холбох_Сүлжээ(int 종단,const struct 통신주소 *хаяг,통신주소길이형 урт_утга) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)хаяг,урт_утга,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int зөвшөөрөх_сүлжээний_холболт(int 종단,struct 통신주소 *хаяг,통신주소길이형 *урт_утга) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)хаяг,(uintptr_t)урт_утга,0,0,0));
}

/* Файл 함수도 독립된 Монгол ФУНКЦ_утга 심볼로 제공한다. */
int нээх_файл(const char *ЗАМ,int арга_горим,...) { return 결과검사(사용자호출(3,(uintptr_t)ЗАМ,арга_горим,0,0,0,0)); }
입출력결과형 파일자료읽기(int Файл,void *өгөгдөл,size_t 개수) { return 결과검사(사용자호출(2,Файл,(uintptr_t)өгөгдөл,개수,0,0,0)); }
입출력결과형 бичих_файл_өгөгдөл(int Файл,const void *өгөгдөл,size_t 개수) { return 결과검사(사용자호출(1,Файл,(uintptr_t)өгөгдөл,개수,0,0,0)); }
int хаах_файл(int Файл) { return 결과검사(사용자호출(4,Файл,0,0,0,0,0)); }
файл_Оффсет_бичих хайх_файл(int Файл,файл_Оффсет_бичих 거리,int 기준) { return 결과검사(사용자호출(5,Файл,거리,기준,0,0,0)); }
int арилгах_файл_оролт_нэр(const char *ЗАМ) { return 결과검사(사용자호출(11,(uintptr_t)ЗАМ,0,0,0,0,0)); }
int багц_файл_урт(int Файл,файл_Оффсет_бичих Хэмжээ) { return 결과검사(사용자호출(10,Файл,Хэмжээ,0,0,0,0)); }
int 파일저장확정(int Файл) { return 결과검사(사용자호출(12,Файл,0,0,0,0,0)); }
int файл_хэмжээ(int Файл) { return 결과검사(사용자호출(9,Файл,0,0,0,0,0)); }

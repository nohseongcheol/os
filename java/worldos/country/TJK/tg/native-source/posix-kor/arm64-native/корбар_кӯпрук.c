// 동일 한국어 헤더를 사용하는 별도 EL0 китобхона. ҳаста_қимат 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int 오류값;
int *pk_errno_location(void) { return &오류값; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { 오류값 = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
файл_Интиқолшавӣ_навъ pk_lseek(int fd, файл_Интиқолшавӣ_навъ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, файл_Интиқолшавӣ_навъ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 воқеӣ_иттилоот EL0 구현. 구조체는 SVC에서 ҳолат_қимат·검증한다. */
int 통신종단점만들기(int суроға_Оила,int 통신방식,int интиқол_протокол) {
    return 결과검사(사용자호출(32,суроға_Оила,통신방식,интиқол_протокол,0,0,0));
}
int иртибот_додан_суроға(int 종단,const struct 통신주소 *суроға,통신주소길이형 дарозӣ_қимат) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)суроға,дарозӣ_қимат,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *иттилоот,size_t 개수,int интихоб_қимат,const struct 통신주소 *суроға,통신주소길이형 дарозӣ_қимат) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)иттилоот,개수,интихоб_қимат,(uintptr_t)суроға,дарозӣ_қимат));
}
intptr_t 자료전문받기(int 종단,void *иттилоот,size_t 개수,int интихоб_қимат,struct 통신주소 *суроға,통신주소길이형 *дарозӣ_қимат) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)иттилоот,개수,интихоб_қимат,(uintptr_t)суроға,(uintptr_t)дарозӣ_қимат));
}
int 통신주소읽기(int 종단,struct 통신주소 *суроға,통신주소길이형 *дарозӣ_қимат) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)суроға,(uintptr_t)дарозӣ_қимат,0,0,0));
}
int ПАЙВАСТ_Шабака(int 종단,const struct 통신주소 *суроға,통신주소길이형 дарозӣ_қимат) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)суроға,дарозӣ_қимат,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int қабул_кардан_пайвасти_шабака(int 종단,struct 통신주소 *суроға,통신주소길이형 *дарозӣ_қимат) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)суроға,(uintptr_t)дарозӣ_қимат,0,0,0));
}

/* Файл 함수도 독립된 한국어 функсия_қимат 심볼로 제공한다. */
int кушодан_файл(const char *масир,int сабк_ҳолат,...) { return 결과검사(사용자호출(3,(uintptr_t)масир,сабк_ҳолат,0,0,0,0)); }
입출력결과형 파일자료읽기(int Файл,void *иттилоот,size_t 개수) { return 결과검사(사용자호출(2,Файл,(uintptr_t)иттилоот,개수,0,0,0)); }
입출력결과형 навиштан_файл_иттилоот(int Файл,const void *иттилоот,size_t 개수) { return 결과검사(사용자호출(1,Файл,(uintptr_t)иттилоот,개수,0,0,0)); }
int пӯшидан_файл(int Файл) { return 결과검사(사용자호출(4,Файл,0,0,0,0,0)); }
файл_Интиқолшавӣ_навъ ҷустан_файл(int Файл,файл_Интиқолшавӣ_навъ 거리,int 기준) { return 결과검사(사용자호출(5,Файл,거리,기준,0,0,0)); }
int тоза_кардан_файл_ворида_ном(const char *масир) { return 결과검사(사용자호출(11,(uintptr_t)масир,0,0,0,0,0)); }
int маҷмуъ_файл_дарозӣ(int Файл,файл_Интиқолшавӣ_навъ андоза_кардан) { return 결과검사(사용자호출(10,Файл,андоза_кардан,0,0,0,0)); }
int 파일저장확정(int Файл) { return 결과검사(사용자호출(12,Файл,0,0,0,0,0)); }
int файл_андоза_кардан(int Файл) { return 결과검사(사용자호출(9,Файл,0,0,0,0,0)); }

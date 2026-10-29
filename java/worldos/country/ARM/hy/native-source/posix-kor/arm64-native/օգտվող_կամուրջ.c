// 동일 한국어 헤더를 사용하는 별도 EL0 դարան. միջուկ_արժեք 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int սխալի_կոդ;
int *pk_errno_location(void) { return &սխալի_կոդ; }
static intptr_t 결과검사(intptr_t չափ) { if (չափ < 0) { սխալի_կոդ = -չափ; return -1; } return չափ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
նիշք_Տեղաշարժում_մուտքագրել pk_lseek(int fd, նիշք_Տեղաշարժում_մուտքագրել offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, նիշք_Տեղաշարժում_մուտքագրել size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 իրական_տվյալ EL0 구현. 구조체는 SVC에서 պատճեն_արժեք·검증한다. */
int 통신종단점만들기(int հասցե_Ընտանիք,int 통신방식,int փոխանցել_հաղորդակարգ) {
    return 결과검사(사용자호출(32,հասցե_Ընտանիք,통신방식,փոխանցել_հաղորդակարգ,0,0,0));
}
int կապել_հասցե(int 종단,const struct 통신주소 *հասցե,통신주소길이형 տեւողություն_արժեք) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)հասցե,տեւողություն_արժեք,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *տվյալ,size_t 개수,int ընտրվածք_արժեք,const struct 통신주소 *հասցե,통신주소길이형 տեւողություն_արժեք) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)տվյալ,개수,ընտրվածք_արժեք,(uintptr_t)հասցե,տեւողություն_արժեք));
}
intptr_t 자료전문받기(int 종단,void *տվյալ,size_t 개수,int ընտրվածք_արժեք,struct 통신주소 *հասցե,통신주소길이형 *տեւողություն_արժեք) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)տվյալ,개수,ընտրվածք_արժեք,(uintptr_t)հասցե,(uintptr_t)տեւողություն_արժեք));
}
int 통신주소읽기(int 종단,struct 통신주소 *հասցե,통신주소길이형 *տեւողություն_արժեք) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)հասցե,(uintptr_t)տեւողություն_արժեք,0,0,0));
}
int Կապակցել_Ցանց(int 종단,const struct 통신주소 *հասցե,통신주소길이형 տեւողություն_արժեք) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)հասցե,տեւողություն_արժեք,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ընդունել_ցանցային_կապակցում(int 종단,struct 통신주소 *հասցե,통신주소길이형 *տեւողություն_արժեք) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)հասցե,(uintptr_t)տեւողություն_արժեք,0,0,0));
}

/* Ֆայլ 함수도 독립된 한국어 ՖՈՒՆԿՑԻԱ_արժեք 심볼로 제공한다. */
int բացել_նիշք(const char *Ճանապարհ,int եղանակ_կերպ,...) { return 결과검사(사용자호출(3,(uintptr_t)Ճանապարհ,եղանակ_կերպ,0,0,0,0)); }
입출력결과형 파일자료읽기(int Ֆայլ,void *տվյալ,size_t 개수) { return 결과검사(사용자호출(2,Ֆայլ,(uintptr_t)տվյալ,개수,0,0,0)); }
입출력결과형 գրել_նիշք_տվյալ(int Ֆայլ,const void *տվյալ,size_t 개수) { return 결과검사(사용자호출(1,Ֆայլ,(uintptr_t)տվյալ,개수,0,0,0)); }
int փակել_նիշք(int Ֆայլ) { return 결과검사(사용자호출(4,Ֆայլ,0,0,0,0,0)); }
նիշք_Տեղաշարժում_մուտքագրել որոնել_նիշք(int Ֆայլ,նիշք_Տեղաշարժում_մուտքագրել 거리,int արձակել_արմատ) { return 결과검사(사용자호출(5,Ֆայլ,거리,արձակել_արմատ,0,0,0)); }
int հեռացնել_նիշք_մուտքագրում_անուն(const char *Ճանապարհ) { return 결과검사(사용자호출(11,(uintptr_t)Ճանապարհ,0,0,0,0,0)); }
int կազմ_նիշք_տեւողություն(int Ֆայլ,նիշք_Տեղաշարժում_մուտքագրել Չափս) { return 결과검사(사용자호출(10,Ֆայլ,Չափս,0,0,0,0)); }
int 파일저장확정(int Ֆայլ) { return 결과검사(사용자호출(12,Ֆայլ,0,0,0,0,0)); }
int նիշք_չափափոխել(int Ֆայլ) { return 결과검사(사용자호출(9,Ֆայլ,0,0,0,0,0)); }

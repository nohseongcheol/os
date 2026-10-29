// 동일 ગુજરાતી 헤더를 사용하는 별도 EL0 લાઇબ્રેરી. કર્નેલ_મૂલ્ય 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ભુલ_કોડ;
int *pk_errno_location(void) { return &ભુલ_કોડ; }
static intptr_t 결과검사(intptr_t પરિમાણ) { if (પરિમાણ < 0) { ભુલ_કોડ = -પરિમાણ; return -1; } return પરિમાણ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ફાઇલ_ઑફસેટ_લખો pk_lseek(int fd, ફાઇલ_ઑફસેટ_લખો offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ફાઇલ_ઑફસેટ_લખો size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* ગુજરાતી 공개 함수의 વાસ્તવિક_ડેટા EL0 구현. 구조체는 SVC에서 ઉદાહરણ_મૂલ્ય·검증한다. */
int 통신종단점만들기(int સરનામું_કુટુંબ,int 통신방식,int સ્થાનાંતર_પ્રોટોકૉલ) {
    return 결과검사(사용자호출(32,સરનામું_કુટુંબ,통신방식,સ્થાનાંતર_પ્રોટોકૉલ,0,0,0));
}
int બાઇંડ_કરો_સરનામું(int 종단,const struct 통신주소 *સરનામું,통신주소길이형 લંબાઈ_મૂલ્ય) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)સરનામું,લંબાઈ_મૂલ્ય,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ડેટા,size_t 개수,int ચયન_મૂલ્ય,const struct 통신주소 *સરનામું,통신주소길이형 લંબાઈ_મૂલ્ય) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ડેટા,개수,ચયન_મૂલ્ય,(uintptr_t)સરનામું,લંબાઈ_મૂલ્ય));
}
intptr_t 자료전문받기(int 종단,void *ડેટા,size_t 개수,int ચયન_મૂલ્ય,struct 통신주소 *સરનામું,통신주소길이형 *લંબાઈ_મૂલ્ય) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ડેટા,개수,ચયન_મૂલ્ય,(uintptr_t)સરનામું,(uintptr_t)લંબાઈ_મૂલ્ય));
}
int 통신주소읽기(int 종단,struct 통신주소 *સરનામું,통신주소길이형 *લંબાઈ_મૂલ્ય) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)સરનામું,(uintptr_t)લંબાઈ_મૂલ્ય,0,0,0));
}
int કનેક્ટ_નેટવર્ક(int 종단,const struct 통신주소 *સરનામું,통신주소길이형 લંબાઈ_મૂલ્ય) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)સરનામું,લંબાઈ_મૂલ્ય,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int સ્વીકારો_નેટવર્ક_કનેક્શન(int 종단,struct 통신주소 *સરનામું,통신주소길이형 *લંબાઈ_મૂલ્ય) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)સરનામું,(uintptr_t)લંબાઈ_મૂલ્ય,0,0,0));
}

/* ફાઈલ 함수도 독립된 ગુજરાતી ફંક્શંસ_મૂલ્ય 심볼로 제공한다. */
int બનાવો_ફાઇલ(const char *પથ,int પદ્ધતિ_મોડ,...) { return 결과검사(사용자호출(3,(uintptr_t)પથ,પદ્ધતિ_મોડ,0,0,0,0)); }
입출력결과형 파일자료읽기(int ફાઈલ,void *ડેટા,size_t 개수) { return 결과검사(사용자호출(2,ફાઈલ,(uintptr_t)ડેટા,개수,0,0,0)); }
입출력결과형 લખો_ફાઇલ_ડેટા(int ફાઈલ,const void *ડેટા,size_t 개수) { return 결과검사(사용자호출(1,ફાઈલ,(uintptr_t)ડેટા,개수,0,0,0)); }
int બંધ_કરો_ફાઇલ(int ફાઈલ) { return 결과검사(사용자호출(4,ફાઈલ,0,0,0,0,0)); }
ફાઇલ_ઑફસેટ_લખો સીક_ફાઇલ(int ફાઈલ,ફાઇલ_ઑફસેટ_લખો 거리,int પ્રોજેક્ટ_રૂટ) { return 결과검사(사용자호출(5,ફાઈલ,거리,પ્રોજેક્ટ_રૂટ,0,0,0)); }
int કાઢી_નાંખો_ફાઇલ_પ્રવેશ_નામ(const char *પથ) { return 결과검사(사용자호출(11,(uintptr_t)પથ,0,0,0,0,0)); }
int સેટ_ફાઇલ_લંબાઈ(int ફાઈલ,ફાઇલ_ઑફસેટ_લખો માપ) { return 결과검사(사용자호출(10,ફાઈલ,માપ,0,0,0,0)); }
int 파일저장확정(int ફાઈલ) { return 결과검사(사용자호출(12,ફાઈલ,0,0,0,0,0)); }
int ફાઇલ_આકાર(int ફાઈલ) { return 결과검사(사용자호출(9,ફાઈલ,0,0,0,0,0)); }

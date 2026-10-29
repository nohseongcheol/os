// 동일 한국어 헤더를 사용하는 별도 EL0 لائبريري. ڪرنل_قدر 직접 호출판과 혼합 금지.
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
فائل_آف_سيٽ_قسم pk_lseek(int fd, فائل_آف_سيٽ_قسم offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, فائل_آف_سيٽ_قسم size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 اصلي_ڪوائف EL0 구현. 구조체는 SVC에서 نقل_قدر·검증한다. */
int 통신종단점만들기(int پتو_خاندان,int 통신방식,int منتقلي_پروٽوڪو0ل) {
    return 결과검사(사용자호출(32,پتو_خاندان,통신방식,منتقلي_پروٽوڪو0ل,0,0,0));
}
int ٻڌو_پتو(int 종단,const struct 통신주소 *پتو,통신주소길이형 لمبائي_قدر) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)پتو,لمبائي_قدر,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ڪوائف,size_t 개수,int چونڊ_قدر,const struct 통신주소 *پتو,통신주소길이형 لمبائي_قدر) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ڪوائف,개수,چونڊ_قدر,(uintptr_t)پتو,لمبائي_قدر));
}
intptr_t 자료전문받기(int 종단,void *ڪوائف,size_t 개수,int چونڊ_قدر,struct 통신주소 *پتو,통신주소길이형 *لمبائي_قدر) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ڪوائف,개수,چونڊ_قدر,(uintptr_t)پتو,(uintptr_t)لمبائي_قدر));
}
int 통신주소읽기(int 종단,struct 통신주소 *پتو,통신주소길이형 *لمبائي_قدر) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)پتو,(uintptr_t)لمبائي_قدر,0,0,0));
}
int ڪنيڪٽ_نيٽ_ورڪ(int 종단,const struct 통신주소 *پتو,통신주소길이형 لمبائي_قدر) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)پتو,لمبائي_قدر,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int قبول_ڪريو_نيٽ_ورڪ_ڪنيڪشن(int 종단,struct 통신주소 *پتو,통신주소길이형 *لمبائي_قدر) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)پتو,(uintptr_t)لمبائي_قدر,0,0,0));
}

/* فائل 함수도 독립된 한국어 فعل_قدر 심볼로 제공한다. */
int ٺاھيو_فائل(const char *راههه,int طريقو_موڊ,...) { return 결과검사(사용자호출(3,(uintptr_t)راههه,طريقو_موڊ,0,0,0,0)); }
입출력결과형 파일자료읽기(int فائل,void *ڪوائف,size_t 개수) { return 결과검사(사용자호출(2,فائل,(uintptr_t)ڪوائف,개수,0,0,0)); }
입출력결과형 لکو_فائل_ڪوائف(int فائل,const void *ڪوائف,size_t 개수) { return 결과검사(사용자호출(1,فائل,(uintptr_t)ڪوائف,개수,0,0,0)); }
int بند_ڪرڻ_فائل(int فائل) { return 결과검사(사용자호출(4,فائل,0,0,0,0,0)); }
فائل_آف_سيٽ_قسم ڳولا_فائل(int فائل,فائل_آف_سيٽ_قسم 거리,int 기준) { return 결과검사(사용자호출(5,فائل,거리,기준,0,0,0)); }
int هٽايو_فائل_داخلا_نالو(const char *راههه) { return 결과검사(사용자호출(11,(uintptr_t)راههه,0,0,0,0,0)); }
int سيٽ_فائل_لمبائي(int فائل,فائل_آف_سيٽ_قسم سائيز) { return 결과검사(사용자호출(10,فائل,سائيز,0,0,0,0)); }
int 파일저장확정(int فائل) { return 결과검사(사용자호출(12,فائل,0,0,0,0,0)); }
int فائل_سائيز(int فائل) { return 결과검사(사용자호출(9,فائل,0,0,0,0,0)); }

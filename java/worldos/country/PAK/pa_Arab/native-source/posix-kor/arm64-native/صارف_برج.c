// 동일 한국어 헤더를 사용하는 별도 EL0 لائبریری. کرنل_قدر 직접 호출판과 혼합 금지.
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
فائل_آف_سیٹ_ٹائپ_کرو pk_lseek(int fd, فائل_آف_سیٹ_ٹائپ_کرو offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, فائل_آف_سیٹ_ٹائپ_کرو size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 اصلی_کوائف EL0 구현. 구조체는 SVC에서 نقل_قدر·검증한다. */
int 통신종단점만들기(int پتا_خاندان,int 통신방식,int منتقلی_پروٹوکول) {
    return 결과검사(사용자호출(32,پتا_خاندان,통신방식,منتقلی_پروٹوکول,0,0,0));
}
int بنھنا_پتا(int 종단,const struct 통신주소 *پتا,통신주소길이형 لمبائی_قدر) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)پتا,لمبائی_قدر,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *کوائف,size_t 개수,int انتخاب_قدر,const struct 통신주소 *پتا,통신주소길이형 لمبائی_قدر) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)کوائف,개수,انتخاب_قدر,(uintptr_t)پتا,لمبائی_قدر));
}
intptr_t 자료전문받기(int 종단,void *کوائف,size_t 개수,int انتخاب_قدر,struct 통신주소 *پتا,통신주소길이형 *لمبائی_قدر) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)کوائف,개수,انتخاب_قدر,(uintptr_t)پتا,(uintptr_t)لمبائی_قدر));
}
int 통신주소읽기(int 종단,struct 통신주소 *پتا,통신주소길이형 *لمبائی_قدر) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)پتا,(uintptr_t)لمبائی_قدر,0,0,0));
}
int جڑو_نیٹ_ورک(int 종단,const struct 통신주소 *پتا,통신주소길이형 لمبائی_قدر) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)پتا,لمبائی_قدر,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int قبول_کرو_نیٹ_ورک_کنکشن(int 종단,struct 통신주소 *پتا,통신주소길이형 *لمبائی_قدر) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)پتا,(uintptr_t)لمبائی_قدر,0,0,0));
}

/* فائل 함수도 독립된 한국어 فعل_قدر 심볼로 제공한다. */
int بنڑاؤ_فائل(const char *راہ,int طریقہ_موڈ,...) { return 결과검사(사용자호출(3,(uintptr_t)راہ,طریقہ_موڈ,0,0,0,0)); }
입출력결과형 파일자료읽기(int فائل,void *کوائف,size_t 개수) { return 결과검사(사용자호출(2,فائل,(uintptr_t)کوائف,개수,0,0,0)); }
입출력결과형 لکھو_فائل_کوائف(int فائل,const void *کوائف,size_t 개수) { return 결과검사(사용자호출(1,فائل,(uintptr_t)کوائف,개수,0,0,0)); }
int بند_کرو_فائل(int فائل) { return 결과검사(사용자호출(4,فائل,0,0,0,0,0)); }
فائل_آف_سیٹ_ٹائپ_کرو تلاش_کرو_فائل(int فائل,فائل_آف_سیٹ_ٹائپ_کرو 거리,int 기준) { return 결과검사(사용자호출(5,فائل,거리,기준,0,0,0)); }
int ہٹاؤ_فائل_داخلہ_ناں(const char *راہ) { return 결과검사(사용자호출(11,(uintptr_t)راہ,0,0,0,0,0)); }
int سیٹ_فائل_لمبائی(int فائل,فائل_آف_سیٹ_ٹائپ_کرو سائز) { return 결과검사(사용자호출(10,فائل,سائز,0,0,0,0)); }
int 파일저장확정(int فائل) { return 결과검사(사용자호출(12,فائل,0,0,0,0,0)); }
int فائل_سائز(int فائل) { return 결과검사(사용자호출(9,فائل,0,0,0,0,0)); }

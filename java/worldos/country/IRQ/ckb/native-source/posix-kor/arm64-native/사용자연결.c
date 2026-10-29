// 동일 한국어 헤더를 사용하는 별도 EL0 کتێبخانە. کوورەک_نرخ 직접 호출판과 혼합 금지.
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
فایل_ئۆفسێت_چاپکردن pk_lseek(int fd, فایل_ئۆفسێت_چاپکردن offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, فایل_ئۆفسێت_چاپکردن size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ڕاستەکی_دەیتا EL0 구현. 구조체는 SVC에서 کۆپی_نرخ·검증한다. */
int 통신종단점만들기(int ناونیشان_خێزان,int 통신방식,int گواستنەوە_شێوازنامە) {
    return 결과검사(사용자호출(32,ناونیشان_خێزان,통신방식,گواستنەوە_شێوازنامە,0,0,0));
}
int BIND_ناونیشان(int 종단,const struct 통신주소 *ناونیشان,통신주소길이형 درێژی_نرخ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ناونیشان,درێژی_نرخ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *دەیتا,size_t 개수,int بژاردە_نرخ,const struct 통신주소 *ناونیشان,통신주소길이형 درێژی_نرخ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)دەیتا,개수,بژاردە_نرخ,(uintptr_t)ناونیشان,درێژی_نرخ));
}
intptr_t 자료전문받기(int 종단,void *دەیتا,size_t 개수,int بژاردە_نرخ,struct 통신주소 *ناونیشان,통신주소길이형 *درێژی_نرخ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)دەیتا,개수,بژاردە_نرخ,(uintptr_t)ناونیشان,(uintptr_t)درێژی_نرخ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ناونیشان,통신주소길이형 *درێژی_نرخ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ناونیشان,(uintptr_t)درێژی_نرخ,0,0,0));
}
int لكاندن_تۆڕ(int 종단,const struct 통신주소 *ناونیشان,통신주소길이형 درێژی_نرخ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ناونیشان,درێژی_نرخ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int قەبووڵکردن_گرێدانی_تۆڕ(int 종단,struct 통신주소 *ناونیشان,통신주소길이형 *درێژی_نرخ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ناونیشان,(uintptr_t)درێژی_نرخ,0,0,0));
}

/* فایل 함수도 독립된 한국어 کردار_نرخ 심볼로 제공한다. */
int کردنەوە_فایل(const char *گوزەر,int ڕێگا_دۆخ,...) { return 결과검사(사용자호출(3,(uintptr_t)گوزەر,ڕێگا_دۆخ,0,0,0,0)); }
입출력결과형 파일자료읽기(int فایل,void *دەیتا,size_t 개수) { return 결과검사(사용자호출(2,فایل,(uintptr_t)دەیتا,개수,0,0,0)); }
입출력결과형 ڕایت_کردن_فایل_دەیتا(int فایل,const void *دەیتا,size_t 개수) { return 결과검사(사용자호출(1,فایل,(uintptr_t)دەیتا,개수,0,0,0)); }
int داخستن_فایل(int فایل) { return 결과검사(사용자호출(4,فایل,0,0,0,0,0)); }
فایل_ئۆفسێت_چاپکردن گەڕان_فایل(int فایل,فایل_ئۆفسێت_چاپکردن 거리,int 기준) { return 결과검사(사용자호출(5,فایل,거리,기준,0,0,0)); }
int لابردن_فایل_تێنووسین_ناو(const char *گوزەر) { return 결과검사(사용자호출(11,(uintptr_t)گوزەر,0,0,0,0,0)); }
int سێت_فایل_درێژی(int فایل,فایل_ئۆفسێت_چاپکردن گۆڕینی_ئەندازە) { return 결과검사(사용자호출(10,فایل,گۆڕینی_ئەندازە,0,0,0,0)); }
int 파일저장확정(int فایل) { return 결과검사(사용자호출(12,فایل,0,0,0,0,0)); }
int فایل_گۆڕینی_ئەندازە(int فایل) { return 결과검사(사용자호출(9,فایل,0,0,0,0,0)); }

// 동일 한국어 헤더를 사용하는 별도 EL0 লাইব্ৰেৰী. কাৰ্ণেল_মান 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ত্ৰুটি_ক_ড;
int *pk_errno_location(void) { return &ত্ৰুটি_ক_ড; }
static intptr_t 결과검사(intptr_t পৰিমাপ) { if (পৰিমাপ < 0) { ত্ৰুটি_ক_ড = -পৰিমাপ; return -1; } return পৰিমাপ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ফাইল_অফছেট_প্ৰকাৰ pk_lseek(int fd, ফাইল_অফছেট_প্ৰকাৰ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ফাইল_অফছেট_প্ৰকাৰ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 প্ৰকৃত_ডাটা EL0 구현. 구조체는 SVC에서 নজিৰ_মান·검증한다. */
int 통신종단점만들기(int ঠিকনা_পৰিয়াল,int 통신방식,int স্থানান্তৰণ_প্ৰ_ট_ক_ল) {
    return 결과검사(사용자호출(32,ঠিকনা_পৰিয়াল,통신방식,স্থানান্তৰণ_প্ৰ_ট_ক_ল,0,0,0));
}
int বান্ধক_ঠিকনা(int 종단,const struct 통신주소 *ঠিকনা,통신주소길이형 দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ঠিকনা,দৈর্ঘ্য_মান,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ডাটা,size_t 개수,int চয়ন_মান,const struct 통신주소 *ঠিকনা,통신주소길이형 দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ডাটা,개수,চয়ন_মান,(uintptr_t)ঠিকনা,দৈর্ঘ্য_মান));
}
intptr_t 자료전문받기(int 종단,void *ডাটা,size_t 개수,int চয়ন_মান,struct 통신주소 *ঠিকনা,통신주소길이형 *দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ডাটা,개수,চয়ন_মান,(uintptr_t)ঠিকনা,(uintptr_t)দৈর্ঘ্য_মান));
}
int 통신주소읽기(int 종단,struct 통신주소 *ঠিকনা,통신주소길이형 *দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ঠিকনা,(uintptr_t)দৈর্ঘ্য_মান,0,0,0));
}
int সংযোগ_নেটৱৰ্ক(int 종단,const struct 통신주소 *ঠিকনা,통신주소길이형 দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ঠিকনা,দৈর্ঘ্য_মান,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int গ্ৰহণ_নেটৱৰ্ক_সংযোগ(int 종단,struct 통신주소 *ঠিকনা,통신주소길이형 *দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ঠিকনা,(uintptr_t)দৈর্ঘ্য_মান,0,0,0));
}

/* নথিপত্ৰ 함수도 독립된 한국어 ফাংছন_মান 심볼로 제공한다. */
int খোলক_ফাইল(const char *পথ,int পদ্ধতি_মোড,...) { return 결과검사(사용자호출(3,(uintptr_t)পথ,পদ্ধতি_মোড,0,0,0,0)); }
입출력결과형 파일자료읽기(int নথিপত্ৰ,void *ডাটা,size_t 개수) { return 결과검사(사용자호출(2,নথিপত্ৰ,(uintptr_t)ডাটা,개수,0,0,0)); }
입출력결과형 লিখক_ফাইল_ডাটা(int নথিপত্ৰ,const void *ডাটা,size_t 개수) { return 결과검사(사용자호출(1,নথিপত্ৰ,(uintptr_t)ডাটা,개수,0,0,0)); }
int বন্ধ_কৰক_ফাইল(int নথিপত্ৰ) { return 결과검사(사용자호출(4,নথিপত্ৰ,0,0,0,0,0)); }
ফাইল_অফছেট_প্ৰকাৰ ছীক_ফাইল(int নথিপত্ৰ,ফাইল_অফছেট_প্ৰকাৰ 거리,int 기준) { return 결과검사(사용자호출(5,নথিপত্ৰ,거리,기준,0,0,0)); }
int আঁতৰাওক_ফাইল_প্রবিষ্ট_নাম(const char *পথ) { return 결과검사(사용자호출(11,(uintptr_t)পথ,0,0,0,0,0)); }
int ছেট_ফাইল_দৈর্ঘ্য(int নথিপত্ৰ,ফাইল_অফছেট_প্ৰকাৰ মাপ) { return 결과검사(사용자호출(10,নথিপত্ৰ,মাপ,0,0,0,0)); }
int 파일저장확정(int নথিপত্ৰ) { return 결과검사(사용자호출(12,নথিপত্ৰ,0,0,0,0,0)); }
int ফাইল_আকাৰ_কৰক(int নথিপত্ৰ) { return 결과검사(사용자호출(9,নথিপত্ৰ,0,0,0,0,0)); }

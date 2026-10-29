// 동일 বাংলা 헤더를 사용하는 별도 EL0 লাইব্রেরি. কারনেল_মান 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ত্রুটি_কোড;
int *pk_errno_location(void) { return &ত্রুটি_কোড; }
static intptr_t 결과검사(intptr_t পরিমাপ) { if (পরিমাপ < 0) { ত্রুটি_কোড = -পরিমাপ; return -1; } return পরিমাপ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ফাইল_অফসেট_টাইপ_করুন pk_lseek(int fd, ফাইল_অফসেট_টাইপ_করুন offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ফাইল_অফসেট_টাইপ_করুন size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* বাংলা 공개 함수의 প্রকৃত_ডাটা EL0 구현. 구조체는 SVC에서 নজির_মান·검증한다. */
int 통신종단점만들기(int ইমেইল_পরিবার,int 통신방식,int স্থানান্তর_প্রটোকল) {
    return 결과검사(사용자호출(32,ইমেইল_পরিবার,통신방식,স্থানান্তর_প্রটোকল,0,0,0));
}
int বন্ধন_করা_ইমেইল(int 종단,const struct 통신주소 *ইমেইল,통신주소길이형 দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ইমেইল,দৈর্ঘ্য_মান,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ডাটা,size_t 개수,int বাছাই_মান,const struct 통신주소 *ইমেইল,통신주소길이형 দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ডাটা,개수,বাছাই_মান,(uintptr_t)ইমেইল,দৈর্ঘ্য_মান));
}
intptr_t 자료전문받기(int 종단,void *ডাটা,size_t 개수,int বাছাই_মান,struct 통신주소 *ইমেইল,통신주소길이형 *দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ডাটা,개수,বাছাই_মান,(uintptr_t)ইমেইল,(uintptr_t)দৈর্ঘ্য_মান));
}
int 통신주소읽기(int 종단,struct 통신주소 *ইমেইল,통신주소길이형 *দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ইমেইল,(uintptr_t)দৈর্ঘ্য_মান,0,0,0));
}
int সংযোগ_নেটওয়ার্ক(int 종단,const struct 통신주소 *ইমেইল,통신주소길이형 দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ইমেইল,দৈর্ঘ্য_মান,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int স্বীকার_করুন_নেটওয়ার্ক_সংযোগ(int 종단,struct 통신주소 *ইমেইল,통신주소길이형 *দৈর্ঘ্য_মান) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ইমেইল,(uintptr_t)দৈর্ঘ্য_মান,0,0,0));
}

/* নথির_নাম 함수도 독립된 বাংলা ফাংশন_মান 심볼로 제공한다. */
int খোলা_ফাইল(const char *পথ_2,int পদ্ধতি_মোড,...) { return 결과검사(사용자호출(3,(uintptr_t)পথ_2,পদ্ধতি_মোড,0,0,0,0)); }
입출력결과형 파일자료읽기(int নথির_নাম,void *ডাটা,size_t 개수) { return 결과검사(사용자호출(2,নথির_নাম,(uintptr_t)ডাটা,개수,0,0,0)); }
입출력결과형 লেখা_ফাইল_ডাটা(int নথির_নাম,const void *ডাটা,size_t 개수) { return 결과검사(사용자호출(1,নথির_নাম,(uintptr_t)ডাটা,개수,0,0,0)); }
int বন্ধ_ফাইল(int নথির_নাম) { return 결과검사(사용자호출(4,নথির_নাম,0,0,0,0,0)); }
ফাইল_অফসেট_টাইপ_করুন সিক_ফাইল(int নথির_নাম,ফাইল_অফসেট_টাইপ_করুন 거리,int প্রকল্প_মূল) { return 결과검사(사용자호출(5,নথির_নাম,거리,প্রকল্প_মূল,0,0,0)); }
int সরানো_ফাইল_ভুক্তি_নাম(const char *পথ_2) { return 결과검사(사용자호출(11,(uintptr_t)পথ_2,0,0,0,0,0)); }
int সেট_ফাইল_দৈর্ঘ্য(int নথির_নাম,ফাইল_অফসেট_টাইপ_করুন আকার) { return 결과검사(사용자호출(10,নথির_নাম,আকার,0,0,0,0)); }
int 파일저장확정(int নথির_নাম) { return 결과검사(사용자호출(12,নথির_নাম,0,0,0,0,0)); }
int ফাইল_আয়তন(int নথির_নাম) { return 결과검사(사용자호출(9,নথির_নাম,0,0,0,0,0)); }

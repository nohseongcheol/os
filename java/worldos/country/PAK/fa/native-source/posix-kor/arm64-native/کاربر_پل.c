// 동일 فارسی 헤더를 사용하는 별도 EL0 کتابخانه. هسته_مقدار 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int کد_خطا;
int *pk_errno_location(void) { return &کد_خطا; }
static intptr_t 결과검사(intptr_t سنجش) { if (سنجش < 0) { کد_خطا = -سنجش; return -1; } return سنجش; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
فایل_جابجایی_لایه_ای_تایپ_کردن pk_lseek(int fd, فایل_جابجایی_لایه_ای_تایپ_کردن offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, فایل_جابجایی_لایه_ای_تایپ_کردن size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* فارسی 공개 함수의 واقعی_داده_ها EL0 구현. 구조체는 SVC에서 کپی_مقدار·검증한다. */
int 통신종단점만들기(int آدرس_خانواده,int 통신방식,int انتقال_پروتکل) {
    return 결과검사(사용자호출(32,آدرس_خانواده,통신방식,انتقال_پروتکل,0,0,0));
}
int مرتبط_سازی_آدرس(int 종단,const struct 통신주소 *آدرس,통신주소길이형 طول_مقدار) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)آدرس,طول_مقدار,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *داده_ها,size_t 개수,int مورد_انتخابی_مقدار,const struct 통신주소 *آدرس,통신주소길이형 طول_مقدار) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)داده_ها,개수,مورد_انتخابی_مقدار,(uintptr_t)آدرس,طول_مقدار));
}
intptr_t 자료전문받기(int 종단,void *داده_ها,size_t 개수,int مورد_انتخابی_مقدار,struct 통신주소 *آدرس,통신주소길이형 *طول_مقدار) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)داده_ها,개수,مورد_انتخابی_مقدار,(uintptr_t)آدرس,(uintptr_t)طول_مقدار));
}
int 통신주소읽기(int 종단,struct 통신주소 *آدرس,통신주소길이형 *طول_مقدار) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)آدرس,(uintptr_t)طول_مقدار,0,0,0));
}
int اتصال_شبکه(int 종단,const struct 통신주소 *آدرس,통신주소길이형 طول_مقدار) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)آدرس,طول_مقدار,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int پذیرش_اتصال_شبکه(int 종단,struct 통신주소 *آدرس,통신주소길이형 *طول_مقدار) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)آدرس,(uintptr_t)طول_مقدار,0,0,0));
}

/* پرونده 함수도 독립된 فارسی عملکرد_مقدار 심볼로 제공한다. */
int ایجاد_فایل(const char *مسیر,int روش_حالت,...) { return 결과검사(사용자호출(3,(uintptr_t)مسیر,روش_حالت,0,0,0,0)); }
입출력결과형 파일자료읽기(int پرونده,void *داده_ها,size_t 개수) { return 결과검사(사용자호출(2,پرونده,(uintptr_t)داده_ها,개수,0,0,0)); }
입출력결과형 نوشتن_فایل_داده_ها(int پرونده,const void *داده_ها,size_t 개수) { return 결과검사(사용자호출(1,پرونده,(uintptr_t)داده_ها,개수,0,0,0)); }
int بستن_فایل(int پرونده) { return 결과검사(사용자호출(4,پرونده,0,0,0,0,0)); }
فایل_جابجایی_لایه_ای_تایپ_کردن جستجو_کردن_فایل(int پرونده,فایل_جابجایی_لایه_ای_تایپ_کردن 거리,int نمایش_دادن_جذر) { return 결과검사(사용자호출(5,پرونده,거리,نمایش_دادن_جذر,0,0,0)); }
int حذف_فایل_ورودی_نام(const char *مسیر) { return 결과검사(사용자호출(11,(uintptr_t)مسیر,0,0,0,0,0)); }
int مجموعه_فایل_طول(int پرونده,فایل_جابجایی_لایه_ای_تایپ_کردن اندازه) { return 결과검사(사용자호출(10,پرونده,اندازه,0,0,0,0)); }
int 파일저장확정(int پرونده) { return 결과검사(사용자호출(12,پرونده,0,0,0,0,0)); }
int فایل_اندازه_کردن(int پرونده) { return 결과검사(사용자호출(9,پرونده,0,0,0,0,0)); }

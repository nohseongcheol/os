// 동일 اردو 헤더를 사용하는 별도 EL0 لائبریری. کرنیل_قدر 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int نقص_کوڈ;
int *pk_errno_location(void) { return &نقص_کوڈ; }
static intptr_t 결과검사(intptr_t پیمائش) { if (پیمائش < 0) { نقص_کوڈ = -پیمائش; return -1; } return پیمائش; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
فائل_آفسٹ_ٹائپ_کریں pk_lseek(int fd, فائل_آفسٹ_ٹائپ_کریں offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, فائل_آفسٹ_ٹائپ_کریں size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* اردو 공개 함수의 اصل_کوائف EL0 구현. 구조체는 SVC에서 نقل_قدر·검증한다. */
int 통신종단점만들기(int پتہ_خاندان,int 통신방식,int منتقلی_پروٹوکول) {
    return 결과검사(사용자호출(32,پتہ_خاندان,통신방식,منتقلی_پروٹوکول,0,0,0));
}
int باندھیں_پتہ(int 종단,const struct 통신주소 *پتہ,통신주소길이형 لمبا_ئی_قدر) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)پتہ,لمبا_ئی_قدر,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *کوائف,size_t 개수,int انتخاب_قدر,const struct 통신주소 *پتہ,통신주소길이형 لمبا_ئی_قدر) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)کوائف,개수,انتخاب_قدر,(uintptr_t)پتہ,لمبا_ئی_قدر));
}
intptr_t 자료전문받기(int 종단,void *کوائف,size_t 개수,int انتخاب_قدر,struct 통신주소 *پتہ,통신주소길이형 *لمبا_ئی_قدر) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)کوائف,개수,انتخاب_قدر,(uintptr_t)پتہ,(uintptr_t)لمبا_ئی_قدر));
}
int 통신주소읽기(int 종단,struct 통신주소 *پتہ,통신주소길이형 *لمبا_ئی_قدر) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)پتہ,(uintptr_t)لمبا_ئی_قدر,0,0,0));
}
int جڑیں_نیٹ_ورک(int 종단,const struct 통신주소 *پتہ,통신주소길이형 لمبا_ئی_قدر) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)پتہ,لمبا_ئی_قدر,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int قبول_کریں_نیٹ_ورک_کنکشن(int 종단,struct 통신주소 *پتہ,통신주소길이형 *لمبا_ئی_قدر) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)پتہ,(uintptr_t)لمبا_ئی_قدر,0,0,0));
}

/* فائل_کا_نام 함수도 독립된 اردو فعل_قدر 심볼로 제공한다. */
int بنائیں_فائل(const char *راستہ_2,int طریقہ_موڈ,...) { return 결과검사(사용자호출(3,(uintptr_t)راستہ_2,طریقہ_موڈ,0,0,0,0)); }
입출력결과형 파일자료읽기(int فائل_کا_نام,void *کوائف,size_t 개수) { return 결과검사(사용자호출(2,فائل_کا_نام,(uintptr_t)کوائف,개수,0,0,0)); }
입출력결과형 لکھیں_فائل_کوائف(int فائل_کا_نام,const void *کوائف,size_t 개수) { return 결과검사(사용자호출(1,فائل_کا_نام,(uintptr_t)کوائف,개수,0,0,0)); }
int بند_فائل(int فائل_کا_نام) { return 결과검사(사용자호출(4,فائل_کا_نام,0,0,0,0,0)); }
فائل_آفسٹ_ٹائپ_کریں تلاش_کرنا_فائل(int فائل_کا_نام,فائل_آفسٹ_ٹائپ_کریں 거리,int عکس_ڈالنا_روٹ) { return 결과검사(사용자호출(5,فائل_کا_نام,거리,عکس_ڈالنا_روٹ,0,0,0)); }
int ہٹائیں_فائل_اندراج_نام(const char *راستہ_2) { return 결과검사(사용자호출(11,(uintptr_t)راستہ_2,0,0,0,0,0)); }
int سیٹ_فائل_لمبا_ئی(int فائل_کا_نام,فائل_آفسٹ_ٹائپ_کریں حجم) { return 결과검사(사용자호출(10,فائل_کا_نام,حجم,0,0,0,0)); }
int 파일저장확정(int فائل_کا_نام) { return 결과검사(사용자호출(12,فائل_کا_نام,0,0,0,0,0)); }
int فائل_سائز_دیں(int فائل_کا_نام) { return 결과검사(사용자호출(9,فائل_کا_نام,0,0,0,0,0)); }

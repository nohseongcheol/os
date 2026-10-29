// 동일 العربية 헤더를 사용하는 별도 EL0 مكتبة. نواة_قيمة 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int رمز_الخطأ;
int *pk_errno_location(void) { return &رمز_الخطأ; }
static intptr_t 결과검사(intptr_t نتيجة) { if (نتيجة < 0) { رمز_الخطأ = -نتيجة; return -1; } return نتيجة; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ملف_إزاحة_نوع pk_lseek(int fd, ملف_إزاحة_نوع offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ملف_إزاحة_نوع size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* العربية 공개 함수의 الفعلي_بيانات EL0 구현. 구조체는 SVC에서 مثيل_قيمة·검증한다. */
int فتح_المشارك(int عنوان_عائلة,int 통신방식,int نقل_بروتوكول) {
    return 결과검사(사용자호출(32,عنوان_عائلة,통신방식,نقل_بروتوكول,0,0,0));
}
int يربط_عنوان(int المشارك,const struct مأخذ_التوصيل_عنوان *عنوان,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,المشارك,(uintptr_t)عنوان,길이,0,0,0));
}
intptr_t يرسل_مخطط_بيانات_بيانات(int المشارك,const void *بيانات,size_t 개수,int تحديد_قيمة,const struct مأخذ_التوصيل_عنوان *عنوان,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,المشارك,(uintptr_t)بيانات,개수,تحديد_قيمة,(uintptr_t)عنوان,길이));
}
intptr_t يستلم_مخطط_بيانات_بيانات(int المشارك,void *بيانات,size_t 개수,int تحديد_قيمة,struct مأخذ_التوصيل_عنوان *عنوان,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,المشارك,(uintptr_t)بيانات,개수,تحديد_قيمة,(uintptr_t)عنوان,(uintptr_t)길이));
}
int يقرأ_مأخذ_التوصيل_عنوان(int المشارك,struct مأخذ_التوصيل_عنوان *عنوان,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,المشارك,(uintptr_t)عنوان,(uintptr_t)길이,0,0,0));
}
int يتصل_شبكة(int المشارك,const struct مأخذ_التوصيل_عنوان *عنوان,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,المشارك,(uintptr_t)عنوان,길이,0,0,0));
}
int 통신연결기다리기(int المشارك,int 대기수) {
    return 결과검사(사용자호출(38,المشارك,대기수,0,0,0,0));
}
int قبول_اتصال_الشبكة(int المشارك,struct مأخذ_التوصيل_عنوان *عنوان,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,المشارك,(uintptr_t)عنوان,(uintptr_t)길이,0,0,0));
}

/* ملف 함수도 독립된 العربية دالة_قيمة 심볼로 제공한다. */
int فتح_ملف(const char *مسار,int أسلوب_الوضع,...) { return 결과검사(사용자호출(3,(uintptr_t)مسار,أسلوب_الوضع,0,0,0,0)); }
입출력결과형 يقرأ_ملف_بيانات(int ملف,void *بيانات,size_t 개수) { return 결과검사(사용자호출(2,ملف,(uintptr_t)بيانات,개수,0,0,0)); }
입출력결과형 كتابة_ملف_بيانات(int ملف,const void *بيانات,size_t 개수) { return 결과검사(사용자호출(1,ملف,(uintptr_t)بيانات,개수,0,0,0)); }
int يغلق_ملف(int ملف) { return 결과검사(사용자호출(4,ملف,0,0,0,0,0)); }
ملف_إزاحة_نوع يبحث_ملف(int ملف,ملف_إزاحة_نوع 거리,int يعرض_جذر) { return 결과검사(사용자호출(5,ملف,거리,يعرض_جذر,0,0,0)); }
int يزيل_ملف_إدخال_اسم(const char *مسار) { return 결과검사(사용자호출(11,(uintptr_t)مسار,0,0,0,0,0)); }
int 파일길이정하기(int ملف,ملف_إزاحة_نوع حجم) { return 결과검사(사용자호출(10,ملف,حجم,0,0,0,0)); }
int تثبيت_تخزين_الملفات(int ملف) { return 결과검사(사용자호출(12,ملف,0,0,0,0,0)); }
int حجم_الملف(int ملف) { return 결과검사(사용자호출(9,ملف,0,0,0,0,0)); }

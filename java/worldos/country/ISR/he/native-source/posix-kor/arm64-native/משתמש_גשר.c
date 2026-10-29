// 동일 עברית 헤더를 사용하는 별도 EL0 ספריה. ליבה_ערך 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int קוד_שגיאה;
int *pk_errno_location(void) { return &קוד_שגיאה; }
static intptr_t 결과검사(intptr_t תוצאה) { if (תוצאה < 0) { קוד_שגיאה = -תוצאה; return -1; } return תוצאה; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
קובץ_היסט_כתב pk_lseek(int fd, קובץ_היסט_כתב offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, קובץ_היסט_כתב size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* עברית 공개 함수의 בפועל_נתונים EL0 구현. 구조체는 SVC에서 מופע_ערך·검증한다. */
int ליצור_משתתף(int למען_משפחה,int 통신방식,int העבר_פרוטוקול) {
    return 결과검사(사용자호출(32,למען_משפחה,통신방식,העבר_פרוטוקול,0,0,0));
}
int לאגד_למען(int משתתף,const struct 통신주소 *למען,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,משתתף,(uintptr_t)למען,길이,0,0,0));
}
intptr_t שלח_יחידת_נתונים_נתונים(int משתתף,const void *נתונים,size_t 개수,int קטע_נבחר_ערך,const struct 통신주소 *למען,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,משתתף,(uintptr_t)נתונים,개수,קטע_נבחר_ערך,(uintptr_t)למען,길이));
}
intptr_t לקבל_יחידת_נתונים_נתונים(int משתתף,void *נתונים,size_t 개수,int קטע_נבחר_ערך,struct 통신주소 *למען,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,משתתף,(uintptr_t)נתונים,개수,קטע_נבחר_ערך,(uintptr_t)למען,(uintptr_t)길이));
}
int 통신주소읽기(int משתתף,struct 통신주소 *למען,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,משתתף,(uintptr_t)למען,(uintptr_t)길이,0,0,0));
}
int לקשר_רשת(int משתתף,const struct 통신주소 *למען,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,משתתף,(uintptr_t)למען,길이,0,0,0));
}
int 통신연결기다리기(int משתתף,int 대기수) {
    return 결과검사(사용자호출(38,משתתף,대기수,0,0,0,0));
}
int לקבל_חיבור_רשת(int משתתף,struct 통신주소 *למען,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,משתתף,(uintptr_t)למען,(uintptr_t)길이,0,0,0));
}

/* קובץ 함수도 독립된 עברית פונקציה_ערך 심볼로 제공한다. */
int פתח_קובץ(const char *נתיב,int פעולת_שירות_מצב,...) { return 결과검사(사용자호출(3,(uintptr_t)נתיב,פעולת_שירות_מצב,0,0,0,0)); }
입출력결과형 파일자료읽기(int קובץ,void *נתונים,size_t 개수) { return 결과검사(사용자호출(2,קובץ,(uintptr_t)נתונים,개수,0,0,0)); }
입출력결과형 כתיבה_קובץ_נתונים(int קובץ,const void *נתונים,size_t 개수) { return 결과검사(사용자호출(1,קובץ,(uintptr_t)נתונים,개수,0,0,0)); }
int סגור_קובץ(int קובץ) { return 결과검사(사용자호출(4,קובץ,0,0,0,0,0)); }
קובץ_היסט_כתב חפש_קובץ(int קובץ,קובץ_היסט_כתב 거리,int לשקף_בסיס) { return 결과검사(사용자호출(5,קובץ,거리,לשקף_בסיס,0,0,0)); }
int הסר_קובץ_ערך_שם(const char *נתיב) { return 결과검사(사용자호출(11,(uintptr_t)נתיב,0,0,0,0,0)); }
int 파일길이정하기(int קובץ,קובץ_היסט_כתב גודל) { return 결과검사(사용자호출(10,קובץ,גודל,0,0,0,0)); }
int 파일저장확정(int קובץ) { return 결과검사(사용자호출(12,קובץ,0,0,0,0,0)); }
int גודל_קובץ(int קובץ) { return 결과검사(사용자호출(9,קובץ,0,0,0,0,0)); }

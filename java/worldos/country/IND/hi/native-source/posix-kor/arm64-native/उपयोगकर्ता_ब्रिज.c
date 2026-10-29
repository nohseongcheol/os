// 동일 हिंदी 헤더를 사용하는 별도 EL0 लाइब्रेरी. कर्नेल_मान 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int त्रुटि_कोड;
int *pk_errno_location(void) { return &त्रुटि_कोड; }
static intptr_t 결과검사(intptr_t परिणाम) { if (परिणाम < 0) { त्रुटि_कोड = -परिणाम; return -1; } return परिणाम; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
फ़ाइल_ऑफ़सेट_लिखें pk_lseek(int fd, फ़ाइल_ऑफ़सेट_लिखें offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, फ़ाइल_ऑफ़सेट_लिखें size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* हिंदी 공개 함수의 वास्तविक_डेटा EL0 구현. 구조체는 SVC에서 आवृत्ति_मान·검증한다. */
int बनाएँ_एंडपॉइंट(int पता_समूह,int 통신방식,int हस्तांतरण_प्रोटोकॉल) {
    return 결과검사(사용자호출(32,पता_समूह,통신방식,हस्तांतरण_प्रोटोकॉल,0,0,0));
}
int बाइंड_करें_पता(int एंडपॉइंट,const struct सॉकेट_पता *पता,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,एंडपॉइंट,(uintptr_t)पता,길이,0,0,0));
}
intptr_t 자료전문보내기(int एंडपॉइंट,const void *आँकड़े,size_t 개수,int चयन_मान,const struct सॉकेट_पता *पता,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,एंडपॉइंट,(uintptr_t)आँकड़े,개수,चयन_मान,(uintptr_t)पता,길이));
}
intptr_t 자료전문받기(int एंडपॉइंट,void *आँकड़े,size_t 개수,int चयन_मान,struct सॉकेट_पता *पता,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,एंडपॉइंट,(uintptr_t)आँकड़े,개수,चयन_मान,(uintptr_t)पता,(uintptr_t)길이));
}
int पढें_सॉकेट_पता(int एंडपॉइंट,struct सॉकेट_पता *पता,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,एंडपॉइंट,(uintptr_t)पता,(uintptr_t)길이,0,0,0));
}
int कनेक्ट_नेटवर्क(int एंडपॉइंट,const struct सॉकेट_पता *पता,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,एंडपॉइंट,(uintptr_t)पता,길이,0,0,0));
}
int 통신연결기다리기(int एंडपॉइंट,int 대기수) {
    return 결과검사(사용자호출(38,एंडपॉइंट,대기수,0,0,0,0));
}
int स्वीकार_करें_नेटवर्क_कनेक्शन(int एंडपॉइंट,struct सॉकेट_पता *पता,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,एंडपॉइंट,(uintptr_t)पता,(uintptr_t)길이,0,0,0));
}

/* संचिका 함수도 독립된 हिंदी फ़ंक्_शन_मान 심볼로 제공한다. */
int जारी_फ़ाइल(const char *पथ,int विधि_मोड,...) { return 결과검사(사용자호출(3,(uintptr_t)पथ,विधि_मोड,0,0,0,0)); }
입출력결과형 पढें_फ़ाइल_डेटा(int संचिका,void *आँकड़े,size_t 개수) { return 결과검사(사용자호출(2,संचिका,(uintptr_t)आँकड़े,개수,0,0,0)); }
입출력결과형 लिखना_फ़ाइल_डेटा(int संचिका,const void *आँकड़े,size_t 개수) { return 결과검사(사용자호출(1,संचिका,(uintptr_t)आँकड़े,개수,0,0,0)); }
int बंद_फ़ाइल(int संचिका) { return 결과검사(사용자호출(4,संचिका,0,0,0,0,0)); }
फ़ाइल_ऑफ़सेट_लिखें खोजें_फ़ाइल(int संचिका,फ़ाइल_ऑफ़सेट_लिखें 거리,int प्रोजेक्ट_करें_मूल) { return 결과검사(사용자호출(5,संचिका,거리,प्रोजेक्ट_करें_मूल,0,0,0)); }
int निकालें_फ़ाइल_एन्ट्री_नाम(const char *पथ) { return 결과검사(사용자호출(11,(uintptr_t)पथ,0,0,0,0,0)); }
int 파일길이정하기(int संचिका,फ़ाइल_ऑफ़सेट_लिखें आकार) { return 결과검사(사용자호출(10,संचिका,आकार,0,0,0,0)); }
int कमिट_फ़ाइल_संग्रहण(int संचिका) { return 결과검사(사용자호출(12,संचिका,0,0,0,0,0)); }
int फ़ाइल_आकार(int संचिका) { return 결과검사(사용자호출(9,संचिका,0,0,0,0,0)); }

// 동일 नेपाली 헤더를 사용하는 별도 EL0 पुस्तकालय. कर्णेल_मान 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int त्रुटिकोड;
int *pk_errno_location(void) { return &त्रुटिकोड; }
static intptr_t 결과검사(intptr_t मापन) { if (मापन < 0) { त्रुटिकोड = -मापन; return -1; } return मापन; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
फाइल_अफसेट_प्रकार pk_lseek(int fd, फाइल_अफसेट_प्रकार offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, फाइल_अफसेट_प्रकार size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* नेपाली 공개 함수의 वास्तविक_लगत EL0 구현. 구조체는 SVC에서 उद्धरण_मान_37b3d3b1·검증한다. */
int 통신종단점만들기(int ठेगाना_परिवार,int 통신방식,int ट्रान्सफर_प्रोटोकल) {
    return 결과검사(사용자호출(32,ठेगाना_परिवार,통신방식,ट्रान्सफर_प्रोटोकल,0,0,0));
}
int बाँध्नु_ठेगाना(int 종단,const struct 통신주소 *ठेगाना,통신주소길이형 लम्बाइ_मान) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ठेगाना,लम्बाइ_मान,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *लगत,size_t 개수,int चयन_मान,const struct 통신주소 *ठेगाना,통신주소길이형 लम्बाइ_मान) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)लगत,개수,चयन_मान,(uintptr_t)ठेगाना,लम्बाइ_मान));
}
intptr_t 자료전문받기(int 종단,void *लगत,size_t 개수,int चयन_मान,struct 통신주소 *ठेगाना,통신주소길이형 *लम्बाइ_मान) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)लगत,개수,चयन_मान,(uintptr_t)ठेगाना,(uintptr_t)लम्बाइ_मान));
}
int 통신주소읽기(int 종단,struct 통신주소 *ठेगाना,통신주소길이형 *लम्बाइ_मान) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ठेगाना,(uintptr_t)लम्बाइ_मान,0,0,0));
}
int कनेक्ट_सञ्जाल(int 종단,const struct 통신주소 *ठेगाना,통신주소길이형 लम्बाइ_मान) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ठेगाना,लम्बाइ_मान,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int स्वीकार्नुहोस्_नेटवर्क_जडान(int 종단,struct 통신주소 *ठेगाना,통신주소길이형 *लम्बाइ_मान) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ठेगाना,(uintptr_t)लम्बाइ_मान,0,0,0));
}

/* फाइल 함수도 독립된 नेपाली प्रकार्य_मान 심볼로 제공한다. */
int सिर्जना_फाइल(const char *मार्ग,int तरिका_मोड,...) { return 결과검사(사용자호출(3,(uintptr_t)मार्ग,तरिका_मोड,0,0,0,0)); }
입출력결과형 파일자료읽기(int फाइल,void *लगत,size_t 개수) { return 결과검사(사용자호출(2,फाइल,(uintptr_t)लगत,개수,0,0,0)); }
입출력결과형 लेख्नुहोस्_फाइल_लगत(int फाइल,const void *लगत,size_t 개수) { return 결과검사(사용자호출(1,फाइल,(uintptr_t)लगत,개수,0,0,0)); }
int बन्द_गर्नुहोस्_फाइल(int फाइल) { return 결과검사(사용자호출(4,फाइल,0,0,0,0,0)); }
फाइल_अफसेट_प्रकार खोज्नुहोस्_फाइल(int फाइल,फाइल_अफसेट_प्रकार 거리,int परियोजना_रूट) { return 결과검사(사용자호출(5,फाइल,거리,परियोजना_रूट,0,0,0)); }
int हटाउनुहोस्_फाइल_प्रविष्टि_नाम(const char *मार्ग) { return 결과검사(사용자호출(11,(uintptr_t)मार्ग,0,0,0,0,0)); }
int सेट_फाइल_लम्बाइ(int फाइल,फाइल_अफसेट_प्रकार आकार) { return 결과검사(사용자호출(10,फाइल,आकार,0,0,0,0)); }
int 파일저장확정(int फाइल) { return 결과검사(사용자호출(12,फाइल,0,0,0,0,0)); }
int फाइल_साइज(int फाइल) { return 결과검사(사용자호출(9,फाइल,0,0,0,0,0)); }

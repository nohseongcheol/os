// 동일 한국어 헤더를 사용하는 별도 EL0 लायब्ररी. कर्नेल_मोल 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int चुकिचो_कोड;
int *pk_errno_location(void) { return &चुकिचो_कोड; }
static intptr_t 결과검사(intptr_t मेजप) { if (मेजप < 0) { चुकिचो_कोड = -मेजप; return -1; } return मेजप; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
फायल_ऑफसॅट_TYPE pk_lseek(int fd, फायल_ऑफसॅट_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, फायल_ऑफसॅट_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 प्रत्यक्ष_डेटा EL0 구현. 구조체는 SVC에서 इन्सटन्स_मोल·검증한다. */
int 통신종단점만들기(int नामो_कुटुंब,int 통신방식,int ट्रान्सफर_प्रोटोकॉल) {
    return 결과검사(사용자호출(32,नामो_कुटुंब,통신방식,ट्रान्सफर_प्रोटोकॉल,0,0,0));
}
int BIND_नामो(int 종단,const struct 통신주소 *नामो,통신주소길이형 लांबाय_मोल) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)नामो,लांबाय_मोल,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *डेटा,size_t आयटम_COUNT,int निवड_मोल,const struct 통신주소 *नामो,통신주소길이형 लांबाय_मोल) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)डेटा,आयटम_COUNT,निवड_मोल,(uintptr_t)नामो,लांबाय_मोल));
}
intptr_t 자료전문받기(int 종단,void *डेटा,size_t आयटम_COUNT,int निवड_मोल,struct 통신주소 *नामो,통신주소길이형 *लांबाय_मोल) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)डेटा,आयटम_COUNT,निवड_मोल,(uintptr_t)नामो,(uintptr_t)लांबाय_मोल));
}
int 통신주소읽기(int 종단,struct 통신주소 *नामो,통신주소길이형 *लांबाय_मोल) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)नामो,(uintptr_t)लांबाय_मोल,0,0,0));
}
int कनॅक्ट_नॅटवर्क(int 종단,const struct 통신주소 *नामो,통신주소길이형 लांबाय_मोल) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)नामो,लांबाय_मोल,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int स्विकारचें_नॅटवर्क_कनॅक्शन(int 종단,struct 통신주소 *नामो,통신주소길이형 *लांबाय_मोल) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)नामो,(uintptr_t)लांबाय_मोल,0,0,0));
}

/* फायल 함수도 독립된 한국어 फंक्शन_मोल 심볼로 제공한다. */
int उगडचें_फायल(const char *पाथ,int पद्दत_मोड,...) { return 결과검사(사용자호출(3,(uintptr_t)पाथ,पद्दत_मोड,0,0,0,0)); }
입출력결과형 파일자료읽기(int फायल,void *डेटा,size_t आयटम_COUNT) { return 결과검사(사용자호출(2,फायल,(uintptr_t)डेटा,आयटम_COUNT,0,0,0)); }
입출력결과형 बरोवचें_फायल_डेटा(int फायल,const void *डेटा,size_t आयटम_COUNT) { return 결과검사(사용자호출(1,फायल,(uintptr_t)डेटा,आयटम_COUNT,0,0,0)); }
int शेवट_फायल(int फायल) { return 결과검사(사용자호출(4,फायल,0,0,0,0,0)); }
फायल_ऑफसॅट_TYPE सोद_फायल(int फायल,फायल_ऑफसॅट_TYPE 거리,int प्रॉजॅक्ट_रूट) { return 결과검사(사용자호출(5,फायल,거리,प्रॉजॅक्ट_रूट,0,0,0)); }
int काडचें_फायल_प्रवेश_नांव(const char *पाथ) { return 결과검사(사용자호출(11,(uintptr_t)पाथ,0,0,0,0,0)); }
int संच_फायल_लांबाय(int फायल,फायल_ऑफसॅट_TYPE आवाठ) { return 결과검사(사용자호출(10,फायल,आवाठ,0,0,0,0)); }
int 파일저장확정(int फायल) { return 결과검사(사용자호출(12,फायल,0,0,0,0,0)); }
int फायल_आवाठ(int फायल) { return 결과검사(사용자호출(9,फायल,0,0,0,0,0)); }

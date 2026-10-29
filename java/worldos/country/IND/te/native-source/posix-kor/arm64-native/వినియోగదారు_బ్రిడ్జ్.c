// 동일 한국어 헤더를 사용하는 별도 EL0 లైబ్రరీ. కెర్నల్_మూల్యం 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int దోష_కోడ్;
int *pk_errno_location(void) { return &దోష_కోడ్; }
static intptr_t 결과검사(intptr_t ప్రమాణం) { if (ప్రమాణం < 0) { దోష_కోడ్ = -ప్రమాణం; return -1; } return ప్రమాణం; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి pk_lseek(int fd, ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 వాస్తవ_డేటా EL0 구현. 구조체는 SVC에서 కాపీ_మూల్యం·검증한다. */
int 통신종단점만들기(int ఇమెయిల్_కుటుంబం,int 통신방식,int బదిలీ_ప్రోటోకాల్) {
    return 결과검사(사용자호출(32,ఇమెయిల్_కుటుంబం,통신방식,బదిలీ_ప్రోటోకాల్,0,0,0));
}
int బైండ్_చేయి_ఇమెయిల్(int 종단,const struct 통신주소 *ఇమెయిల్,통신주소길이형 పొడవు_మూల్యం) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ఇమెయిల్,పొడవు_మూల్యం,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *డేటా,size_t 개수,int ఎంపిక_మూల్యం,const struct 통신주소 *ఇమెయిల్,통신주소길이형 పొడవు_మూల్యం) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)డేటా,개수,ఎంపిక_మూల్యం,(uintptr_t)ఇమెయిల్,పొడవు_మూల్యం));
}
intptr_t 자료전문받기(int 종단,void *డేటా,size_t 개수,int ఎంపిక_మూల్యం,struct 통신주소 *ఇమెయిల్,통신주소길이형 *పొడవు_మూల్యం) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)డేటా,개수,ఎంపిక_మూల్యం,(uintptr_t)ఇమెయిల్,(uintptr_t)పొడవు_మూల్యం));
}
int 통신주소읽기(int 종단,struct 통신주소 *ఇమెయిల్,통신주소길이형 *పొడవు_మూల్యం) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ఇమెయిల్,(uintptr_t)పొడవు_మూల్యం,0,0,0));
}
int అనుసంధానించు_నెట్_వర్క్(int 종단,const struct 통신주소 *ఇమెయిల్,통신주소길이형 పొడవు_మూల్యం) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ఇమెయిల్,పొడవు_మూల్యం,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ఆమోదించు_నెట్_వర్క్_కనెక్షన్(int 종단,struct 통신주소 *ఇమెయిల్,통신주소길이형 *పొడవు_మూల్యం) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ఇమెయిల్,(uintptr_t)పొడవు_మూల్యం,0,0,0));
}

/* దస్త్రం 함수도 독립된 한국어 కార్యం_మూల్యం 심볼로 제공한다. */
int తెరువు_ఫైలు(const char *పాత్,int విధానం_మోడ్_3f5e5497,...) { return 결과검사(사용자호출(3,(uintptr_t)పాత్,విధానం_మోడ్_3f5e5497,0,0,0,0)); }
입출력결과형 파일자료읽기(int దస్త్రం,void *డేటా,size_t 개수) { return 결과검사(사용자호출(2,దస్త్రం,(uintptr_t)డేటా,개수,0,0,0)); }
입출력결과형 వ్రాయి_ఫైలు_డేటా(int దస్త్రం,const void *డేటా,size_t 개수) { return 결과검사(사용자호출(1,దస్త్రం,(uintptr_t)డేటా,개수,0,0,0)); }
int మూసివేయి_ఫైలు(int దస్త్రం) { return 결과검사(사용자호출(4,దస్త్రం,0,0,0,0,0)); }
ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి శోధించు_ఫైలు(int దస్త్రం,ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి 거리,int ప్రొజెక్ట్_మూలం) { return 결과검사(사용자호출(5,దస్త్రం,거리,ప్రొజెక్ట్_మూలం,0,0,0)); }
int తీసివెయ్యి_ఫైలు_ప్రవేశం_పేరు(const char *పాత్) { return 결과검사(사용자호출(11,(uintptr_t)పాత్,0,0,0,0,0)); }
int సెట్_ఫైలు_పొడవు(int దస్త్రం,ఫైలు_ఆఫ్_సెట్_టైప్_చేయండి పరిమాణం) { return 결과검사(사용자호출(10,దస్త్రం,పరిమాణం,0,0,0,0)); }
int 파일저장확정(int దస్త్రం) { return 결과검사(사용자호출(12,దస్త్రం,0,0,0,0,0)); }
int ఫైలు_పరిమాణం_మార్చు(int దస్త్రం) { return 결과검사(사용자호출(9,దస్త్రం,0,0,0,0,0)); }

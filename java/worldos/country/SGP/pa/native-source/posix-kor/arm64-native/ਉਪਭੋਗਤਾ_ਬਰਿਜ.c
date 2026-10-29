// 동일 ਪੰਜਾਬੀ 헤더를 사용하는 별도 EL0 ਪੁਸਤਕਾਲਾ. ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ਗਲਤ_ਕੋਡ;
int *pk_errno_location(void) { return &ਗਲਤ_ਕੋਡ; }
static intptr_t 결과검사(intptr_t ਮਾਪ) { if (ਮਾਪ < 0) { ਗਲਤ_ਕੋਡ = -ਮਾਪ; return -1; } return ਮਾਪ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ pk_lseek(int fd, ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* ਪੰਜਾਬੀ 공개 함수의 ਅਸਲ_ਸਮੱਗਰੀ EL0 구현. 구조체는 SVC에서 ਇਨਸਟੈਂਸ_ਕੀਮਤ·검증한다. */
int 통신종단점만들기(int ਪਤਾ_ਪਰਿਵਾਰ,int 통신방식,int ਸਥਾਂਨਤਰ_ਖਰੜਾ) {
    return 결과검사(사용자호출(32,ਪਤਾ_ਪਰਿਵਾਰ,통신방식,ਸਥਾਂਨਤਰ_ਖਰੜਾ,0,0,0));
}
int ਜ਼ਿਲਦਬੰਦੀ_ਪਤਾ(int 종단,const struct 통신주소 *ਪਤਾ,통신주소길이형 ਲੰਬਾਈ_ਕੀਮਤ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ਪਤਾ,ਲੰਬਾਈ_ਕੀਮਤ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ਸਮੱਗਰੀ,size_t 개수,int ਚੋਣ_ਕੀਮਤ,const struct 통신주소 *ਪਤਾ,통신주소길이형 ਲੰਬਾਈ_ਕੀਮਤ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ਸਮੱਗਰੀ,개수,ਚੋਣ_ਕੀਮਤ,(uintptr_t)ਪਤਾ,ਲੰਬਾਈ_ਕੀਮਤ));
}
intptr_t 자료전문받기(int 종단,void *ਸਮੱਗਰੀ,size_t 개수,int ਚੋਣ_ਕੀਮਤ,struct 통신주소 *ਪਤਾ,통신주소길이형 *ਲੰਬਾਈ_ਕੀਮਤ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ਸਮੱਗਰੀ,개수,ਚੋਣ_ਕੀਮਤ,(uintptr_t)ਪਤਾ,(uintptr_t)ਲੰਬਾਈ_ਕੀਮਤ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ਪਤਾ,통신주소길이형 *ਲੰਬਾਈ_ਕੀਮਤ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ਪਤਾ,(uintptr_t)ਲੰਬਾਈ_ਕੀਮਤ,0,0,0));
}
int ਕਨੈਕਟ_ਕਰੋ_ਨੈਟਵਰਕ(int 종단,const struct 통신주소 *ਪਤਾ,통신주소길이형 ਲੰਬਾਈ_ਕੀਮਤ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ਪਤਾ,ਲੰਬਾਈ_ਕੀਮਤ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ਸਵੀਕਾਰ_ਕਰੋ_ਨੈਟਵਰਕ_ਕਨੈਕਸ਼ਨ(int 종단,struct 통신주소 *ਪਤਾ,통신주소길이형 *ਲੰਬਾਈ_ਕੀਮਤ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ਪਤਾ,(uintptr_t)ਲੰਬਾਈ_ਕੀਮਤ,0,0,0));
}

/* ਫਾਇਲ 함수도 독립된 ਪੰਜਾਬੀ ਫੰਗਸ਼ਨ_ਕੀਮਤ 심볼로 제공한다. */
int ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ(const char *ਮਾਰਗ,int ਮੈਥਡ_ਮੋਡ,...) { return 결과검사(사용자호출(3,(uintptr_t)ਮਾਰਗ,ਮੈਥਡ_ਮੋਡ,0,0,0,0)); }
입출력결과형 파일자료읽기(int ਫਾਇਲ,void *ਸਮੱਗਰੀ,size_t 개수) { return 결과검사(사용자호출(2,ਫਾਇਲ,(uintptr_t)ਸਮੱਗਰੀ,개수,0,0,0)); }
입출력결과형 ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(int ਫਾਇਲ,const void *ਸਮੱਗਰੀ,size_t 개수) { return 결과검사(사용자호출(1,ਫਾਇਲ,(uintptr_t)ਸਮੱਗਰੀ,개수,0,0,0)); }
int ਬੰਦ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ(int ਫਾਇਲ) { return 결과검사(사용자호출(4,ਫਾਇਲ,0,0,0,0,0)); }
ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ ਸੀਕ_ਲਿਖਤ_ਪੱਤਰ(int ਫਾਇਲ,ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ 거리,int ਪ੍ਰੋਜੈਕਟ_ਰੂਟ) { return 결과검사(사용자호출(5,ਫਾਇਲ,거리,ਪ੍ਰੋਜੈਕਟ_ਰੂਟ,0,0,0)); }
int ਹਟਾਉਣਾ_ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ(const char *ਮਾਰਗ) { return 결과검사(사용자호출(11,(uintptr_t)ਮਾਰਗ,0,0,0,0,0)); }
int ਸੈਟ_ਲਿਖਤ_ਪੱਤਰ_ਲੰਬਾਈ(int ਫਾਇਲ,ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ ਆਕਾਰ) { return 결과검사(사용자호출(10,ਫਾਇਲ,ਆਕਾਰ,0,0,0,0)); }
int 파일저장확정(int ਫਾਇਲ) { return 결과검사(사용자호출(12,ਫਾਇਲ,0,0,0,0,0)); }
int ਲਿਖਤ_ਪੱਤਰ_ਆਕਾਰ(int ਫਾਇਲ) { return 결과검사(사용자호출(9,ਫਾਇਲ,0,0,0,0,0)); }

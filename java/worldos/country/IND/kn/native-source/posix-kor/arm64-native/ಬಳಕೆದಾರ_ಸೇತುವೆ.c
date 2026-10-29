// 동일 ಕನ್ನಡ 헤더를 사용하는 별도 EL0 ಲೈಬ್ರರಿ. ಕರ್ನಲ್_ಮೌಲ್ಯ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ದೋಷ_ಕೋಡ್;
int *pk_errno_location(void) { return &ದೋಷ_ಕೋಡ್; }
static intptr_t 결과검사(intptr_t ಮಾಪನ) { if (ಮಾಪನ < 0) { ದೋಷ_ಕೋಡ್ = -ಮಾಪನ; return -1; } return ಮಾಪನ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ pk_lseek(int fd, ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* ಕನ್ನಡ 공개 함수의 ನಿಜವಾದ_ಡೇಟಾ EL0 구현. 구조체는 SVC에서 ನಕಲಿಸು_ಮೌಲ್ಯ·검증한다. */
int 통신종단점만들기(int ಇಮೇಲ್_ಕುಟುಂಬ,int 통신방식,int ವರ್ಗಾವಣೆ_ಪ್ರೊಟೋಕಾಲ್) {
    return 결과검사(사용자호출(32,ಇಮೇಲ್_ಕುಟುಂಬ,통신방식,ವರ್ಗಾವಣೆ_ಪ್ರೊಟೋಕಾಲ್,0,0,0));
}
int ಬೈಂಡ್_ಮಾಡು_ಇಮೇಲ್(int 종단,const struct 통신주소 *ಇಮೇಲ್,통신주소길이형 ಉದ್ದ_ಮೌಲ್ಯ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ಇಮೇಲ್,ಉದ್ದ_ಮೌಲ್ಯ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ಡೇಟಾ,size_t 개수,int ಆಯ್ಕೆ_ಮೌಲ್ಯ,const struct 통신주소 *ಇಮೇಲ್,통신주소길이형 ಉದ್ದ_ಮೌಲ್ಯ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ಡೇಟಾ,개수,ಆಯ್ಕೆ_ಮೌಲ್ಯ,(uintptr_t)ಇಮೇಲ್,ಉದ್ದ_ಮೌಲ್ಯ));
}
intptr_t 자료전문받기(int 종단,void *ಡೇಟಾ,size_t 개수,int ಆಯ್ಕೆ_ಮೌಲ್ಯ,struct 통신주소 *ಇಮೇಲ್,통신주소길이형 *ಉದ್ದ_ಮೌಲ್ಯ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ಡೇಟಾ,개수,ಆಯ್ಕೆ_ಮೌಲ್ಯ,(uintptr_t)ಇಮೇಲ್,(uintptr_t)ಉದ್ದ_ಮೌಲ್ಯ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ಇಮೇಲ್,통신주소길이형 *ಉದ್ದ_ಮೌಲ್ಯ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ಇಮೇಲ್,(uintptr_t)ಉದ್ದ_ಮೌಲ್ಯ,0,0,0));
}
int ಕನೆಕ್ಟ್_ನೆಟ್_ವರ್ಕ್(int 종단,const struct 통신주소 *ಇಮೇಲ್,통신주소길이형 ಉದ್ದ_ಮೌಲ್ಯ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ಇಮೇಲ್,ಉದ್ದ_ಮೌಲ್ಯ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ಸಮ್ಮತಿಸು_ನೆಟ್_ವರ್ಕ್_ಸಂಪರ್ಕ(int 종단,struct 통신주소 *ಇಮೇಲ್,통신주소길이형 *ಉದ್ದ_ಮೌಲ್ಯ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ಇಮೇಲ್,(uintptr_t)ಉದ್ದ_ಮೌಲ್ಯ,0,0,0));
}

/* ಕಡತ 함수도 독립된 ಕನ್ನಡ ಕಾರ್ಯ_ಮೌಲ್ಯ 심볼로 제공한다. */
int ರಚಿಸು_ಫೈಲ್(const char *ಮಾರ್ಗ,int ವಿಧಾನ_ಮೋಡ್,...) { return 결과검사(사용자호출(3,(uintptr_t)ಮಾರ್ಗ,ವಿಧಾನ_ಮೋಡ್,0,0,0,0)); }
입출력결과형 파일자료읽기(int ಕಡತ,void *ಡೇಟಾ,size_t 개수) { return 결과검사(사용자호출(2,ಕಡತ,(uintptr_t)ಡೇಟಾ,개수,0,0,0)); }
입출력결과형 ಬರೆ_ಫೈಲ್_ಡೇಟಾ(int ಕಡತ,const void *ಡೇಟಾ,size_t 개수) { return 결과검사(사용자호출(1,ಕಡತ,(uintptr_t)ಡೇಟಾ,개수,0,0,0)); }
int ಮುಚ್ಚು_ಫೈಲ್(int ಕಡತ) { return 결과검사(사용자호출(4,ಕಡತ,0,0,0,0,0)); }
ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ ಸೀಕ್_ಫೈಲ್(int ಕಡತ,ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ 거리,int ಬಿಂಬಿಸು_ಮೂಲ) { return 결과검사(사용자호출(5,ಕಡತ,거리,ಬಿಂಬಿಸು_ಮೂಲ,0,0,0)); }
int ತೆಗೆ_ಫೈಲ್_ನಮೂದು_ಹೆಸರು(const char *ಮಾರ್ಗ) { return 결과검사(사용자호출(11,(uintptr_t)ಮಾರ್ಗ,0,0,0,0,0)); }
int ಸೆಟ್_ಫೈಲ್_ಉದ್ದ(int ಕಡತ,ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ ಗಾತ್ರ) { return 결과검사(사용자호출(10,ಕಡತ,ಗಾತ್ರ,0,0,0,0)); }
int 파일저장확정(int ಕಡತ) { return 결과검사(사용자호출(12,ಕಡತ,0,0,0,0,0)); }
int ಫೈಲ್_ಗಾತ್ರಿಸು(int ಕಡತ) { return 결과검사(사용자호출(9,ಕಡತ,0,0,0,0,0)); }

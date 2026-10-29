// 동일 ትግርኛ 헤더를 사용하는 별도 EL0 ቤት_ንባብ. ፍረ_ዋጋ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int 오류값;
int *pk_errno_location(void) { return &오류값; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { 오류값 = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ፋይል_ሽፋን_ዓይነት pk_lseek(int fd, ፋይል_ሽፋን_ዓይነት offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ፋይል_ሽፋን_ዓይነት size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* ትግርኛ 공개 함수의 ትኽክለኛ_ሓበሬታ EL0 구현. 구조체는 SVC에서 ቅዳሕ_ዋጋ·검증한다. */
int 통신종단점만들기(int ኣድራሻ_ስድራቤት,int 통신방식,int ምስጋር_ኣገባብ) {
    return 결과검사(사용자호출(32,ኣድራሻ_ስድራቤት,통신방식,ምስጋር_ኣገባብ,0,0,0));
}
int ኣጣምር_ኣድራሻ(int 종단,const struct 통신주소 *ኣድራሻ,통신주소길이형 ንውሓት_ዋጋ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ኣድራሻ,ንውሓት_ዋጋ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ሓበሬታ,size_t 개수,int ምሩጽ_ዋጋ,const struct 통신주소 *ኣድራሻ,통신주소길이형 ንውሓት_ዋጋ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ሓበሬታ,개수,ምሩጽ_ዋጋ,(uintptr_t)ኣድራሻ,ንውሓት_ዋጋ));
}
intptr_t 자료전문받기(int 종단,void *ሓበሬታ,size_t 개수,int ምሩጽ_ዋጋ,struct 통신주소 *ኣድራሻ,통신주소길이형 *ንውሓት_ዋጋ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ሓበሬታ,개수,ምሩጽ_ዋጋ,(uintptr_t)ኣድራሻ,(uintptr_t)ንውሓት_ዋጋ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ኣድራሻ,통신주소길이형 *ንውሓት_ዋጋ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ኣድራሻ,(uintptr_t)ንውሓት_ዋጋ,0,0,0));
}
int ኣላግብ_ማሕበራዊ_ኔትወርክ(int 종단,const struct 통신주소 *ኣድራሻ,통신주소길이형 ንውሓት_ዋጋ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ኣድራሻ,ንውሓት_ዋጋ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ተቐበል_ርክብ_ኔትወርክ(int 종단,struct 통신주소 *ኣድራሻ,통신주소길이형 *ንውሓት_ዋጋ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ኣድራሻ,(uintptr_t)ንውሓት_ዋጋ,0,0,0));
}

/* ፋይል 함수도 독립된 ትግርኛ ተግባር_ዋጋ 심볼로 제공한다. */
int ክፈት_ፋይል(const char *መገዲ,int ሜላ_ኹነት,...) { return 결과검사(사용자호출(3,(uintptr_t)መገዲ,ሜላ_ኹነት,0,0,0,0)); }
입출력결과형 파일자료읽기(int ፋይል,void *ሓበሬታ,size_t 개수) { return 결과검사(사용자호출(2,ፋይል,(uintptr_t)ሓበሬታ,개수,0,0,0)); }
입출력결과형 ጸሓፍ_ፋይል_ሓበሬታ(int ፋይል,const void *ሓበሬታ,size_t 개수) { return 결과검사(사용자호출(1,ፋይል,(uintptr_t)ሓበሬታ,개수,0,0,0)); }
int ዕጸው_ፋይል(int ፋይል) { return 결과검사(사용자호출(4,ፋይል,0,0,0,0,0)); }
ፋይል_ሽፋን_ዓይነት መድለዪ_ፋይል(int ፋይል,ፋይል_ሽፋን_ዓይነት 거리,int 기준) { return 결과검사(사용자호출(5,ፋይል,거리,기준,0,0,0)); }
int ኣልግስ_ፋይል_ምእታው_ሽም(const char *መገዲ) { return 결과검사(사용자호출(11,(uintptr_t)መገዲ,0,0,0,0,0)); }
int እኩብ_ፋይል_ንውሓት(int ፋይል,ፋይል_ሽፋን_ዓይነት መጠን) { return 결과검사(사용자호출(10,ፋይል,መጠን,0,0,0,0)); }
int 파일저장확정(int ፋይል) { return 결과검사(사용자호출(12,ፋይል,0,0,0,0,0)); }
int ፋይል_መጠን(int ፋይል) { return 결과검사(사용자호출(9,ፋይል,0,0,0,0,0)); }

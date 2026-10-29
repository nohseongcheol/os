// 동일 አማርኛ 헤더를 사용하는 별도 EL0 ማከማቻ_ስፍራ. ዓንኳር_እሴት 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int የስሕተት_ኮድ;
int *pk_errno_location(void) { return &የስሕተት_ኮድ; }
static intptr_t 결과검사(intptr_t ልኬት) { if (ልኬት < 0) { የስሕተት_ኮድ = -ልኬት; return -1; } return ልኬት; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ፋይል_ዝንፍ_ተይብ pk_lseek(int fd, ፋይል_ዝንፍ_ተይብ offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ፋይል_ዝንፍ_ተይብ size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* አማርኛ 공개 함수의 ትክክለኛ_ውሂብ EL0 구현. 구조체는 SVC에서 ቅዳ_እሴት·검증한다. */
int 통신종단점만들기(int አድራሻ_ቤተሰብ,int 통신방식,int ትልልፍ_ፕሮቶኮል) {
    return 결과검사(사용자호출(32,አድራሻ_ቤተሰብ,통신방식,ትልልፍ_ፕሮቶኮል,0,0,0));
}
int አጣምር_አድራሻ(int 종단,const struct 통신주소 *አድራሻ,통신주소길이형 ርዝመት_እሴት) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)አድራሻ,ርዝመት_እሴት,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ውሂብ,size_t 개수,int የተመረጠ_እሴት,const struct 통신주소 *አድራሻ,통신주소길이형 ርዝመት_እሴት) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ውሂብ,개수,የተመረጠ_እሴት,(uintptr_t)አድራሻ,ርዝመት_እሴት));
}
intptr_t 자료전문받기(int 종단,void *ውሂብ,size_t 개수,int የተመረጠ_እሴት,struct 통신주소 *አድራሻ,통신주소길이형 *ርዝመት_እሴት) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ውሂብ,개수,የተመረጠ_እሴት,(uintptr_t)አድራሻ,(uintptr_t)ርዝመት_እሴት));
}
int 통신주소읽기(int 종단,struct 통신주소 *አድራሻ,통신주소길이형 *ርዝመት_እሴት) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)አድራሻ,(uintptr_t)ርዝመት_እሴት,0,0,0));
}
int አገናኝ_መረብ(int 종단,const struct 통신주소 *አድራሻ,통신주소길이형 ርዝመት_እሴት) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)አድራሻ,ርዝመት_እሴት,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ተቀበል_የአውታረመረብ_ግንኙነት(int 종단,struct 통신주소 *አድራሻ,통신주소길이형 *ርዝመት_እሴት) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)አድራሻ,(uintptr_t)ርዝመት_እሴት,0,0,0));
}

/* ፋይል 함수도 독립된 አማርኛ ተግባር_እሴት 심볼로 제공한다. */
int ክፈት_ፋይል(const char *መተላለፊያ,int ስልት_ሁነታ,...) { return 결과검사(사용자호출(3,(uintptr_t)መተላለፊያ,ስልት_ሁነታ,0,0,0,0)); }
입출력결과형 파일자료읽기(int ፋይል,void *ውሂብ,size_t 개수) { return 결과검사(사용자호출(2,ፋይል,(uintptr_t)ውሂብ,개수,0,0,0)); }
입출력결과형 ጻፍ_ፋይል_ውሂብ(int ፋይል,const void *ውሂብ,size_t 개수) { return 결과검사(사용자호출(1,ፋይል,(uintptr_t)ውሂብ,개수,0,0,0)); }
int ዝጋ_ፋይል(int ፋይል) { return 결과검사(사용자호출(4,ፋይል,0,0,0,0,0)); }
ፋይል_ዝንፍ_ተይብ ፈልግ_ፋይል(int ፋይል,ፋይል_ዝንፍ_ተይብ 거리,int አሳይ_ስር) { return 결과검사(사용자호출(5,ፋይል,거리,አሳይ_ስር,0,0,0)); }
int አስወግድ_ፋይል_ምዝግብ_ስም(const char *መተላለፊያ) { return 결과검사(사용자호출(11,(uintptr_t)መተላለፊያ,0,0,0,0,0)); }
int ስብስብ_ፋይል_ርዝመት(int ፋይል,ፋይል_ዝንፍ_ተይብ መጠን) { return 결과검사(사용자호출(10,ፋይል,መጠን,0,0,0,0)); }
int 파일저장확정(int ፋይል) { return 결과검사(사용자호출(12,ፋይል,0,0,0,0,0)); }
int ፋይል_መጠን_ቀይር(int ፋይል) { return 결과검사(사용자호출(9,ፋይል,0,0,0,0,0)); }

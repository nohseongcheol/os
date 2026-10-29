// 동일 한국어 헤더를 사용하는 별도 EL0 ibi_ìpamọ́. kánẹ́ẹ̀lì_iye 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kóòdù_àṣìṣe;
int *pk_errno_location(void) { return &kóòdù_àṣìṣe; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { kóòdù_àṣìṣe = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fáìlì_Ìtayọ_irú pk_lseek(int fd, fáìlì_Ìtayọ_irú offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fáìlì_Ìtayọ_irú size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 gangan_détà EL0 구현. 구조체는 SVC에서 ṣẹ̀dà_iye·검증한다. */
int 통신종단점만들기(int àdírẹ́ẹ̀sì_Ẹbí,int 통신방식,int ṣàgbélọ_ìfẹnukò) {
    return 결과검사(사용자호출(32,àdírẹ́ẹ̀sì_Ẹbí,통신방식,ṣàgbélọ_ìfẹnukò,0,0,0));
}
int BIND_àdírẹ́ẹ̀sì(int 종단,const struct 통신주소 *àdírẹ́ẹ̀sì,통신주소길이형 gígùn_iye) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)àdírẹ́ẹ̀sì,gígùn_iye,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *détà,size_t 개수,int ẹ̀yàn_iye,const struct 통신주소 *àdírẹ́ẹ̀sì,통신주소길이형 gígùn_iye) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)détà,개수,ẹ̀yàn_iye,(uintptr_t)àdírẹ́ẹ̀sì,gígùn_iye));
}
intptr_t 자료전문받기(int 종단,void *détà,size_t 개수,int ẹ̀yàn_iye,struct 통신주소 *àdírẹ́ẹ̀sì,통신주소길이형 *gígùn_iye) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)détà,개수,ẹ̀yàn_iye,(uintptr_t)àdírẹ́ẹ̀sì,(uintptr_t)gígùn_iye));
}
int 통신주소읽기(int 종단,struct 통신주소 *àdírẹ́ẹ̀sì,통신주소길이형 *gígùn_iye) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)àdírẹ́ẹ̀sì,(uintptr_t)gígùn_iye,0,0,0));
}
int SOMỌ́_Alásopọ̀(int 종단,const struct 통신주소 *àdírẹ́ẹ̀sì,통신주소길이형 gígùn_iye) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)àdírẹ́ẹ̀sì,gígùn_iye,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int gbà_ìsopọ̀_alásopọ̀(int 종단,struct 통신주소 *àdírẹ́ẹ̀sì,통신주소길이형 *gígùn_iye) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)àdírẹ́ẹ̀sì,(uintptr_t)gígùn_iye,0,0,0));
}

/* Fáìlì 함수도 독립된 한국어 ÀKÀNṢEFỌMÚLÀ_iye 심볼로 제공한다. */
int ṣí_fáìlì(const char *ọ̀nà,int ìlànà_móòdù,...) { return 결과검사(사용자호출(3,(uintptr_t)ọ̀nà,ìlànà_móòdù,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fáìlì,void *détà,size_t 개수) { return 결과검사(사용자호출(2,Fáìlì,(uintptr_t)détà,개수,0,0,0)); }
입출력결과형 kọ_fáìlì_détà(int Fáìlì,const void *détà,size_t 개수) { return 결과검사(사용자호출(1,Fáìlì,(uintptr_t)détà,개수,0,0,0)); }
int pa_dé_fáìlì(int Fáìlì) { return 결과검사(사용자호출(4,Fáìlì,0,0,0,0,0)); }
fáìlì_Ìtayọ_irú ṣàwárí_fáìlì(int Fáìlì,fáìlì_Ìtayọ_irú 거리,int 기준) { return 결과검사(사용자호출(5,Fáìlì,거리,기준,0,0,0)); }
int ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ(const char *ọ̀nà) { return 결과검사(사용자호출(11,(uintptr_t)ọ̀nà,0,0,0,0,0)); }
int ọ̀wọ̀_fáìlì_gígùn(int Fáìlì,fáìlì_Ìtayọ_irú Ìwọ̀n) { return 결과검사(사용자호출(10,Fáìlì,Ìwọ̀n,0,0,0,0)); }
int 파일저장확정(int Fáìlì) { return 결과검사(사용자호출(12,Fáìlì,0,0,0,0,0)); }
int fáìlì_ìwọn(int Fáìlì) { return 결과검사(사용자호출(9,Fáìlì,0,0,0,0,0)); }

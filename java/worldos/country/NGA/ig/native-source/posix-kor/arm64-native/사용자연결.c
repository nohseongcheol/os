// 동일 한국어 헤더를 사용하는 별도 EL0 ọbaakwụkwọ. mkpụrụobī_kọmpùta_valuu 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int koòdu_nzi_mmehìè;
int *pk_errno_location(void) { return &koòdu_nzi_mmehìè; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { koòdu_nzi_mmehìè = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ọbọakwụkwọ_Nnokwata_pinye pk_lseek(int fd, ọbọakwụkwọ_Nnokwata_pinye offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ọbọakwụkwọ_Nnokwata_pinye size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ǹdịnezie_datà EL0 구현. 구조체는 SVC에서 ṅomie_valuu·검증한다. */
int 통신종단점만들기(int àdreèsì_Ezinụlọ,int 통신방식,int dògharịa_iwùùsòrò) {
    return 결과검사(사용자호출(32,àdreèsì_Ezinụlọ,통신방식,dògharịa_iwùùsòrò,0,0,0));
}
int JIKỌNYE_àdreèsì(int 종단,const struct 통신주소 *àdreèsì,통신주소길이형 ogologo_valuu) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)àdreèsì,ogologo_valuu,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *datà,size_t 개수,int ebenhọrọ_valuu,const struct 통신주소 *àdreèsì,통신주소길이형 ogologo_valuu) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)datà,개수,ebenhọrọ_valuu,(uintptr_t)àdreèsì,ogologo_valuu));
}
intptr_t 자료전문받기(int 종단,void *datà,size_t 개수,int ebenhọrọ_valuu,struct 통신주소 *àdreèsì,통신주소길이형 *ogologo_valuu) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)datà,개수,ebenhọrọ_valuu,(uintptr_t)àdreèsì,(uintptr_t)ogologo_valuu));
}
int 통신주소읽기(int 종단,struct 통신주소 *àdreèsì,통신주소길이형 *ogologo_valuu) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)àdreèsì,(uintptr_t)ogologo_valuu,0,0,0));
}
int JIKỌ_Netwọọkụ(int 종단,const struct 통신주소 *àdreèsì,통신주소길이형 ogologo_valuu) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)àdreèsì,ogologo_valuu,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int nabata_njikọ_netwọk(int 종단,struct 통신주소 *àdreèsì,통신주소길이형 *ogologo_valuu) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)àdreèsì,(uintptr_t)ogologo_valuu,0,0,0));
}

/* Faịlụ 함수도 독립된 한국어 ọrụ_valuu 심볼로 제공한다. */
int mepee_ọbọakwụkwọ(const char *ụzọ_ozi,int usoro_moòdù,...) { return 결과검사(사용자호출(3,(uintptr_t)ụzọ_ozi,usoro_moòdù,0,0,0,0)); }
입출력결과형 파일자료읽기(int Faịlụ,void *datà,size_t 개수) { return 결과검사(사용자호출(2,Faịlụ,(uintptr_t)datà,개수,0,0,0)); }
입출력결과형 dee_ọbọakwụkwọ_datà(int Faịlụ,const void *datà,size_t 개수) { return 결과검사(사용자호출(1,Faịlụ,(uintptr_t)datà,개수,0,0,0)); }
int mmechi_ọbọakwụkwọ(int Faịlụ) { return 결과검사(사용자호출(4,Faịlụ,0,0,0,0,0)); }
ọbọakwụkwọ_Nnokwata_pinye ọchịchọ_ọbọakwụkwọ(int Faịlụ,ọbọakwụkwọ_Nnokwata_pinye 거리,int 기준) { return 결과검사(사용자호출(5,Faịlụ,거리,기준,0,0,0)); }
int wepụ_ọbọakwụkwọ_ndebà_akara_ahà(const char *ụzọ_ozi) { return 결과검사(사용자호출(11,(uintptr_t)ụzọ_ozi,0,0,0,0,0)); }
int Seti_ọbọakwụkwọ_ogologo(int Faịlụ,ọbọakwụkwọ_Nnokwata_pinye Ụhara) { return 결과검사(사용자호출(10,Faịlụ,Ụhara,0,0,0,0)); }
int 파일저장확정(int Faịlụ) { return 결과검사(사용자호출(12,Faịlụ,0,0,0,0,0)); }
int ọbọakwụkwọ_ụha(int Faịlụ) { return 결과검사(사용자호출(9,Faịlụ,0,0,0,0,0)); }

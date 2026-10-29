// 동일 한국어 헤더를 사용하는 별도 EL0 laburare. Kwara_Daraja 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int Lambar_sirri_ta_kuskure;
int *pk_errno_location(void) { return &Lambar_sirri_ta_kuskure; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { Lambar_sirri_ta_kuskure = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fayil_Sassautawa_rubuta pk_lseek(int fd, Fayil_Sassautawa_rubuta offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fayil_Sassautawa_rubuta size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 Na_hakika_Tarin_bayani EL0 구현. 구조체는 SVC에서 Kwafi_Daraja·검증한다. */
int 통신종단점만들기(int imel_Iyali,int 통신방식,int Gusar_da_furotukol) {
    return 결과검사(사용자호출(32,imel_Iyali,통신방식,Gusar_da_furotukol,0,0,0));
}
int BIND_imel(int 종단,const struct 통신주소 *imel,통신주소길이형 Tsawo_Daraja) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)imel,Tsawo_Daraja,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *Tarin_bayani,size_t 개수,int bangaren_zaɓi_Daraja,const struct 통신주소 *imel,통신주소길이형 Tsawo_Daraja) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)Tarin_bayani,개수,bangaren_zaɓi_Daraja,(uintptr_t)imel,Tsawo_Daraja));
}
intptr_t 자료전문받기(int 종단,void *Tarin_bayani,size_t 개수,int bangaren_zaɓi_Daraja,struct 통신주소 *imel,통신주소길이형 *Tsawo_Daraja) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)Tarin_bayani,개수,bangaren_zaɓi_Daraja,(uintptr_t)imel,(uintptr_t)Tsawo_Daraja));
}
int 통신주소읽기(int 종단,struct 통신주소 *imel,통신주소길이형 *Tsawo_Daraja) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)imel,(uintptr_t)Tsawo_Daraja,0,0,0));
}
int HAƊI_Hanyar_sadarwa(int 종단,const struct 통신주소 *imel,통신주소길이형 Tsawo_Daraja) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)imel,Tsawo_Daraja,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int 통신연결받기(int 종단,struct 통신주소 *imel,통신주소길이형 *Tsawo_Daraja) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)imel,(uintptr_t)Tsawo_Daraja,0,0,0));
}

/* Fayil 함수도 독립된 한국어 AIKI_Daraja 심볼로 제공한다. */
int buɗe_Fayil(const char *Hanyar_shiga,int tsari_yanayin_aiki,...) { return 결과검사(사용자호출(3,(uintptr_t)Hanyar_shiga,tsari_yanayin_aiki,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fayil,void *Tarin_bayani,size_t 개수) { return 결과검사(사용자호출(2,Fayil,(uintptr_t)Tarin_bayani,개수,0,0,0)); }
입출력결과형 Rubuta_Fayil_Tarin_bayani(int Fayil,const void *Tarin_bayani,size_t 개수) { return 결과검사(사용자호출(1,Fayil,(uintptr_t)Tarin_bayani,개수,0,0,0)); }
int Rufe_Fayil(int Fayil) { return 결과검사(사용자호출(4,Fayil,0,0,0,0,0)); }
Fayil_Sassautawa_rubuta binciko_Fayil(int Fayil,Fayil_Sassautawa_rubuta 거리,int 기준) { return 결과검사(사용자호출(5,Fayil,거리,기준,0,0,0)); }
int Cire_Fayil_Mashigar_bayanai_Suna(const char *Hanyar_shiga) { return 결과검사(사용자호출(11,(uintptr_t)Hanyar_shiga,0,0,0,0,0)); }
int zubi_Fayil_Tsawo(int Fayil,Fayil_Sassautawa_rubuta Girma) { return 결과검사(사용자호출(10,Fayil,Girma,0,0,0,0)); }
int 파일저장확정(int Fayil) { return 결과검사(사용자호출(12,Fayil,0,0,0,0,0)); }
int Fayil_girma(int Fayil) { return 결과검사(사용자호출(9,Fayil,0,0,0,0,0)); }

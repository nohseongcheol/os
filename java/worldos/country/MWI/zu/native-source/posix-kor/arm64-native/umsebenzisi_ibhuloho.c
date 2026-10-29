// 동일 Isi_Zulu 헤더를 사용하는 별도 EL0 umtapo. ikhenela_inani 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ikhodi_yephutha;
int *pk_errno_location(void) { return &ikhodi_yephutha; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { ikhodi_yephutha = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ifayela_I_ofisethi_thayipha pk_lseek(int fd, ifayela_I_ofisethi_thayipha offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ifayela_I_ofisethi_thayipha size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Isi_Zulu 공개 함수의 ulwazi_ngokwenzekile_imininingwane EL0 구현. 구조체는 SVC에서 kopisha_inani·검증한다. */
int 통신종단점만들기(int ikheli_Umndeni,int 통신방식,int dlulisa_iphrothokholi) {
    return 결과검사(사용자호출(32,ikheli_Umndeni,통신방식,dlulisa_iphrothokholi,0,0,0));
}
int i_BIND_ikheli(int 종단,const struct 통신주소 *ikheli,통신주소길이형 ubude_inani) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ikheli,ubude_inani,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *imininingwane,size_t 개수,int okukhethiwe_inani,const struct 통신주소 *ikheli,통신주소길이형 ubude_inani) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)imininingwane,개수,okukhethiwe_inani,(uintptr_t)ikheli,ubude_inani));
}
intptr_t 자료전문받기(int 종단,void *imininingwane,size_t 개수,int okukhethiwe_inani,struct 통신주소 *ikheli,통신주소길이형 *ubude_inani) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)imininingwane,개수,okukhethiwe_inani,(uintptr_t)ikheli,(uintptr_t)ubude_inani));
}
int 통신주소읽기(int 종단,struct 통신주소 *ikheli,통신주소길이형 *ubude_inani) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ikheli,(uintptr_t)ubude_inani,0,0,0));
}
int xhuma_iNethiwekhi(int 종단,const struct 통신주소 *ikheli,통신주소길이형 ubude_inani) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ikheli,ubude_inani,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int yamukela_uxhumano_lwenethiwekhi(int 종단,struct 통신주소 *ikheli,통신주소길이형 *ubude_inani) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ikheli,(uintptr_t)ubude_inani,0,0,0));
}

/* Ihele 함수도 독립된 Isi_Zulu umsebenzi_inani 심볼로 제공한다. */
int vula_ifayela(const char *Indlela_2,int indlela_inqubo,...) { return 결과검사(사용자호출(3,(uintptr_t)Indlela_2,indlela_inqubo,0,0,0,0)); }
입출력결과형 파일자료읽기(int Ihele,void *imininingwane,size_t 개수) { return 결과검사(사용자호출(2,Ihele,(uintptr_t)imininingwane,개수,0,0,0)); }
입출력결과형 bhala_ifayela_imininingwane(int Ihele,const void *imininingwane,size_t 개수) { return 결과검사(사용자호출(1,Ihele,(uintptr_t)imininingwane,개수,0,0,0)); }
int vala_ifayela(int Ihele) { return 결과검사(사용자호출(4,Ihele,0,0,0,0,0)); }
ifayela_I_ofisethi_thayipha cinga_ifayela(int Ihele,ifayela_I_ofisethi_thayipha 거리,int 기준) { return 결과검사(사용자호출(5,Ihele,거리,기준,0,0,0)); }
int khipha_ifayela_okufakwayo_igama(const char *Indlela_2) { return 결과검사(사용자호출(11,(uintptr_t)Indlela_2,0,0,0,0,0)); }
int isethi_ifayela_ubude(int Ihele,ifayela_I_ofisethi_thayipha Ubungako) { return 결과검사(사용자호출(10,Ihele,Ubungako,0,0,0,0)); }
int 파일저장확정(int Ihele) { return 결과검사(사용자호출(12,Ihele,0,0,0,0,0)); }
int ifayela_linganisa(int Ihele) { return 결과검사(사용자호출(9,Ihele,0,0,0,0,0)); }

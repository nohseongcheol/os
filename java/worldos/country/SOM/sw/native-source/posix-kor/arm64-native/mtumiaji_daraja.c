// 동일 한국어 헤더를 사용하는 별도 EL0 maktaba. kiini_thamani_0611a8a8 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int msimbo_wa_kosa;
int *pk_errno_location(void) { return &msimbo_wa_kosa; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { msimbo_wa_kosa = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
faili_Chipua_aina pk_lseek(int fd, faili_Chipua_aina offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, faili_Chipua_aina size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 halisi_data EL0 구현. 구조체는 SVC에서 mfano_thamani·검증한다. */
int 통신종단점만들기(int anwani_Familia,int 통신방식,int hamisha_itifaki) {
    return 결과검사(사용자호출(32,anwani_Familia,통신방식,hamisha_itifaki,0,0,0));
}
int FUNGA_anwani(int 종단,const struct 통신주소 *anwani,통신주소길이형 urefu_thamani) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)anwani,urefu_thamani,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *data,size_t 개수,int uteuzi_thamani,const struct 통신주소 *anwani,통신주소길이형 urefu_thamani) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)data,개수,uteuzi_thamani,(uintptr_t)anwani,urefu_thamani));
}
intptr_t 자료전문받기(int 종단,void *data,size_t 개수,int uteuzi_thamani,struct 통신주소 *anwani,통신주소길이형 *urefu_thamani) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)data,개수,uteuzi_thamani,(uintptr_t)anwani,(uintptr_t)urefu_thamani));
}
int 통신주소읽기(int 종단,struct 통신주소 *anwani,통신주소길이형 *urefu_thamani) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)anwani,(uintptr_t)urefu_thamani,0,0,0));
}
int UNGANISHA_Mtandao(int 종단,const struct 통신주소 *anwani,통신주소길이형 urefu_thamani) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)anwani,urefu_thamani,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int kubali_muunganisho_wa_mtandao(int 종단,struct 통신주소 *anwani,통신주소길이형 *urefu_thamani) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)anwani,(uintptr_t)urefu_thamani,0,0,0));
}

/* faili 함수도 독립된 한국어 KITENDAKAZI_thamani 심볼로 제공한다. */
int unda_faili(const char *njia,int mbinu_hali_tumizi,...) { return 결과검사(사용자호출(3,(uintptr_t)njia,mbinu_hali_tumizi,0,0,0,0)); }
입출력결과형 파일자료읽기(int faili,void *data,size_t 개수) { return 결과검사(사용자호출(2,faili,(uintptr_t)data,개수,0,0,0)); }
입출력결과형 andika_faili_data(int faili,const void *data,size_t 개수) { return 결과검사(사용자호출(1,faili,(uintptr_t)data,개수,0,0,0)); }
int funga_faili(int faili) { return 결과검사(사용자호출(4,faili,0,0,0,0,0)); }
faili_Chipua_aina tafuta_faili(int faili,faili_Chipua_aina 거리,int 기준) { return 결과검사(사용자호출(5,faili,거리,기준,0,0,0)); }
int ondoa_faili_ingizo_jina(const char *njia) { return 결과검사(사용자호출(11,(uintptr_t)njia,0,0,0,0,0)); }
int seti_faili_urefu(int faili,faili_Chipua_aina panga_ukubwa) { return 결과검사(사용자호출(10,faili,panga_ukubwa,0,0,0,0)); }
int 파일저장확정(int faili) { return 결과검사(사용자호출(12,faili,0,0,0,0,0)); }
int faili_panga_ukubwa(int faili) { return 결과검사(사용자호출(9,faili,0,0,0,0,0)); }

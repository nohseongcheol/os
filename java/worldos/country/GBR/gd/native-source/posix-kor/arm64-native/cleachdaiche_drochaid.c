// 동일 한국어 헤더를 사용하는 별도 EL0 leabhar_lann. eitean_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int mearachd_CODE;
int *pk_errno_location(void) { return &mearachd_CODE; }
static intptr_t 결과검사(intptr_t tomhas) { if (tomhas < 0) { mearachd_CODE = -tomhas; return -1; } return tomhas; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
faidhle_OFFSET_TYPE pk_lseek(int fd, faidhle_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, faidhle_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 dearbh_dàta EL0 구현. 구조체는 SVC에서 ionstans_VALUE·검증한다. */
int 통신종단점만들기(int ADDRESS_teaghlach,int 통신방식,int tar_chur_pròtacal) {
    return 결과검사(사용자호출(32,ADDRESS_teaghlach,통신방식,tar_chur_pròtacal,0,0,0));
}
int BIND_ADDRESS(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 faid_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ADDRESS,faid_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *dàta,size_t nì_COUNT,int taghadh_VALUE,const struct 통신주소 *ADDRESS,통신주소길이형 faid_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)dàta,nì_COUNT,taghadh_VALUE,(uintptr_t)ADDRESS,faid_VALUE));
}
intptr_t 자료전문받기(int 종단,void *dàta,size_t nì_COUNT,int taghadh_VALUE,struct 통신주소 *ADDRESS,통신주소길이형 *faid_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)dàta,nì_COUNT,taghadh_VALUE,(uintptr_t)ADDRESS,(uintptr_t)faid_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *faid_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ADDRESS,(uintptr_t)faid_VALUE,0,0,0));
}
int CONNECT_lìonra(int 종단,const struct 통신주소 *ADDRESS,통신주소길이형 faid_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ADDRESS,faid_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int A_feitheamh_COUNT) {
    return 결과검사(사용자호출(38,종단,A_feitheamh_COUNT,0,0,0,0));
}
int gabh_ris_ceangal_lìonraidh(int 종단,struct 통신주소 *ADDRESS,통신주소길이형 *faid_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ADDRESS,(uintptr_t)faid_VALUE,0,0,0));
}

/* faidhle 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int fosgail_faidhle(const char *Slighe,int dòigh_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)Slighe,dòigh_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int faidhle,void *dàta,size_t nì_COUNT) { return 결과검사(사용자호출(2,faidhle,(uintptr_t)dàta,nì_COUNT,0,0,0)); }
입출력결과형 sgrìobh_faidhle_dàta(int faidhle,const void *dàta,size_t nì_COUNT) { return 결과검사(사용자호출(1,faidhle,(uintptr_t)dàta,nì_COUNT,0,0,0)); }
int dùin_faidhle(int faidhle) { return 결과검사(사용자호출(4,faidhle,0,0,0,0,0)); }
faidhle_OFFSET_TYPE sir_faidhle(int faidhle,faidhle_OFFSET_TYPE 거리,int tilg_freumh) { return 결과검사(사용자호출(5,faidhle,거리,tilg_freumh,0,0,0)); }
int thoir_air_falbh_faidhle_cur_a_steach_ainm(const char *Slighe) { return 결과검사(사용자호출(11,(uintptr_t)Slighe,0,0,0,0,0)); }
int seata_faidhle_faid(int faidhle,faidhle_OFFSET_TYPE atharraich_am_meud) { return 결과검사(사용자호출(10,faidhle,atharraich_am_meud,0,0,0,0)); }
int 파일저장확정(int faidhle) { return 결과검사(사용자호출(12,faidhle,0,0,0,0,0)); }
int faidhle_atharraich_am_meud(int faidhle) { return 결과검사(사용자호출(9,faidhle,0,0,0,0,0)); }

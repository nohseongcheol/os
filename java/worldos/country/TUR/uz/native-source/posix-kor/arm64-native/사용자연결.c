// 동일 한국어 헤더를 사용하는 별도 EL0 kutubxona. o_zak_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int xato_kodi;
int *pk_errno_location(void) { return &xato_kodi; }
static intptr_t 결과검사(intptr_t o_lchov) { if (o_lchov < 0) { xato_kodi = -o_lchov; return -1; } return o_lchov; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fayl_OFFSET_TYPE pk_lseek(int fd, fayl_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fayl_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 real_ma_lumotlar EL0 구현. 구조체는 SVC에서 namuna_VALUE·검증한다. */
int 통신종단점만들기(int manzil_Oila,int 통신방식,int uzatish_bayonnoma) {
    return 결과검사(사용자호출(32,manzil_Oila,통신방식,uzatish_bayonnoma,0,0,0));
}
int BOG_LAMOQ_manzil(int 종단,const struct 통신주소 *manzil,통신주소길이형 uzunlik_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)manzil,uzunlik_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ma_lumotlar,size_t element_COUNT,int tanlanma_VALUE,const struct 통신주소 *manzil,통신주소길이형 uzunlik_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ma_lumotlar,element_COUNT,tanlanma_VALUE,(uintptr_t)manzil,uzunlik_VALUE));
}
intptr_t 자료전문받기(int 종단,void *ma_lumotlar,size_t element_COUNT,int tanlanma_VALUE,struct 통신주소 *manzil,통신주소길이형 *uzunlik_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ma_lumotlar,element_COUNT,tanlanma_VALUE,(uintptr_t)manzil,(uintptr_t)uzunlik_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *manzil,통신주소길이형 *uzunlik_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)manzil,(uintptr_t)uzunlik_VALUE,0,0,0));
}
int ulash_Tarmoq(int 종단,const struct 통신주소 *manzil,통신주소길이형 uzunlik_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)manzil,uzunlik_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Kutish_COUNT) {
    return 결과검사(사용자호출(38,종단,Kutish_COUNT,0,0,0,0));
}
int qabul_qilish_tarmoq_ulanishi(int 종단,struct 통신주소 *manzil,통신주소길이형 *uzunlik_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)manzil,(uintptr_t)uzunlik_VALUE,0,0,0));
}

/* Fayl 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int ochmoq_fayl(const char *yo_l,int uslub_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)yo_l,uslub_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fayl,void *ma_lumotlar,size_t element_COUNT) { return 결과검사(사용자호출(2,Fayl,(uintptr_t)ma_lumotlar,element_COUNT,0,0,0)); }
입출력결과형 yozmoq_fayl_ma_lumotlar(int Fayl,const void *ma_lumotlar,size_t element_COUNT) { return 결과검사(사용자호출(1,Fayl,(uintptr_t)ma_lumotlar,element_COUNT,0,0,0)); }
int yopmoq_fayl(int Fayl) { return 결과검사(사용자호출(4,Fayl,0,0,0,0,0)); }
fayl_OFFSET_TYPE izlamoq_fayl(int Fayl,fayl_OFFSET_TYPE 거리,int Project_ildiz) { return 결과검사(사용자호출(5,Fayl,거리,Project_ildiz,0,0,0)); }
int olib_tashlamoq_fayl_kiritish_nom(const char *yo_l) { return 결과검사(사용자호출(11,(uintptr_t)yo_l,0,0,0,0,0)); }
int to_plam_fayl_uzunlik(int Fayl,fayl_OFFSET_TYPE Hajmi) { return 결과검사(사용자호출(10,Fayl,Hajmi,0,0,0,0)); }
int 파일저장확정(int Fayl) { return 결과검사(사용자호출(12,Fayl,0,0,0,0,0)); }
int fayl_o_lcham(int Fayl) { return 결과검사(사용자호출(9,Fayl,0,0,0,0,0)); }

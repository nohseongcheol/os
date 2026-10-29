// 동일 한국어 헤더를 사용하는 별도 EL0 kitabxana. nüvə_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int səhvin_kodu;
int *pk_errno_location(void) { return &səhvin_kodu; }
static intptr_t 결과검사(intptr_t ölçü) { if (ölçü < 0) { səhvin_kodu = -ölçü; return -1; } return ölçü; }
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

/* 한국어 공개 함수의 faktiki_verilənlər EL0 구현. 구조체는 SVC에서 nümunə_VALUE·검증한다. */
int 통신종단점만들기(int ünvan_Ailə,int 통신방식,int ötürmə_protokol) {
    return 결과검사(사용자호출(32,ünvan_Ailə,통신방식,ötürmə_protokol,0,0,0));
}
int BIND_ünvan(int 종단,const struct 통신주소 *ünvan,통신주소길이형 uzunluq_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ünvan,uzunluq_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *verilənlər,size_t element_COUNT,int seçilmiş_sahə_VALUE,const struct 통신주소 *ünvan,통신주소길이형 uzunluq_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)verilənlər,element_COUNT,seçilmiş_sahə_VALUE,(uintptr_t)ünvan,uzunluq_VALUE));
}
intptr_t 자료전문받기(int 종단,void *verilənlər,size_t element_COUNT,int seçilmiş_sahə_VALUE,struct 통신주소 *ünvan,통신주소길이형 *uzunluq_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)verilənlər,element_COUNT,seçilmiş_sahə_VALUE,(uintptr_t)ünvan,(uintptr_t)uzunluq_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *ünvan,통신주소길이형 *uzunluq_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ünvan,(uintptr_t)uzunluq_VALUE,0,0,0));
}
int QOŞUN_Şəbəkə(int 종단,const struct 통신주소 *ünvan,통신주소길이형 uzunluq_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ünvan,uzunluq_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Gözləyir_COUNT) {
    return 결과검사(사용자호출(38,종단,Gözləyir_COUNT,0,0,0,0));
}
int qəbul_et_şəbəkə_bağlantısı(int 종단,struct 통신주소 *ünvan,통신주소길이형 *uzunluq_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ünvan,(uintptr_t)uzunluq_VALUE,0,0,0));
}

/* FAYL 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int açmaq_fayl(const char *Cığır,int metod_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)Cığır,metod_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int FAYL,void *verilənlər,size_t element_COUNT) { return 결과검사(사용자호출(2,FAYL,(uintptr_t)verilənlər,element_COUNT,0,0,0)); }
입출력결과형 yazmaq_fayl_verilənlər(int FAYL,const void *verilənlər,size_t element_COUNT) { return 결과검사(사용자호출(1,FAYL,(uintptr_t)verilənlər,element_COUNT,0,0,0)); }
int bağlamaq_fayl(int FAYL) { return 결과검사(사용자호출(4,FAYL,0,0,0,0,0)); }
fayl_OFFSET_TYPE axtarmaq_fayl(int FAYL,fayl_OFFSET_TYPE 거리,int Project_kök) { return 결과검사(사용자호출(5,FAYL,거리,Project_kök,0,0,0)); }
int silmək_fayl_daxiletmə_ad(const char *Cığır) { return 결과검사(사용자호출(11,(uintptr_t)Cığır,0,0,0,0,0)); }
int Dəst_fayl_uzunluq(int FAYL,fayl_OFFSET_TYPE Böyüklük) { return 결과검사(사용자호출(10,FAYL,Böyüklük,0,0,0,0)); }
int 파일저장확정(int FAYL) { return 결과검사(사용자호출(12,FAYL,0,0,0,0,0)); }
int fayl_ölçünü_dəyişmək(int FAYL) { return 결과검사(사용자호출(9,FAYL,0,0,0,0,0)); }

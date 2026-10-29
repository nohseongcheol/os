// 동일 Lietuvių 헤더를 사용하는 별도 EL0 biblioteka. branduolys_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int klaidos_kodas;
int *pk_errno_location(void) { return &klaidos_kodas; }
static intptr_t 결과검사(intptr_t REZULTATAS) { if (REZULTATAS < 0) { klaidos_kodas = -REZULTATAS; return -1; } return REZULTATAS; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Failas_OFFSET_TYPE pk_lseek(int fd, Failas_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Failas_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Lietuvių 공개 함수의 faktinis_duomenys EL0 구현. 구조체는 SVC에서 kopijuoti_VALUE·검증한다. */
int kurti_dalyvis(int ADDRESS_Šeima,int 통신방식,int perduoti_protokolas) {
    return 결과검사(사용자호출(32,ADDRESS_Šeima,통신방식,perduoti_protokolas,0,0,0));
}
int BIND_ADDRESS(int dalyvis,const struct 통신주소 *ADDRESS,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,dalyvis,(uintptr_t)ADDRESS,길이,0,0,0));
}
intptr_t siųsti_paketų_kelio_schema_duomenys(int dalyvis,const void *duomenys,size_t prekė_COUNT,int žymėjimas_VALUE,const struct 통신주소 *ADDRESS,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,dalyvis,(uintptr_t)duomenys,prekė_COUNT,žymėjimas_VALUE,(uintptr_t)ADDRESS,길이));
}
intptr_t gauti_paketų_kelio_schema_duomenys(int dalyvis,void *duomenys,size_t prekė_COUNT,int žymėjimas_VALUE,struct 통신주소 *ADDRESS,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,dalyvis,(uintptr_t)duomenys,prekė_COUNT,žymėjimas_VALUE,(uintptr_t)ADDRESS,(uintptr_t)길이));
}
int 통신주소읽기(int dalyvis,struct 통신주소 *ADDRESS,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,dalyvis,(uintptr_t)ADDRESS,(uintptr_t)길이,0,0,0));
}
int ryšys_tinklas(int dalyvis,const struct 통신주소 *ADDRESS,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,dalyvis,(uintptr_t)ADDRESS,길이,0,0,0));
}
int 통신연결기다리기(int dalyvis,int Vis_dar_laukiu_COUNT) {
    return 결과검사(사용자호출(38,dalyvis,Vis_dar_laukiu_COUNT,0,0,0,0));
}
int priimti_tinklo_ryšys(int dalyvis,struct 통신주소 *ADDRESS,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,dalyvis,(uintptr_t)ADDRESS,(uintptr_t)길이,0,0,0));
}

/* Failas 함수도 독립된 Lietuvių FUNCTION_VALUE 심볼로 제공한다. */
int kurti_Failas(const char *KELIAS,int metodas_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)KELIAS,metodas_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Failas,void *duomenys,size_t prekė_COUNT) { return 결과검사(사용자호출(2,Failas,(uintptr_t)duomenys,prekė_COUNT,0,0,0)); }
입출력결과형 rašymas_Failas_duomenys(int Failas,const void *duomenys,size_t prekė_COUNT) { return 결과검사(사용자호출(1,Failas,(uintptr_t)duomenys,prekė_COUNT,0,0,0)); }
int Uždaryti_Failas(int Failas) { return 결과검사(사용자호출(4,Failas,0,0,0,0,0)); }
Failas_OFFSET_TYPE ieškoti_Failas(int Failas,Failas_OFFSET_TYPE 거리,int Project_šaknis) { return 결과검사(사용자호출(5,Failas,거리,Project_šaknis,0,0,0)); }
int pašalinti_Failas_įrašas_pavadinimas(const char *KELIAS) { return 결과검사(사용자호출(11,(uintptr_t)KELIAS,0,0,0,0,0)); }
int 파일길이정하기(int Failas,Failas_OFFSET_TYPE Dydis) { return 결과검사(사용자호출(10,Failas,Dydis,0,0,0,0)); }
int vykdymas_failų_saugykla(int Failas) { return 결과검사(사용자호출(12,Failas,0,0,0,0,0)); }
int failo_dydis(int Failas) { return 결과검사(사용자호출(9,Failas,0,0,0,0,0)); }

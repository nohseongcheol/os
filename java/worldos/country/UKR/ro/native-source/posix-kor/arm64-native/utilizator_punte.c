// 동일 Română 헤더를 사용하는 별도 EL0 bibliotecă. nucleu_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int cod_de_eroare;
int *pk_errno_location(void) { return &cod_de_eroare; }
static intptr_t 결과검사(intptr_t KR) { if (KR < 0) { cod_de_eroare = -KR; return -1; } return KR; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fișier_OFFSET_Tip pk_lseek(int fd, Fișier_OFFSET_Tip offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fișier_OFFSET_Tip size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Română 공개 함수의 real_date EL0 구현. 구조체는 SVC에서 copia_VALUE·검증한다. */
int crea_participant(int adresa_Familie,int 통신방식,int Transfer_protocol) {
    return 결과검사(사용자호출(32,adresa_Familie,통신방식,Transfer_protocol,0,0,0));
}
int BIND_adresa(int participant,const struct 통신주소 *adresa,통신주소길이형 lungime_VALUE) {
    return 결과검사(사용자호출(33,participant,(uintptr_t)adresa,lungime_VALUE,0,0,0));
}
intptr_t trimite_diagramă_informații_date(int participant,const void *date,size_t element_COUNT,int selecție_VALUE,const struct 통신주소 *adresa,통신주소길이형 lungime_VALUE) {
    return 결과검사(사용자호출(34,participant,(uintptr_t)date,element_COUNT,selecție_VALUE,(uintptr_t)adresa,lungime_VALUE));
}
intptr_t primi_diagramă_informații_date(int participant,void *date,size_t element_COUNT,int selecție_VALUE,struct 통신주소 *adresa,통신주소길이형 *lungime_VALUE) {
    return 결과검사(사용자호출(35,participant,(uintptr_t)date,element_COUNT,selecție_VALUE,(uintptr_t)adresa,(uintptr_t)lungime_VALUE));
}
int 통신주소읽기(int participant,struct 통신주소 *adresa,통신주소길이형 *lungime_VALUE) {
    return 결과검사(사용자호출(36,participant,(uintptr_t)adresa,(uintptr_t)lungime_VALUE,0,0,0));
}
int conecta_rețea(int participant,const struct 통신주소 *adresa,통신주소길이형 lungime_VALUE) {
    return 결과검사(사용자호출(37,participant,(uintptr_t)adresa,lungime_VALUE,0,0,0));
}
int 통신연결기다리기(int participant,int Aștept_COUNT) {
    return 결과검사(사용자호출(38,participant,Aștept_COUNT,0,0,0,0));
}
int accepta_conexiune_rețea(int participant,struct 통신주소 *adresa,통신주소길이형 *lungime_VALUE) {
    return 결과검사(사용자호출(39,participant,(uintptr_t)adresa,(uintptr_t)lungime_VALUE,0,0,0));
}

/* Fișier 함수도 독립된 Română funcție_VALUE 심볼로 제공한다. */
int crea_Fișier(const char *Cale,int metodă_mod,...) { return 결과검사(사용자호출(3,(uintptr_t)Cale,metodă_mod,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fișier,void *date,size_t element_COUNT) { return 결과검사(사용자호출(2,Fișier,(uintptr_t)date,element_COUNT,0,0,0)); }
입출력결과형 scriere_Fișier_date(int Fișier,const void *date,size_t element_COUNT) { return 결과검사(사용자호출(1,Fișier,(uintptr_t)date,element_COUNT,0,0,0)); }
int închide_Fișier(int Fișier) { return 결과검사(사용자호출(4,Fișier,0,0,0,0,0)); }
Fișier_OFFSET_Tip căuta_Fișier(int Fișier,Fișier_OFFSET_Tip 거리,int Project_rădăcină) { return 결과검사(사용자호출(5,Fișier,거리,Project_rădăcină,0,0,0)); }
int elimina_Fișier_intrare_nume(const char *Cale) { return 결과검사(사용자호출(11,(uintptr_t)Cale,0,0,0,0,0)); }
int set_Fișier_lungime(int Fișier,Fișier_OFFSET_Tip Mărime) { return 결과검사(사용자호출(10,Fișier,Mărime,0,0,0,0)); }
int comitere_Fișiere(int Fișier) { return 결과검사(사용자호출(12,Fișier,0,0,0,0,0)); }
int dimensiune_fișier(int Fișier) { return 결과검사(사용자호출(9,Fișier,0,0,0,0,0)); }

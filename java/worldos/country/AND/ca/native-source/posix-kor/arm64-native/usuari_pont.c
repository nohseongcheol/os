// 동일 Català 헤더를 사용하는 별도 EL0 biblioteca. nucli_VALOR 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int error_CODI;
int *pk_errno_location(void) { return &error_CODI; }
static intptr_t 결과검사(intptr_t RESULTAT) { if (RESULTAT < 0) { error_CODI = -RESULTAT; return -1; } return RESULTAT; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
arxiu_DESPLAÇAMENT_TIPUS pk_lseek(int fd, arxiu_DESPLAÇAMENT_TIPUS offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, arxiu_DESPLAÇAMENT_TIPUS size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Català 공개 함수의 real_dades EL0 구현. 구조체는 SVC에서 copiar_VALOR·검증한다. */
int Crear_extrem(int ADREÇA_Família,int 통신방식,int transferir_protocol) {
    return 결과검사(사용자호출(32,ADREÇA_Família,통신방식,transferir_protocol,0,0,0));
}
int enllaçar_ADREÇA(int extrem,const struct 통신주소 *Adreça,통신주소길이형 durada_VALOR) {
    return 결과검사(사용자호출(33,extrem,(uintptr_t)Adreça,durada_VALOR,0,0,0));
}
intptr_t 자료전문보내기(int extrem,const void *dades,size_t element_COMPT,int selecció_VALOR,const struct 통신주소 *Adreça,통신주소길이형 durada_VALOR) {
    return 결과검사(사용자호출(34,extrem,(uintptr_t)dades,element_COMPT,selecció_VALOR,(uintptr_t)Adreça,durada_VALOR));
}
intptr_t 자료전문받기(int extrem,void *dades,size_t element_COMPT,int selecció_VALOR,struct 통신주소 *Adreça,통신주소길이형 *durada_VALOR) {
    return 결과검사(사용자호출(35,extrem,(uintptr_t)dades,element_COMPT,selecció_VALOR,(uintptr_t)Adreça,(uintptr_t)durada_VALOR));
}
int 통신주소읽기(int extrem,struct 통신주소 *Adreça,통신주소길이형 *durada_VALOR) {
    return 결과검사(사용자호출(36,extrem,(uintptr_t)Adreça,(uintptr_t)durada_VALOR,0,0,0));
}
int CONNECTA_xarxa(int extrem,const struct 통신주소 *Adreça,통신주소길이형 durada_VALOR) {
    return 결과검사(사용자호출(37,extrem,(uintptr_t)Adreça,durada_VALOR,0,0,0));
}
int 통신연결기다리기(int extrem,int Esperant_COMPT) {
    return 결과검사(사용자호출(38,extrem,Esperant_COMPT,0,0,0,0));
}
int acceptar_connexió_de_xarxa(int extrem,struct 통신주소 *Adreça,통신주소길이형 *durada_VALOR) {
    return 결과검사(사용자호출(39,extrem,(uintptr_t)Adreça,(uintptr_t)durada_VALOR,0,0,0));
}

/* Fitxer 함수도 독립된 Català FUNCIÓ_VALOR 심볼로 제공한다. */
int crear_arxiu(const char *Camí,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)Camí,방식,0,0,0,0)); }
입출력결과형 tancar_arxiu_dades(int Fitxer,void *dades,size_t element_COMPT) { return 결과검사(사용자호출(2,Fitxer,(uintptr_t)dades,element_COMPT,0,0,0)); }
입출력결과형 escriure_arxiu_dades(int Fitxer,const void *dades,size_t element_COMPT) { return 결과검사(사용자호출(1,Fitxer,(uintptr_t)dades,element_COMPT,0,0,0)); }
int Tanca_arxiu(int Fitxer) { return 결과검사(사용자호출(4,Fitxer,0,0,0,0,0)); }
arxiu_DESPLAÇAMENT_TIPUS cercar_arxiu(int Fitxer,arxiu_DESPLAÇAMENT_TIPUS 거리,int Project_rel) { return 결과검사(사용자호출(5,Fitxer,거리,Project_rel,0,0,0)); }
int suprimir_arxiu_introducció_nom(const char *Camí) { return 결과검사(사용자호출(11,(uintptr_t)Camí,0,0,0,0,0)); }
int conjunt_arxiu_durada(int Fitxer,arxiu_DESPLAÇAMENT_TIPUS Mida) { return 결과검사(사용자호출(10,Fitxer,Mida,0,0,0,0)); }
int 파일저장확정(int Fitxer) { return 결과검사(사용자호출(12,Fitxer,0,0,0,0,0)); }
int arxiu_canviar_la_mida(int Fitxer) { return 결과검사(사용자호출(9,Fitxer,0,0,0,0,0)); }

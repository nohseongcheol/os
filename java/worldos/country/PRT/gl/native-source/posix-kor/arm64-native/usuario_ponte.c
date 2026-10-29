// 동일 Galego 헤더를 사용하는 별도 EL0 biblioteca. kernel_VALOR 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int código_de_erro;
int *pk_errno_location(void) { return &código_de_erro; }
static intptr_t 결과검사(intptr_t RESULTANTE) { if (RESULTANTE < 0) { código_de_erro = -RESULTANTE; return -1; } return RESULTANTE; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Ficheiro_DESPRAZAMENTO_TIPO pk_lseek(int fd, Ficheiro_DESPRAZAMENTO_TIPO offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Ficheiro_DESPRAZAMENTO_TIPO size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Galego 공개 함수의 real_datos EL0 구현. 구조체는 SVC에서 copiar_VALOR·검증한다. */
int crear_extremo(int ENDEREZO_Familia,int 통신방식,int Transferir_protocolo) {
    return 결과검사(사용자호출(32,ENDEREZO_Familia,통신방식,Transferir_protocolo,0,0,0));
}
int ligar_ENDEREZO(int extremo,const struct 통신주소 *ENDEREZO,통신주소길이형 duración_VALOR) {
    return 결과검사(사용자호출(33,extremo,(uintptr_t)ENDEREZO,duración_VALOR,0,0,0));
}
intptr_t 자료전문보내기(int extremo,const void *datos,size_t elemento_CONTAR,int selección_VALOR,const struct 통신주소 *ENDEREZO,통신주소길이형 duración_VALOR) {
    return 결과검사(사용자호출(34,extremo,(uintptr_t)datos,elemento_CONTAR,selección_VALOR,(uintptr_t)ENDEREZO,duración_VALOR));
}
intptr_t 자료전문받기(int extremo,void *datos,size_t elemento_CONTAR,int selección_VALOR,struct 통신주소 *ENDEREZO,통신주소길이형 *duración_VALOR) {
    return 결과검사(사용자호출(35,extremo,(uintptr_t)datos,elemento_CONTAR,selección_VALOR,(uintptr_t)ENDEREZO,(uintptr_t)duración_VALOR));
}
int 통신주소읽기(int extremo,struct 통신주소 *ENDEREZO,통신주소길이형 *duración_VALOR) {
    return 결과검사(사용자호출(36,extremo,(uintptr_t)ENDEREZO,(uintptr_t)duración_VALOR,0,0,0));
}
int CONECTAR_Rede(int extremo,const struct 통신주소 *ENDEREZO,통신주소길이형 duración_VALOR) {
    return 결과검사(사용자호출(37,extremo,(uintptr_t)ENDEREZO,duración_VALOR,0,0,0));
}
int 통신연결기다리기(int extremo,int Agardando_CONTAR) {
    return 결과검사(사용자호출(38,extremo,Agardando_CONTAR,0,0,0,0));
}
int aceptar_conexión_de_rede(int extremo,struct 통신주소 *ENDEREZO,통신주소길이형 *duración_VALOR) {
    return 결과검사(사용자호출(39,extremo,(uintptr_t)ENDEREZO,(uintptr_t)duración_VALOR,0,0,0));
}

/* Ficheiro 함수도 독립된 Galego FUNCIÓN_VALOR 심볼로 제공한다. */
int abrir_Ficheiro(const char *CAMIÑO,int 방식,...) { return 결과검사(사용자호출(3,(uintptr_t)CAMIÑO,방식,0,0,0,0)); }
입출력결과형 파일자료읽기(int Ficheiro,void *datos,size_t elemento_CONTAR) { return 결과검사(사용자호출(2,Ficheiro,(uintptr_t)datos,elemento_CONTAR,0,0,0)); }
입출력결과형 escribir_Ficheiro_datos(int Ficheiro,const void *datos,size_t elemento_CONTAR) { return 결과검사(사용자호출(1,Ficheiro,(uintptr_t)datos,elemento_CONTAR,0,0,0)); }
int peche_Ficheiro(int Ficheiro) { return 결과검사(사용자호출(4,Ficheiro,0,0,0,0,0)); }
Ficheiro_DESPRAZAMENTO_TIPO buscar_Ficheiro(int Ficheiro,Ficheiro_DESPRAZAMENTO_TIPO 거리,int Project_raíz) { return 결과검사(사용자호출(5,Ficheiro,거리,Project_raíz,0,0,0)); }
int eliminar_Ficheiro_introdución_nome(const char *CAMIÑO) { return 결과검사(사용자호출(11,(uintptr_t)CAMIÑO,0,0,0,0,0)); }
int conxunto_Ficheiro_duración(int Ficheiro,Ficheiro_DESPRAZAMENTO_TIPO Tamaño) { return 결과검사(사용자호출(10,Ficheiro,Tamaño,0,0,0,0)); }
int 파일저장확정(int Ficheiro) { return 결과검사(사용자호출(12,Ficheiro,0,0,0,0,0)); }
int 파일크기(int Ficheiro) { return 결과검사(사용자호출(9,Ficheiro,0,0,0,0,0)); }

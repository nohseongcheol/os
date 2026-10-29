// 동일 한국어 헤더를 사용하는 별도 EL0 Bibliothéik. Kernel_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int Feelercode;
int *pk_errno_location(void) { return &Feelercode; }
static intptr_t 결과검사(intptr_t Mooss) { if (Mooss < 0) { Feelercode = -Mooss; return -1; } return Mooss; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Fichier_OFFSET_TYPE pk_lseek(int fd, Fichier_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Fichier_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 aktuell_Daten EL0 구현. 구조체는 SVC에서 Instanz_VALUE·검증한다. */
int 통신종단점만들기(int Adress_Famill,int 통신방식,int Transfer_Protokoll) {
    return 결과검사(사용자호출(32,Adress_Famill,통신방식,Transfer_Protokoll,0,0,0));
}
int BANNEN_Adress(int 종단,const struct 통신주소 *Adress,통신주소길이형 Längt_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)Adress,Längt_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *Daten,size_t Element_COUNT,int Auswiel_VALUE,const struct 통신주소 *Adress,통신주소길이형 Längt_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)Daten,Element_COUNT,Auswiel_VALUE,(uintptr_t)Adress,Längt_VALUE));
}
intptr_t 자료전문받기(int 종단,void *Daten,size_t Element_COUNT,int Auswiel_VALUE,struct 통신주소 *Adress,통신주소길이형 *Längt_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)Daten,Element_COUNT,Auswiel_VALUE,(uintptr_t)Adress,(uintptr_t)Längt_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *Adress,통신주소길이형 *Längt_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)Adress,(uintptr_t)Längt_VALUE,0,0,0));
}
int Verbannen_Reseau(int 종단,const struct 통신주소 *Adress,통신주소길이형 Längt_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)Adress,Längt_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Waart_COUNT) {
    return 결과검사(사용자호출(38,종단,Waart_COUNT,0,0,0,0));
}
int acceptéieren_Netzwierksverbindung(int 종단,struct 통신주소 *Adress,통신주소길이형 *Längt_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)Adress,(uintptr_t)Längt_VALUE,0,0,0));
}

/* Fichier 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int ariichten_Fichier(const char *Wee,int Method_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)Wee,Method_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fichier,void *Daten,size_t Element_COUNT) { return 결과검사(사용자호출(2,Fichier,(uintptr_t)Daten,Element_COUNT,0,0,0)); }
입출력결과형 schreiwen_Fichier_Daten(int Fichier,const void *Daten,size_t Element_COUNT) { return 결과검사(사용자호출(1,Fichier,(uintptr_t)Daten,Element_COUNT,0,0,0)); }
int Clôture_Fichier(int Fichier) { return 결과검사(사용자호출(4,Fichier,0,0,0,0,0)); }
Fichier_OFFSET_TYPE sichen_Fichier(int Fichier,Fichier_OFFSET_TYPE 거리,int projezéieren_Racinn) { return 결과검사(사용자호출(5,Fichier,거리,projezéieren_Racinn,0,0,0)); }
int ewechhuelen_Fichier_Agab_Numm(const char *Wee) { return 결과검사(사용자호출(11,(uintptr_t)Wee,0,0,0,0,0)); }
int Saz_Fichier_Längt(int Fichier,Fichier_OFFSET_TYPE d_Gréisst_veränneren) { return 결과검사(사용자호출(10,Fichier,d_Gréisst_veränneren,0,0,0,0)); }
int 파일저장확정(int Fichier) { return 결과검사(사용자호출(12,Fichier,0,0,0,0,0)); }
int Fichier_d_Gréisst_veränneren(int Fichier) { return 결과검사(사용자호출(9,Fichier,0,0,0,0,0)); }

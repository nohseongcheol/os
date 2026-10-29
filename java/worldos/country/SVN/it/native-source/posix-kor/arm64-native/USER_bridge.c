// 동일 Italiano 헤더를 사용하는 별도 EL0 Catalogo. kernel_VALORE 직접 호출판과 혼합 금지.
#include "File_ABI.h"
#include "호출.h"
#include "rete_ABI.h"
static int codice_errore;
int *pk_errno_location(void) { return &codice_errore; }
static intptr_t 결과검사(intptr_t risultato) { if (risultato < 0) { codice_errore = -risultato; return -1; } return risultato; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
File_SCARTO_TIPO pk_lseek(int fd, File_SCARTO_TIPO offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, File_SCARTO_TIPO size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Italiano 공개 함수의 effettivo_dati EL0 implementazione. 구조체는 SVC에서 copiare_VALORE·검증한다. */
int Crea_endpoint(int e_mail_serie,int comunicazione_MODA,int trasferire_protocollo) {
    return 결과검사(사용자호출(32,e_mail_serie,comunicazione_MODA,trasferire_protocollo,0,0,0));
}
int BIND_e_mail(int endpoint,const struct socket_e_mail *e_mail,socket_e_mail_durata_TIPO durata_VALORE) {
    return 결과검사(사용자호출(33,endpoint,(uintptr_t)e_mail,durata_VALORE,0,0,0));
}
intptr_t inviare_datagramma_dati(int endpoint,const void *dati,size_t articolo_CONTA_NUMERI,int selezione_VALORE,const struct socket_e_mail *e_mail,socket_e_mail_durata_TIPO durata_VALORE) {
    return 결과검사(사용자호출(34,endpoint,(uintptr_t)dati,articolo_CONTA_NUMERI,selezione_VALORE,(uintptr_t)e_mail,durata_VALORE));
}
intptr_t ricevere_datagramma_dati(int endpoint,void *dati,size_t articolo_CONTA_NUMERI,int selezione_VALORE,struct socket_e_mail *e_mail,socket_e_mail_durata_TIPO *durata_VALORE) {
    return 결과검사(사용자호출(35,endpoint,(uintptr_t)dati,articolo_CONTA_NUMERI,selezione_VALORE,(uintptr_t)e_mail,(uintptr_t)durata_VALORE));
}
int 통신주소읽기(int endpoint,struct socket_e_mail *e_mail,socket_e_mail_durata_TIPO *durata_VALORE) {
    return 결과검사(사용자호출(36,endpoint,(uintptr_t)e_mail,(uintptr_t)durata_VALORE,0,0,0));
}
int CONNETTI_rete(int endpoint,const struct socket_e_mail *e_mail,socket_e_mail_durata_TIPO durata_VALORE) {
    return 결과검사(사용자호출(37,endpoint,(uintptr_t)e_mail,durata_VALORE,0,0,0));
}
int 통신연결기다리기(int endpoint,int In_attesa_CONTA_NUMERI) {
    return 결과검사(사용자호출(38,endpoint,In_attesa_CONTA_NUMERI,0,0,0,0));
}
int accettare_connessione_di_rete(int endpoint,struct socket_e_mail *e_mail,socket_e_mail_durata_TIPO *durata_VALORE) {
    return 결과검사(사용자호출(39,endpoint,(uintptr_t)e_mail,(uintptr_t)durata_VALORE,0,0,0));
}

/* file 함수도 독립된 Italiano FUNZIONE_VALORE 심볼로 제공한다. */
int aperto_File(const char *percorso,int metodo_MODA,...) { return 결과검사(사용자호출(3,(uintptr_t)percorso,metodo_MODA,0,0,0,0)); }
입출력결과형 파일자료읽기(int file,void *dati,size_t articolo_CONTA_NUMERI) { return 결과검사(사용자호출(2,file,(uintptr_t)dati,articolo_CONTA_NUMERI,0,0,0)); }
입출력결과형 scrivere_File_dati(int file,const void *dati,size_t articolo_CONTA_NUMERI) { return 결과검사(사용자호출(1,file,(uintptr_t)dati,articolo_CONTA_NUMERI,0,0,0)); }
int Chiudi_File(int file) { return 결과검사(사용자호출(4,file,0,0,0,0,0)); }
File_SCARTO_TIPO cercare_File(int file,File_SCARTO_TIPO 거리,int azione_radice) { return 결과검사(사용자호출(5,file,거리,azione_radice,0,0,0)); }
int rimuovere_File_voce_nome(const char *percorso) { return 결과검사(사용자호출(11,(uintptr_t)percorso,0,0,0,0,0)); }
int set_File_durata(int file,File_SCARTO_TIPO Dimensione) { return 결과검사(사용자호출(10,file,Dimensione,0,0,0,0)); }
int commit_File(int file) { return 결과검사(사용자호출(12,file,0,0,0,0,0)); }
int dimensioni_del_file(int file) { return 결과검사(사용자호출(9,file,0,0,0,0,0)); }

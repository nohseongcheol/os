// 동일 Português 헤더를 사용하는 별도 EL0 biblioteca. kernel_VALOR 직접 호출판과 혼합 금지.
#include "Arquivo_ABI.h"
#include "호출.h"
#include "rede_ABI.h"
static int código_de_erro;
int *pk_errno_location(void) { return &código_de_erro; }
static intptr_t 결과검사(intptr_t resultado) { if (resultado < 0) { código_de_erro = -resultado; return -1; } return resultado; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Arquivo_DESLOC_TIPO pk_lseek(int fd, Arquivo_DESLOC_TIPO offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Arquivo_DESLOC_TIPO size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Português 공개 함수의 real_dados EL0 implementação. 구조체는 SVC에서 copiar_VALOR·검증한다. */
int Criar_empresa(int email_Família,int comunicação_MODO,int Transferir_protocolo) {
    return 결과검사(사용자호출(32,email_Família,comunicação_MODO,Transferir_protocolo,0,0,0));
}
int BIND_email(int empresa,const struct soquete_email *Endereço,soquete_email_duração_TIPO duração_VALOR) {
    return 결과검사(사용자호출(33,empresa,(uintptr_t)Endereço,duração_VALOR,0,0,0));
}
intptr_t enviar_datagrama_dados(int empresa,const void *dados,size_t item_CONT_NÚM,int seleção_VALOR,const struct soquete_email *Endereço,soquete_email_duração_TIPO duração_VALOR) {
    return 결과검사(사용자호출(34,empresa,(uintptr_t)dados,item_CONT_NÚM,seleção_VALOR,(uintptr_t)Endereço,duração_VALOR));
}
intptr_t receber_datagrama_dados(int empresa,void *dados,size_t item_CONT_NÚM,int seleção_VALOR,struct soquete_email *Endereço,soquete_email_duração_TIPO *duração_VALOR) {
    return 결과검사(사용자호출(35,empresa,(uintptr_t)dados,item_CONT_NÚM,seleção_VALOR,(uintptr_t)Endereço,(uintptr_t)duração_VALOR));
}
int leitura_soquete_email(int empresa,struct soquete_email *Endereço,soquete_email_duração_TIPO *duração_VALOR) {
    return 결과검사(사용자호출(36,empresa,(uintptr_t)Endereço,(uintptr_t)duração_VALOR,0,0,0));
}
int Conexão_rede(int empresa,const struct soquete_email *Endereço,soquete_email_duração_TIPO duração_VALOR) {
    return 결과검사(사용자호출(37,empresa,(uintptr_t)Endereço,duração_VALOR,0,0,0));
}
int 통신연결기다리기(int empresa,int Esperando_CONT_NÚM) {
    return 결과검사(사용자호출(38,empresa,Esperando_CONT_NÚM,0,0,0,0));
}
int aceitar_conexão_de_rede(int empresa,struct soquete_email *Endereço,soquete_email_duração_TIPO *duração_VALOR) {
    return 결과검사(사용자호출(39,empresa,(uintptr_t)Endereço,(uintptr_t)duração_VALOR,0,0,0));
}

/* ficheiro 함수도 독립된 Português FUNÇÃO_VALOR 심볼로 제공한다. */
int abrir_Arquivo(const char *caminho,int método_MODO,...) { return 결과검사(사용자호출(3,(uintptr_t)caminho,método_MODO,0,0,0,0)); }
입출력결과형 leitura_Arquivo_dados(int ficheiro,void *dados,size_t item_CONT_NÚM) { return 결과검사(사용자호출(2,ficheiro,(uintptr_t)dados,item_CONT_NÚM,0,0,0)); }
입출력결과형 gravar_Arquivo_dados(int ficheiro,const void *dados,size_t item_CONT_NÚM) { return 결과검사(사용자호출(1,ficheiro,(uintptr_t)dados,item_CONT_NÚM,0,0,0)); }
int Close_Arquivo(int ficheiro) { return 결과검사(사용자호출(4,ficheiro,0,0,0,0,0)); }
Arquivo_DESLOC_TIPO busca_Arquivo(int ficheiro,Arquivo_DESLOC_TIPO 거리,int ação_raiz) { return 결과검사(사용자호출(5,ficheiro,거리,ação_raiz,0,0,0)); }
int remover_Arquivo_entrada_nome(const char *caminho) { return 결과검사(사용자호출(11,(uintptr_t)caminho,0,0,0,0,0)); }
int set_Arquivo_duração(int ficheiro,Arquivo_DESLOC_TIPO Tamanho) { return 결과검사(사용자호출(10,ficheiro,Tamanho,0,0,0,0)); }
int commit_Arquivos(int ficheiro) { return 결과검사(사용자호출(12,ficheiro,0,0,0,0,0)); }
int tamanho_do_arquivo(int ficheiro) { return 결과검사(사용자호출(9,ficheiro,0,0,0,0,0)); }

#ifndef JKOROS_ARM64_NETWORK_H
#define JKOROS_ARM64_NETWORK_H
#include "Arquivo_ABI.h"
/* 표준 ABI는 기존 executável·externo_VALOR 코드와 연결할 때만 사용한다. */
#define AF_INET 2
#define SOCK_STREAM 1
#define SOCK_DGRAM 2
#define IPPROTO_UDP 17
#define IPPROTO_TCP 6
#define INADDR_LOOPBACK 0x7f000001u
typedef uint32_t pk_socklen_t;
struct pk_sockaddr { uint16_t sa_family; unsigned char sa_data[14]; };
struct pk_in_addr { uint32_t s_addr; };
struct pk_sockaddr_in { uint16_t sin_family, sin_port; struct pk_in_addr sin_addr; unsigned char sin_zero[8]; };

/* Português 자료형은 macro_VALOR 별칭이 아닌 독립된 구조체다.
 * Endereço(住所)는 도착할 곳, 갈래는 Endereço SO_VALOR, datagrama(電文)은 limite_VALOR 있는 comunicação 자료다. */
enum rede_constante {
    malha_Família = 2, fluxo_rede = 1, datagrama_soquete = 2,
    fluxo_protocolo_de_transporte = 6, datagrama_protocolo = 17,
    endereço_de_loopback = 0x7f000001u, 모든접속주소 = 0, 다시시도오류 = 11
};
typedef uint32_t soquete_email_duração_TIPO;
struct soquete_email { uint16_t email_Família; unsigned char email_dados[14]; };
struct endereço_na_Internet_VALOR { uint32_t email_VALOR; };
struct malha_soquete_email {
    uint16_t email_Família;
    uint16_t número_da_porta;
    struct endereço_na_Internet_VALOR endereço_na_Internet;
    unsigned char margem_VALOR[8];
};
typedef struct soquete_email soquete_email_TIPO;
typedef struct malha_soquete_email malha_soquete_email_TIPO;
/* SVC 경계에서 바이트로 복사한다. 서로 다른 구조체 포인터를 역참조하지 않는다. */
typedef char cheque_malha_soquete_email_dimensionar[(sizeof(struct malha_soquete_email)==16)?1:-1];
typedef char cheque_malha_soquete_email_Layout[(offsetof(struct malha_soquete_email,endereço_na_Internet)==4)?1:-1];
#ifdef __cplusplus
extern "C" {
#endif
int Criar_empresa(int email_Família, int comunicação_MODO, int Transferir_protocolo);
int BIND_email(int empresa, const struct soquete_email *Endereço, soquete_email_duração_TIPO duração_VALOR);
intptr_t enviar_datagrama_dados(int empresa, const void *dados, size_t item_CONT_NÚM, int seleção_VALOR, const struct soquete_email *Endereço, soquete_email_duração_TIPO duração_VALOR);
intptr_t receber_datagrama_dados(int empresa, void *dados, size_t item_CONT_NÚM, int seleção_VALOR, struct soquete_email *Endereço, soquete_email_duração_TIPO *duração_VALOR);
int leitura_soquete_email(int empresa, struct soquete_email *Endereço, soquete_email_duração_TIPO *duração_VALOR);
int Conexão_rede(int empresa, const struct soquete_email *Endereço, soquete_email_duração_TIPO duração_VALOR);
int 통신연결기다리기(int empresa, int Esperando_CONT_NÚM);
int aceitar_conexão_de_rede(int empresa, struct soquete_email *Endereço, soquete_email_duração_TIPO *duração_VALOR);

int pk_connect(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
int pk_listen(int fd, int backlog);
int pk_accept(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_socket(int domain, int type, int protocol);
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length);
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length);
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length);
#ifdef __cplusplus
}
#endif
static inline uint16_t 망차례짧은수(uint16_t VALOR) { return (uint16_t)((VALOR >> 8) | (VALOR << 8)); }
static inline uint32_t rede_inteiro(uint32_t VALOR) { return ((VALOR & 255u) << 24) | ((VALOR & 0xff00u) << 8) | ((VALOR >> 8) & 0xff00u) | (VALOR >> 24); }
static inline uint16_t 장치차례짧은수(uint16_t VALOR) { return 망차례짧은수(VALOR); }
static inline uint32_t celular_ordem_inteiro(uint32_t VALOR) { return rede_inteiro(VALOR); }
static inline uint16_t pk_htons(uint16_t x) { return 망차례짧은수(x); }
static inline uint32_t pk_htonl(uint32_t x) { return rede_inteiro(x); }
#endif

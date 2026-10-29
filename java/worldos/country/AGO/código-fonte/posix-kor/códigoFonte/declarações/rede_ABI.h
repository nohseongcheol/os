#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Criar_empresa socket
#define BIND_email bind
#define enviar_datagrama_dados sendto
#define receber_datagrama_dados recvfrom
#define leitura_soquete_email getsockname
#define alterar_rede_Configurações setsockopt
#define analisar_ID_de_rede inet_pton
#define formato_ID_de_rede inet_ntop
#define 망차례짧은수 htons
#define rede_inteiro htonl
#define 장치차례짧은수 ntohs
#define celular_ordem_inteiro ntohl
#endif

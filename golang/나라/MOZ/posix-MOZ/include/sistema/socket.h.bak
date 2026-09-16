#ifndef _include_sistema_socket
#define _include_sistema_socket

#include <definições_básicas.h>
#include <sistema/tipos_de_dados.h>

typedef unsigned short tipo_da_família_de_endereços;

struct endereço_do_extremo_de_comunicação {
    tipo_da_família_de_endereços família_de_endereços_do_extremo;
    char dados_do_endereço[14];
};

#define família_de_endereços_não_especificada 0
#define código_da_família_de_endereços_entre_redes 2
#define família_de_protocolos_entre_redes código_da_família_de_endereços_entre_redes

#define extremo_de_fluxo_de_dados 1
#define extremo_de_datagramas 2

#define parar_receção 0
#define parar_envio 1
#define parar_ambos_os_sentidos 2

#ifdef __cplusplus
extern "C" {
#endif
int criar_extremo_de_comunicação(int domain, int type, int protocol);
int associar_endereço_local(int descritor_do_ficheiro, const struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço address_len);
int ligar_ao_extremo_remoto(int descritor_do_ficheiro, const struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço address_len);
int preparar_receção_de_ligações(int descritor_do_ficheiro, int backlog);
int aceitar_ligação(int descritor_do_ficheiro, struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *address_len);
int obter_endereço_do_extremo_local(int descritor_do_ficheiro, struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *address_len);
int obter_endereço_do_extremo_remoto(int descritor_do_ficheiro, struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *address_len);
ssize_t enviar(int descritor_do_ficheiro, const void *memória_intermédia_de_transferência_2, size_t comprimento, int flags);
ssize_t receber(int descritor_do_ficheiro, void *memória_intermédia_de_transferência_2, size_t comprimento, int flags);
ssize_t enviar_para_destino(int descritor_do_ficheiro, const void *message, size_t comprimento, int flags,
               const struct endereço_do_extremo_de_comunicação *dest_addr, tipo_do_comprimento_do_endereço dest_len);
ssize_t receber_com_endereço_de_origem(int descritor_do_ficheiro, void *memória_intermédia_de_transferência_2, size_t comprimento, int flags,
                 struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *address_len);
int fechar_sentido_de_comunicação(int descritor_do_ficheiro, int how);
int definir_opção_do_extremo(int descritor_do_ficheiro, int level, int option_name,
               const void *option_value, tipo_do_comprimento_do_endereço option_len);
#ifdef __cplusplus
}
#endif

#endif

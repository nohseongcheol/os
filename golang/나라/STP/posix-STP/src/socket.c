/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <conversão_de_endereços/ordem_de_octetos.h>
#include <sistema/syscall.h>
#include <sistema/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_criar_extremo_de_comunicação = 1, SC_associar_endereço_local = 2, SC_ligar_ao_extremo_remoto = 3, SC_preparar_receção_de_ligações = 4,
    SC_aceitar_ligação = 5, SC_obter_endereço_do_extremo_local = 6, SC_obter_endereço_do_extremo_remoto = 7,
    SC_enviar = 9, SC_receber = 10, SC_enviar_para_destino = 11, SC_receber_com_endereço_de_origem = 12,
    SC_fechar_sentido_de_comunicação = 13, SC_definir_opção_do_extremo = 14
};

static long socket_call(long call, unsigned long *argumentos)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)argumentos, 0, 0, 0, 0));
}

uint16_t converter_16_bits_para_ordem_da_rede(uint16_t valor) { return (uint16_t)((valor << 8) | (valor >> 8)); }
uint16_t converter_16_bits_para_ordem_da_máquina(uint16_t valor) { return converter_16_bits_para_ordem_da_rede(valor); }
uint32_t converter_32_bits_para_ordem_da_rede(uint32_t valor)
{
    return ((valor & 0x000000ffU) << 24) | ((valor & 0x0000ff00U) << 8) |
           ((valor & 0x00ff0000U) >> 8) | ((valor & 0xff000000U) >> 24);
}
uint32_t converter_32_bits_para_ordem_da_máquina(uint32_t valor) { return converter_32_bits_para_ordem_da_rede(valor); }

int criar_extremo_de_comunicação(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_criar_extremo_de_comunicação, a);
}

int associar_endereço_local(int descritor_do_ficheiro, const struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço comprimento)
{
    unsigned long a[3] = {(unsigned long)descritor_do_ficheiro, (unsigned long)address, comprimento};
    return (int)socket_call(SC_associar_endereço_local, a);
}

int ligar_ao_extremo_remoto(int descritor_do_ficheiro, const struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço comprimento)
{
    unsigned long a[3] = {(unsigned long)descritor_do_ficheiro, (unsigned long)address, comprimento};
    return (int)socket_call(SC_ligar_ao_extremo_remoto, a);
}

int preparar_receção_de_ligações(int descritor_do_ficheiro, int backlog)
{
    unsigned long a[2] = {(unsigned long)descritor_do_ficheiro, (unsigned long)backlog};
    return (int)socket_call(SC_preparar_receção_de_ligações, a);
}

int aceitar_ligação(int descritor_do_ficheiro, struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *comprimento)
{
    unsigned long a[3] = {(unsigned long)descritor_do_ficheiro, (unsigned long)address, (unsigned long)comprimento};
    return (int)socket_call(SC_aceitar_ligação, a);
}

int obter_endereço_do_extremo_local(int descritor_do_ficheiro, struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *comprimento)
{
    unsigned long a[3] = {(unsigned long)descritor_do_ficheiro, (unsigned long)address, (unsigned long)comprimento};
    return (int)socket_call(SC_obter_endereço_do_extremo_local, a);
}

int obter_endereço_do_extremo_remoto(int descritor_do_ficheiro, struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *comprimento)
{
    unsigned long a[3] = {(unsigned long)descritor_do_ficheiro, (unsigned long)address, (unsigned long)comprimento};
    return (int)socket_call(SC_obter_endereço_do_extremo_remoto, a);
}

ssize_t enviar(int descritor_do_ficheiro, const void *memória_intermédia_de_transferência_2, size_t comprimento, int flags)
{
    unsigned long a[4] = {(unsigned long)descritor_do_ficheiro, (unsigned long)memória_intermédia_de_transferência_2, comprimento, (unsigned long)flags};
    return (ssize_t)socket_call(SC_enviar, a);
}

ssize_t receber(int descritor_do_ficheiro, void *memória_intermédia_de_transferência_2, size_t comprimento, int flags)
{
    unsigned long a[4] = {(unsigned long)descritor_do_ficheiro, (unsigned long)memória_intermédia_de_transferência_2, comprimento, (unsigned long)flags};
    return (ssize_t)socket_call(SC_receber, a);
}

ssize_t enviar_para_destino(int descritor_do_ficheiro, const void *memória_intermédia_de_transferência_2, size_t comprimento, int flags,
               const struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço address_length)
{
    unsigned long a[6] = {(unsigned long)descritor_do_ficheiro, (unsigned long)memória_intermédia_de_transferência_2, comprimento,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_enviar_para_destino, a);
}

ssize_t receber_com_endereço_de_origem(int descritor_do_ficheiro, void *memória_intermédia_de_transferência_2, size_t comprimento, int flags,
                 struct endereço_do_extremo_de_comunicação *address, tipo_do_comprimento_do_endereço *address_length)
{
    unsigned long a[6] = {(unsigned long)descritor_do_ficheiro, (unsigned long)memória_intermédia_de_transferência_2, comprimento,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_receber_com_endereço_de_origem, a);
}

int fechar_sentido_de_comunicação(int descritor_do_ficheiro, int how)
{
    unsigned long a[2] = {(unsigned long)descritor_do_ficheiro, (unsigned long)how};
    return (int)socket_call(SC_fechar_sentido_de_comunicação, a);
}

int definir_opção_do_extremo(int descritor_do_ficheiro, int level, int option_name,
               const void *option_value, tipo_do_comprimento_do_endereço option_len)
{
    unsigned long a[5] = {(unsigned long)descritor_do_ficheiro, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_definir_opção_do_extremo, a);
}

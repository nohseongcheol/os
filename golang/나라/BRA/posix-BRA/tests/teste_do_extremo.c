/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <conversão_de_endereços/ordem_de_octetos.h>
#include <errno.h>
#include <sistema/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)escrever(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *identidade_do_sistema, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(identidade_do_sistema);
    say("\n");
}

int main(void)
{
    struct endereço_do_extremo_entre_redes server_address = {0};
    struct endereço_do_extremo_entre_redes source = {0};
    tipo_do_comprimento_do_endereço source_length = sizeof(source);
    char memória_intermédia_de_transferência_2[8] = {0};
    int server = criar_extremo_de_comunicação(código_da_família_de_endereços_entre_redes, extremo_de_datagramas, protocolo_de_datagramas_do_utilizador);
    int client = criar_extremo_de_comunicação(código_da_família_de_endereços_entre_redes, extremo_de_datagramas, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.família_de_endereços_entre_redes = código_da_família_de_endereços_entre_redes;
    server_address.número_de_porta_de_comunicação = converter_16_bits_para_ordem_da_rede(32345);
    server_address.conteúdo_do_endereço_entre_redes.valor_do_endereço = converter_32_bits_para_ordem_da_rede(endereço_de_retorno_local);
    report("bind", associar_endereço_local(server, (const struct endereço_do_extremo_de_comunicação *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", ligar_ao_extremo_remoto(client, (const struct endereço_do_extremo_de_comunicação *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", enviar(client, "ping", 4, 0) == 4);
    report("recvfrom", receber_com_endereço_de_origem(server, memória_intermédia_de_transferência_2, sizeof(memória_intermédia_de_transferência_2), 0,
                                (struct endereço_do_extremo_de_comunicação *)&source, &source_length) == 4 &&
                       memória_intermédia_de_transferência_2[0] == 'p' && memória_intermédia_de_transferência_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", receber(server, memória_intermédia_de_transferência_2, sizeof(memória_intermédia_de_transferência_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", obter_endereço_do_extremo_local(server, (struct endereço_do_extremo_de_comunicação *)&source,
                                      &source_length) == 0 && source.número_de_porta_de_comunicação == converter_16_bits_para_ordem_da_rede(32345));
    errno = 0;
    report("udp-listen-not-supported", preparar_receção_de_ligações(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", fechar(client) == 0);
    report("close-server", fechar(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}

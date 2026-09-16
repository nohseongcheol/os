/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <conversión_de_direcciones/orden_de_octetos.h>
#include <errno.h>
#include <sistema/socket.h>
#include <unistd.h>

static unsigned int length_of(const char *s)
{
    unsigned int n = 0;
    while (s[n] != 0) n++;
    return n;
}

static void say(const char *s) { (void)escribir(STDOUT_FILENO, s, length_of(s)); }

static void report(const char *identidad_del_sistema, int pass)
{
    say(pass ? "NTEST:PASS:" : "NTEST:FAIL:");
    say(identidad_del_sistema);
    say("\n");
}

int main(void)
{
    struct dirección_de_extremo_entre_redes server_address = {0};
    struct dirección_de_extremo_entre_redes source = {0};
    tipo_de_longitud_de_dirección source_length = sizeof(source);
    char memoria_intermedia_de_transferencia_2[8] = {0};
    int server = crear_extremo_de_comunicación(código_de_familia_de_direcciones_entre_redes, extremo_de_datagramas, protocolo_de_datagramas_de_usuario);
    int client = crear_extremo_de_comunicación(código_de_familia_de_direcciones_entre_redes, extremo_de_datagramas, 0);

    report("socket-server", server >= 3);
    report("socket-client", client >= 3 && client != server);
    server_address.familia_de_direcciones_entre_redes = código_de_familia_de_direcciones_entre_redes;
    server_address.número_de_puerto_de_comunicación = convertir_16_bits_a_orden_de_red(32345);
    server_address.contenido_de_dirección_entre_redes.valor_de_dirección = convertir_32_bits_a_orden_de_red(dirección_de_retorno_local);
    report("bind", asociar_dirección_local(server, (const struct dirección_de_extremo_de_comunicación *)&server_address,
                        sizeof(server_address)) == 0);
    report("connect", conectar_con_extremo_remoto(client, (const struct dirección_de_extremo_de_comunicación *)&server_address,
                              sizeof(server_address)) == 0);
    report("send", enviar(client, "ping", 4, 0) == 4);
    report("recvfrom", recibir_con_dirección_de_origen(server, memoria_intermedia_de_transferencia_2, sizeof(memoria_intermedia_de_transferencia_2), 0,
                                (struct dirección_de_extremo_de_comunicación *)&source, &source_length) == 4 &&
                       memoria_intermedia_de_transferencia_2[0] == 'p' && memoria_intermedia_de_transferencia_2[3] == 'g' && source_length == 16);
    errno = 0;
    report("empty-eagain", recibir(server, memoria_intermedia_de_transferencia_2, sizeof(memoria_intermedia_de_transferencia_2), 0) == -1 && errno == EAGAIN);
    report("getsockname", obtener_dirección_local(server, (struct dirección_de_extremo_de_comunicación *)&source,
                                      &source_length) == 0 && source.número_de_puerto_de_comunicación == convertir_16_bits_a_orden_de_red(32345));
    errno = 0;
    report("udp-listen-not-supported", preparar_recepción_de_conexiones(server, 1) == -1 && errno == EOPNOTSUPP);
    report("close-client", cerrar(client) == 0);
    report("close-server", cerrar(server) == 0);
    say("NTEST:DONE\n");
    return 0;
}

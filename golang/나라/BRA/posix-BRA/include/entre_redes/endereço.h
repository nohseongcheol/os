/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_entre_redes_endereço
#define _include_entre_redes_endereço

#include <tipos_inteiros.h>
#include <sistema/socket.h>

typedef uint32_t tipo_do_valor_de_endereço_entre_redes;
typedef uint16_t tipo_do_número_de_porta_de_comunicação;

struct endereço_entre_redes {
    tipo_do_valor_de_endereço_entre_redes valor_do_endereço;
};

struct endereço_do_extremo_entre_redes {
    tipo_da_família_de_endereços família_de_endereços_entre_redes;
    tipo_do_número_de_porta_de_comunicação número_de_porta_de_comunicação;
    struct endereço_entre_redes conteúdo_do_endereço_entre_redes;
    unsigned char preenchimento_do_endereço[8];
};

#define protocolo_básico_entre_redes 0
#define protocolo_de_datagramas_do_utilizador 17
#define qualquer_endereço_local ((tipo_do_valor_de_endereço_entre_redes)0x00000000U)
#define endereço_de_retorno_local ((tipo_do_valor_de_endereço_entre_redes)0x7f000001U)

#endif

#ifndef _include_entre_redes_dirección
#define _include_entre_redes_dirección

#include <tipos_enteros.h>
#include <sistema/socket.h>

typedef uint32_t tipo_de_valor_de_dirección_entre_redes;
typedef uint16_t tipo_de_número_de_puerto_de_comunicación;

struct dirección_entre_redes {
    tipo_de_valor_de_dirección_entre_redes valor_de_dirección;
};

struct dirección_de_extremo_entre_redes {
    tipo_de_familia_de_direcciones familia_de_direcciones_entre_redes;
    tipo_de_número_de_puerto_de_comunicación número_de_puerto_de_comunicación;
    struct dirección_entre_redes contenido_de_dirección_entre_redes;
    unsigned char relleno_de_dirección[8];
};

#define protocolo_básico_entre_redes 0
#define protocolo_de_datagramas_de_usuario 17
#define cualquier_dirección_local ((tipo_de_valor_de_dirección_entre_redes)0x00000000U)
#define dirección_de_retorno_local ((tipo_de_valor_de_dirección_entre_redes)0x7f000001U)

#endif

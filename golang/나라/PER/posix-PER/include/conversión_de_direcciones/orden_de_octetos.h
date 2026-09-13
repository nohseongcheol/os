#ifndef _include_conversión_de_direcciones_orden_de_octetos
#define _include_conversión_de_direcciones_orden_de_octetos

#include <entre_redes/dirección.h>

#ifdef __cplusplus
extern "C" {
#endif
uint16_t convertir_16_bits_a_orden_de_red(uint16_t valor_de_16_bits_en_orden_de_máquina);
uint16_t convertir_16_bits_a_orden_de_máquina(uint16_t valor_de_16_bits_en_orden_de_red);
uint32_t convertir_32_bits_a_orden_de_red(uint32_t valor_de_32_bits_en_orden_de_máquina);
uint32_t convertir_32_bits_a_orden_de_máquina(uint32_t valor_de_32_bits_en_orden_de_red);
#ifdef __cplusplus
}
#endif

#endif

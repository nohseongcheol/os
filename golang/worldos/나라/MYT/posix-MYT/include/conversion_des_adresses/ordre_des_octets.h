#ifndef _include_conversion_des_adresses_ordre_des_octets
#define _include_conversion_des_adresses_ordre_des_octets

#include <interréseau/adresse.h>

#ifdef __cplusplus
extern "C" {
#endif
uint16_t convertir_16_bits_vers_ordre_réseau(uint16_t valeur_de_16_bits_en_ordre_machine);
uint16_t convertir_16_bits_vers_ordre_machine(uint16_t valeur_de_16_bits_en_ordre_réseau);
uint32_t convertir_32_bits_vers_ordre_réseau(uint32_t valeur_de_32_bits_en_ordre_machine);
uint32_t convertir_32_bits_vers_ordre_machine(uint32_t valeur_de_32_bits_en_ordre_réseau);
#ifdef __cplusplus
}
#endif

#endif

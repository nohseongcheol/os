#ifndef entêteLotNatif
#define entêteLotNatif
#include <stddef.h>
int ouvrirJAR(const char *nomEntréeÉlémentFichier);
int lireJAR(const char *nom, unsigned char *donnéesRésultat, unsigned capacitéTampon);
const char *principalJAR(void);
#endif

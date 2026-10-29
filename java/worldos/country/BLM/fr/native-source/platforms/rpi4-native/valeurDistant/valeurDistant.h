#ifndef entêteConnexionDistantNatif
#define entêteConnexionDistantNatif
#include "../nommage/nomsLierMachine.h"
#include <stdint.h>
void préparerDistant(void);
void inspecterDistant(void);
void sortieDistant(unsigned char);
int entréeDistant(void);
int entréeDistantAlimenter(const unsigned char *,unsigned);
uintptr_t contrôleDistantCarteMatérielle(uintptr_t,uintptr_t);
uintptr_t commandeDistantFinCarteMatérielle(uintptr_t);
uintptr_t attendreDistantCarteMatérielle(uintptr_t);
void inspecterPrésenterDistant(void);
int présenterDistantContrôle(unsigned);
#endif

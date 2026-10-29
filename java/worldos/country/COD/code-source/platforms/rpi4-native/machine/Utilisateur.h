#ifndef entêteUtilisateurNatif
#define entêteUtilisateurNatif
#include <stdint.h>
#include <stddef.h>
#define baseUtilisateur 0x02000000ul
#define finImageUtilisateur 0x02c00000ul
#define finTasUtilisateur 0x02ed0000ul
#define adressePileUtilisateur 0x02f00000ul
#define finUtilisateur 0x03000000ul
#define nombreÉlémentsPageUtilisateur ((finUtilisateur - baseUtilisateur) / 4096ul)
#define erreurCodeExécutableUtilisateur (-8)
#define erreurDonnéesUtilisateur (-1001)
#define erreurExécutionUtilisateur (-1002)
#define instructionMachineInvalideUtilisateur (-1003)
#define délaiExpirationUtilisateur (-1004)
#define interrompuUtilisateur (-1005)
typedef struct { uint64_t registreDonnées[31], positionCommande, codeÉtatValeur, adressePile; } cadreUtilisateur;
void opérationInitialisationSystèmeUtilisateur(void);
int exceptionUtilisateur(cadreUtilisateur *, unsigned);
int eLFValiderUtilisateur(const unsigned char *, size_t);
uintptr_t lancerUtilisateurCarteMatérielle(uintptr_t);
uintptr_t validerUtilisateurCarteMatérielle(void);
uintptr_t contrôleUtilisateurCarteMatérielle(uintptr_t);
uint32_t lireÉtatValeurUtilisateur(unsigned, unsigned);
#endif

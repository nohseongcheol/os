#ifndef EntêteExempleNatif
#define EntêteExempleNatif
#include <ABIFichier.h>
#include <ABIÉcran.h>
static int longueurTexte(const char *texte) { int longueur=0;while(texte[longueur])longueur++;return longueur; }
static int Sortie(const char *texte) { int longueur=longueurTexte(texte);return écrireDonnéesFichier(1,texte,longueur)==longueur?0:1; }
#endif

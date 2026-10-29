#ifndef entêteRéseauNatif
#define entêteRéseauNatif
#include <stdint.h>
#include <stddef.h>
void préparerRéseau(void);
void inspecterRéseau(void);
int créerExtrémitéPriseRéseau(int catégorieType);
int associerRéseauCourt(int poignéeFichier, uint32_t adresse, unsigned numéroPort);
int écouterRéseauCourt(int poignéeFichier);
void adressePriseRéseauRéutiliser(int poignéeFichier);
int connecterRéseauCourt(int poignéeFichier, uint32_t adresse, unsigned numéroPort);
int accepterRéseauCourt(int poignéeFichier);
int lireRéseauCourt(int poignéeFichier, void *Données, unsigned nombreÉlémentsÉlémentListe);
int écrireRéseauCourt(int poignéeFichier, const void *Données, unsigned nombreÉlémentsÉlémentListe);
int envoyerDatagramme(int poignéeFichier, const void *Données, unsigned nombreÉlémentsÉlémentListe, uint32_t adresse, unsigned numéroPort);
int recevoirDatagramme(int poignéeFichier, void *Données, unsigned nombreÉlémentsÉlémentListe);
unsigned numéroPortRéseau(int poignéeFichier);
unsigned numéroPortPairRéseau(int poignéeFichier);
uint32_t adressePairRéseauRéseauCourt(int poignéeFichier);
void fermerRéseau(int poignéeFichier);
int contrôleTransfertFichier(int action);
void inspecterTransfertFichier(void);
uint32_t lireÉtatRéseau(unsigned valeurEntréeÉlément, unsigned numéro);
int configurerRéseau(unsigned action, uint32_t adresse, uint32_t valeurMasque, uint32_t valeurPasserelle);
int démarrerTestRéponseRetour(uint32_t adresse, unsigned valeurOrdre);
int lireTestRéponseRetour(unsigned valeurEntréeÉlément);
#endif

#include "../nommage/nomsLierMachine.h"
#include "invoquer.h"
extern int main(int,char **);
static char tableauArgument[8][256];
int démarrerUtilisateur(int inutilisé){
    (void)inutilisé;char *listeArgument[9];int nombreÉlémentsArguments=invoquerUtilisateur(15,UINTPTR_MAX,0,0,0,0,0);
    if(nombreÉlémentsArguments<0||nombreÉlémentsArguments>8)return 126;
    for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsArguments;indiceOrdinal++){if(invoquerUtilisateur(15,indiceOrdinal,(uintptr_t)tableauArgument[indiceOrdinal],256,0,0,0)<0)return 126;listeArgument[indiceOrdinal]=tableauArgument[indiceOrdinal];}listeArgument[nombreÉlémentsArguments]=0;
    return main(nombreÉlémentsArguments,listeArgument);
}
void *memset(void*positionDonnées,int codeCaractère,size_t nombreÉlémentsÉlémentListe){unsigned char*donnéesDestination=positionDonnées;while(nombreÉlémentsÉlémentListe--)*donnéesDestination++=codeCaractère;return positionDonnées;}
void *memcpy(void*donnéesDestination,const void*donnéesChaîne,size_t nombreÉlémentsÉlémentListe){unsigned char*valeurPremier=donnéesDestination;const unsigned char*valeurDeuxième=donnéesChaîne;while(nombreÉlémentsÉlémentListe--)*valeurPremier++=*valeurDeuxième++;return donnéesDestination;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned coordonnéeCoordonnéeHorizontale,unsigned coordonnéeCoordonnéeVerticale,unsigned valeurLargeur,unsigned valeurHauteur,unsigned couleurPixel){return rectangleÉcran(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,valeurLargeur,valeurHauteur,couleurPixel);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return invoquerUtilisateur(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return attendreToucheÉcranPour();}
int dessinerRectangle(unsigned positionHorizontal,unsigned positionVertical,unsigned valeurLargeur,unsigned valeurHauteur,unsigned couleurPixel){return pk_rectangle(positionHorizontal,positionVertical,valeurLargeur,valeurHauteur,couleurPixel);}
unsigned millisecondes(void){return pk_ticks_ms();}
int attendreDessinPour(void){return pk_graphics_wait();}
int largeurÉcran(void){return lireLargeurÉcran();}
int hauteurÉcran(void){return lireHauteurÉcran();}

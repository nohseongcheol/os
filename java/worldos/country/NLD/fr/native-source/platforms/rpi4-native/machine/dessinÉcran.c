/* donnéesEffectif Écran 메모리와 기존 C invoquer 규약만 연결한다. 합성 구현은 source/ComposeurTamponImage.java. */
#include "../nommage/nomsLierMachine.h"
#include "informationÉcran.h"
static volatile uint32_t *listePixels;
static unsigned nombreÉlémentsMotRangéeÉcran, largeurÉcran, hauteurÉcran;
extern void préparerDessinJava(int,int),finDessinJava(void),rectangleDessinJava(int,int,int,int,int),pointeurDessinJava(int,int,int);
extern int largeurDessinJava(void),hauteurDessinJava(void),basNombreÉlémentsDessinJava(void),hautNombreÉlémentsDessinJava(void);
extern int rognerDessinJava(int,int,int,int),valeurRognerDessinJava(int),débutPositionDessinJava(int,int,int,int),pixelDessinJava(int,int,int);
uintptr_t lireTamponImageCarteMatérielle(uintptr_t positionHorizontal,uintptr_t positionVertical){
    return listePixels&&positionHorizontal<largeurÉcran&&positionVertical<hauteurÉcran?listePixels[positionVertical*nombreÉlémentsMotRangéeÉcran+positionHorizontal]:0;
}
void écrireTamponImageCarteMatérielle(uintptr_t positionHorizontal,uintptr_t positionVertical,uintptr_t valeurCouleur){
    if(listePixels&&positionHorizontal<largeurÉcran&&positionVertical<hauteurÉcran)listePixels[positionVertical*nombreÉlémentsMotRangéeÉcran+positionHorizontal]=(uint32_t)valeurCouleur;
}
void dessinPréparerCarteMatérielle(volatile uint32_t *Données,unsigned étendueLargeur,unsigned longueur,unsigned valeurEspacementLigne){
    listePixels=Données;largeurÉcran=étendueLargeur;hauteurÉcran=longueur;nombreÉlémentsMotRangéeÉcran=valeurEspacementLigne/4;préparerDessinJava((int)étendueLargeur,(int)longueur);
}
uintptr_t largeurÉcranCarteMatérielle(void){return (unsigned)largeurDessinJava();}
uintptr_t hauteurÉcranCarteMatérielle(void){return (unsigned)hauteurDessinJava();}
uint64_t nombreÉlémentsDessinCarteMatérielle(void){return ((uint64_t)(uint32_t)hautNombreÉlémentsDessinJava()<<32)|(uint32_t)basNombreÉlémentsDessinJava();}
uint32_t écranLireCarteMatérielle(unsigned positionHorizontal,unsigned positionVertical){return (uint32_t)lireTamponImageCarteMatérielle(positionHorizontal,positionVertical);}
int bornesDessinCarteMatérielle(int *positionHorizontal,int *positionVertical,int *étendueLargeur,int *longueur){
    if(!rognerDessinJava(*positionHorizontal,*positionVertical,*étendueLargeur,*longueur))return 0;
    *positionHorizontal=valeurRognerDessinJava(0);*positionVertical=valeurRognerDessinJava(1);*étendueLargeur=valeurRognerDessinJava(2);*longueur=valeurRognerDessinJava(3);return 1;
}
int dessinDémarrerCarteMatérielle(int positionHorizontal,int positionVertical,int étendueLargeur,int longueur){return débutPositionDessinJava(positionHorizontal,positionVertical,étendueLargeur,longueur);}
void dessinTerminerCarteMatérielle(void){finDessinJava();}
uintptr_t pixelCarteMatérielle(uintptr_t positionHorizontal,uintptr_t positionVertical,uintptr_t valeurCouleur){return (unsigned)pixelDessinJava((int)positionHorizontal,(int)positionVertical,(int)valeurCouleur);}
void remplirRectangleCarteMatérielle(int positionHorizontal,int positionVertical,int étendueLargeur,int longueur,uint32_t valeurCouleur){rectangleDessinJava(positionHorizontal,positionVertical,étendueLargeur,longueur,(int)valeurCouleur);}
void pointeurCarteMatérielle(int positionHorizontal,int positionVertical,unsigned valeurForme){pointeurDessinJava(positionHorizontal,positionVertical,(int)valeurForme);}

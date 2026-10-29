#include "../nommage/nomsLierMachine.h"
#include "../machine/informationÉcran.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void arrêtFatalNoyau(const char *description){fputs(description,stderr);abort();}
extern uintptr_t terminalCarteMatérielle(uintptr_t),pixelCarteMatérielle(uintptr_t,uintptr_t,uintptr_t);
extern void pointeurTerminal(unsigned,int,int),octetTerminal(unsigned);
extern int invoquerÉcran(int,unsigned,int,int,int,int,int);
static uint32_t Écran[1080][1936],imageComparaison[1080][1936];
uintptr_t tamponImageCarteMatérielle(void){return 1;}
static void comparerEntier(void){
    pointeurCarteMatérielle(0,0,0);memcpy(imageComparaison,Écran,sizeof(Écran));
    uint64_t élémentListePrécédentÉlément=nombreÉlémentsDessinCarteMatérielle();terminalCarteMatérielle(3);
    assert(memcmp(imageComparaison,Écran,sizeof(Écran))==0);
    assert(nombreÉlémentsDessinCarteMatérielle()==élémentListePrécédentÉlément); /* 같은 화면을 valeurRéessayer 그려도 afficherValeur 메모리에 쓰지 않는다. */
}
static void écrireTexte(const char *texte){while(*texte)octetTerminal((unsigned char)*texte++);}
int main(void){
    dessinPréparerCarteMatérielle(&Écran[0][0],1920,1080,sizeof(Écran[0]));
    terminalCarteMatérielle(300);écrireTexte("élémentListePremier 창의 한글 Données\n");
    for(int numéro=1;numéro<4;numéro++){terminalCarteMatérielle(1);terminalCarteMatérielle(100+numéro);écrireTexte("겹친 창의 한글 Données\n\033[41m색칠한 sauterEspacesBlancs     \033[0m\n");}
    comparerEntier();
    int positionHorizontal=60,positionVertical=102,étendueLargeur=568,valeurHauteur=360;
    uint64_t journalDéplacer=0;double tempsMouvement=0;
    for(int valeurSéquence=0;valeurSéquence<80;valeurSéquence++){
        pointeurTerminal(1,positionHorizontal+100,positionVertical+15);
        int positionHorizontalNouveau=80+(valeurSéquence*37)%850,positionVerticalNouveau=50+(valeurSéquence*13)%450;
        pixelCarteMatérielle(1900,1050,0x123456); /* actualiser valeurRégion 밖의 Utilisateur Dessin */
        uint64_t élémentListePrécédentÉlément=nombreÉlémentsDessinCarteMatérielle();clock_t lancer=clock();
        pointeurTerminal(1,positionHorizontalNouveau+100,positionVerticalNouveau+15);
        tempsMouvement+=(double)(clock()-lancer)/CLOCKS_PER_SEC;
        journalDéplacer+=nombreÉlémentsDessinCarteMatérielle()-élémentListePrécédentÉlément;
        assert(nombreÉlémentsDessinCarteMatérielle()-élémentListePrécédentÉlément<=2u*étendueLargeur*valeurHauteur);
        assert(Écran[1050][1900]==0x123456);
        pixelCarteMatérielle(1900,1050,0x302018);
        pointeurTerminal(0,positionHorizontalNouveau+100,positionVerticalNouveau+15);positionHorizontal=positionHorizontalNouveau;positionVertical=positionVerticalNouveau;
        comparerEntier();
    }
    for(int valeurSéquence=0;valeurSéquence<40;valeurSéquence++){
        int largeurNouveau=360+(valeurSéquence*29)%700,hauteurNouveau=216+(valeurSéquence*17)%350;
        if(largeurNouveau>1920-positionHorizontal)largeurNouveau=1920-positionHorizontal;if(hauteurNouveau>1080-positionVertical)hauteurNouveau=1080-positionVertical;
        pointeurTerminal(1,positionHorizontal+étendueLargeur-4,positionVertical+valeurHauteur-4);
        pointeurTerminal(1,positionHorizontal+largeurNouveau-4,positionVertical+hauteurNouveau-4);
        uint64_t élémentListePrécédentÉlément=nombreÉlémentsDessinCarteMatérielle();
        pointeurTerminal(1,positionHorizontal+largeurNouveau-4,positionVertical+hauteurNouveau-4);
        assert(nombreÉlémentsDessinCarteMatérielle()==élémentListePrécédentÉlément); /* 같은 좌표의 중복 évènement */
        pointeurTerminal(0,positionHorizontal+largeurNouveau-4,positionVertical+hauteurNouveau-4);étendueLargeur=largeurNouveau;valeurHauteur=hauteurNouveau;
        comparerEntier();
    }
    /* valeurRogné 범위와 donnéesEffectif ligne 간격을 지킨다. */
    for(int ligne=0;ligne<1080;ligne++)for(int entréeÉlémentEmplacement=1920;entréeÉlémentEmplacement<1936;entréeÉlémentEmplacement++)assert(Écran[ligne][entréeÉlémentEmplacement]==0);
    assert(!dessinDémarrerCarteMatérielle(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",tempsMouvement*1000/80,(unsigned long long)(journalDéplacer/80));
    return 0;
}

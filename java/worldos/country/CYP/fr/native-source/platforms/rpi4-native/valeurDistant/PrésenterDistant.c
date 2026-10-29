/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 connecter, 제한된 valeurEntrée longueur, 비동기 envoyerValeur, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 Écran Données 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "valeurDistant.h"
#include "priseEnChargeCryptographie.h"
#include "profil.h"
#include "../PileRéseau/PileRéseau.h"
#include "../machine/informationÉcran.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(motPasseÉcran)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t millisecondesÉcouléesCarteMatérielle(void);
extern uintptr_t terminalCarteMatérielle(uintptr_t);
void traitToucheDistant(unsigned,int);
void initialiserTraitToucheDistant(void);
void toucheDistantConfirmer(void);
static int extrémitéÉcouteEnCours=-1,valeurPairRéseau=-1,valeurÉtapePhase,futurFermer;
static uintptr_t tempsConnexion,encoreRecevoirActivé;
static unsigned char valeurEntrée[8192],Sortie[4096],valeurDéfi[16];
static unsigned nombreÉlémentsEntrée,nombreÉlémentsSortie,nombreÉlémentsEnvoyé;
static unsigned valeurLargeur,valeurHauteur,taillePixel=4,valeurOrdreOctetsGrand,maximalRouge=255,maximalVert=255,maximalBleu=255,décalerRouge=16,décalerVert=8,décalerBleu;
static uint32_t résuméPrécédentÉlément[60*68];
static unsigned short tuileChangé[60*68];
static unsigned nombreÉlémentsTuile,positionTuile,coordonnéeHorizontaleDemandé,coordonnéeVerticaleDemandé,étendueDemandé,hauteurDemandé;
static unsigned lire16Bits(const unsigned char *positionDonnées){return(unsigned)positionDonnées[0]*256+positionDonnées[1];}
static uint32_t lire32Bits(const unsigned char *positionDonnées){return(uint32_t)positionDonnées[0]<<24|(uint32_t)positionDonnées[1]<<16|(uint32_t)positionDonnées[2]<<8|positionDonnées[3];}
static void écrire16Bits(unsigned char *positionDonnées,unsigned valeur){positionDonnées[0]=valeur>>8;positionDonnées[1]=valeur;}
static void écrire32Bits(unsigned char *positionDonnées,uint32_t valeur){positionDonnées[0]=valeur>>24;positionDonnées[1]=valeur>>16;positionDonnées[2]=valeur>>8;positionDonnées[3]=valeur;}
static void fermer(void){if(valeurPairRéseau>=0)fermerRéseau(valeurPairRéseau);valeurPairRéseau=-1;valeurÉtapePhase=0;nombreÉlémentsEntrée=nombreÉlémentsSortie=nombreÉlémentsEnvoyé=0;nombreÉlémentsTuile=positionTuile=0;futurFermer=0;initialiserTraitToucheDistant();encoreRecevoirActivé=millisecondesÉcouléesCarteMatérielle()+500;}
static void émettreValeur(const void *Données,unsigned nombre){memcpy(Sortie,Données,nombre);nombreÉlémentsSortie=nombre;nombreÉlémentsEnvoyé=0;}
static void consommerValeur(unsigned nombre){nombreÉlémentsEntrée-=nombre;memmove(valeurEntrée,valeurEntrée+nombre,nombreÉlémentsEntrée);}
int présenterDistantContrôle(unsigned action){
    if(action==0){fermer();if(extrémitéÉcouteEnCours>=0)fermerRéseau(extrémitéÉcouteEnCours);extrémitéÉcouteEnCours=-1;return 0;}
    if(action!=1)return extrémitéÉcouteEnCours>=0;
    if(extrémitéÉcouteEnCours>=0)return 0;
    int valeurPort=créerExtrémitéPriseRéseau(1);if(valeurPort<0)return valeurPort;adressePriseRéseauRéutiliser(valeurPort);
    int résultat=associerRéseauCourt(valeurPort,0,5900);if(!résultat)résultat=écouterRéseauCourt(valeurPort);
    if(résultat<0){fermerRéseau(valeurPort);return résultat;}extrémitéÉcouteEnCours=valeurPort;return 0;
}
static uint32_t résuméTuile(unsigned positionHorizontal,unsigned positionVertical){
    uint32_t valeur=2166136261u;
    for(unsigned coordonnéeCoordonnéeVerticale=positionVertical;coordonnéeCoordonnéeVerticale<positionVertical+16&&coordonnéeCoordonnéeVerticale<valeurHauteur;coordonnéeCoordonnéeVerticale++)for(unsigned coordonnéeCoordonnéeHorizontale=positionHorizontal;coordonnéeCoordonnéeHorizontale<positionHorizontal+32&&coordonnéeCoordonnéeHorizontale<valeurLargeur;coordonnéeCoordonnéeHorizontale++)valeur=(valeur^écranLireCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale))*16777619u;
    return valeur;
}
static void requêteÉcran(const unsigned char *positionDonnées){
    coordonnéeHorizontaleDemandé=lire16Bits(positionDonnées+2);coordonnéeVerticaleDemandé=lire16Bits(positionDonnées+4);étendueDemandé=lire16Bits(positionDonnées+6);hauteurDemandé=lire16Bits(positionDonnées+8);
    if(coordonnéeHorizontaleDemandé>=valeurLargeur||coordonnéeVerticaleDemandé>=valeurHauteur)étendueDemandé=hauteurDemandé=0;
    if(étendueDemandé>valeurLargeur-coordonnéeHorizontaleDemandé&&coordonnéeHorizontaleDemandé<valeurLargeur)étendueDemandé=valeurLargeur-coordonnéeHorizontaleDemandé;
    if(hauteurDemandé>valeurHauteur-coordonnéeVerticaleDemandé&&coordonnéeVerticaleDemandé<valeurHauteur)hauteurDemandé=valeurHauteur-coordonnéeVerticaleDemandé;
    nombreÉlémentsTuile=positionTuile=0;
    if(étendueDemandé&&hauteurDemandé)for(unsigned coordonnéeCoordonnéeVerticale=coordonnéeVerticaleDemandé/16;coordonnéeCoordonnéeVerticale<=(coordonnéeVerticaleDemandé+hauteurDemandé-1)/16;coordonnéeCoordonnéeVerticale++)for(unsigned coordonnéeCoordonnéeHorizontale=coordonnéeHorizontaleDemandé/32;coordonnéeCoordonnéeHorizontale<=(coordonnéeHorizontaleDemandé+étendueDemandé-1)/32;coordonnéeCoordonnéeHorizontale++){
        unsigned indicePosition=coordonnéeCoordonnéeVerticale*60+coordonnéeCoordonnéeHorizontale;uint32_t valeurRésumé=résuméTuile(coordonnéeCoordonnéeHorizontale*32,coordonnéeCoordonnéeVerticale*16);
        if(!positionDonnées[1]||résuméPrécédentÉlément[indicePosition]!=valeurRésumé)tuileChangé[nombreÉlémentsTuile++]=indicePosition;
    }
    Sortie[0]=Sortie[1]=0;écrire16Bits(Sortie+2,nombreÉlémentsTuile);nombreÉlémentsSortie=4;nombreÉlémentsEnvoyé=0;
}
static void envoyerTuile(void){
    unsigned indicePosition=tuileChangé[positionTuile++],positionHorizontal=(indicePosition%60)*32,positionVertical=(indicePosition/60)*16;
    unsigned coordonnéeHorizontaleFin=positionHorizontal+32,coordonnéeVerticaleFin=positionVertical+16;if(coordonnéeHorizontaleFin>valeurLargeur)coordonnéeHorizontaleFin=valeurLargeur;if(coordonnéeVerticaleFin>valeurHauteur)coordonnéeVerticaleFin=valeurHauteur;
    /* valeurSousPartie 타일 requête 뒤에도 valeurResteDivision 화소를 보낸 것으로 처리하지 않는다. */
    int valeursTous=positionHorizontal>=coordonnéeHorizontaleDemandé&&positionVertical>=coordonnéeVerticaleDemandé&&coordonnéeHorizontaleFin<=coordonnéeHorizontaleDemandé+étendueDemandé&&coordonnéeVerticaleFin<=coordonnéeVerticaleDemandé+hauteurDemandé;
    if(valeursTous)résuméPrécédentÉlément[indicePosition]=résuméTuile(positionHorizontal,positionVertical);
    if(positionHorizontal<coordonnéeHorizontaleDemandé)positionHorizontal=coordonnéeHorizontaleDemandé;if(positionVertical<coordonnéeVerticaleDemandé)positionVertical=coordonnéeVerticaleDemandé;
    if(coordonnéeHorizontaleFin>coordonnéeHorizontaleDemandé+étendueDemandé)coordonnéeHorizontaleFin=coordonnéeHorizontaleDemandé+étendueDemandé;if(coordonnéeVerticaleFin>coordonnéeVerticaleDemandé+hauteurDemandé)coordonnéeVerticaleFin=coordonnéeVerticaleDemandé+hauteurDemandé;
    écrire16Bits(Sortie,positionHorizontal);écrire16Bits(Sortie+2,positionVertical);écrire16Bits(Sortie+4,coordonnéeHorizontaleFin-positionHorizontal);écrire16Bits(Sortie+6,coordonnéeVerticaleFin-positionVertical);écrire32Bits(Sortie+8,0);
    nombreÉlémentsSortie=12;nombreÉlémentsEnvoyé=0;
    for(unsigned coordonnéeCoordonnéeVerticale=positionVertical;coordonnéeCoordonnéeVerticale<coordonnéeVerticaleFin;coordonnéeCoordonnéeVerticale++)for(unsigned coordonnéeCoordonnéeHorizontale=positionHorizontal;coordonnéeCoordonnéeHorizontale<coordonnéeHorizontaleFin;coordonnéeCoordonnéeHorizontale++){
        uint32_t valeurCouleur=écranLireCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale),valeur=(((valeurCouleur>>16)&255)*maximalRouge/255)<<décalerRouge|
            (((valeurCouleur>>8)&255)*maximalVert/255)<<décalerVert|((valeurCouleur&255)*maximalBleu/255)<<décalerBleu;
        for(unsigned indiceOrdinal=0;indiceOrdinal<taillePixel;indiceOrdinal++)Sortie[nombreÉlémentsSortie++]=valeur>>(8*(valeurOrdreOctetsGrand?taillePixel-1-indiceOrdinal:indiceOrdinal));
    }
}
void inspecterPrésenterDistant(void){
    if(extrémitéÉcouteEnCours<0)return;
    if(valeurPairRéseau<0){if(millisecondesÉcouléesCarteMatérielle()<encoreRecevoirActivé)return;valeurPairRéseau=accepterRéseauCourt(extrémitéÉcouteEnCours);if(valeurPairRéseau<0)return;
        tempsConnexion=millisecondesÉcouléesCarteMatérielle();valeurÉtapePhase=1;émettreValeur("RFB 003.008\n",12);memset(résuméPrécédentÉlément,0,sizeof(résuméPrécédentÉlément));
        taillePixel=4;valeurOrdreOctetsGrand=0;maximalRouge=maximalVert=maximalBleu=255;décalerRouge=16;décalerVert=8;décalerBleu=0;}
    if(valeurÉtapePhase<5&&millisecondesÉcouléesCarteMatérielle()-tempsConnexion>15000){fermer();return;}
    if(nombreÉlémentsSortie){int nombre=écrireRéseauCourt(valeurPairRéseau,Sortie+nombreÉlémentsEnvoyé,nombreÉlémentsSortie-nombreÉlémentsEnvoyé);if(nombre>0){nombreÉlémentsEnvoyé+=nombre;if(nombreÉlémentsEnvoyé==nombreÉlémentsSortie)nombreÉlémentsSortie=nombreÉlémentsEnvoyé=0;}else if(nombre!=-11){fermer();return;}}
    if(!nombreÉlémentsSortie&&futurFermer){fermer();return;}
    if(!nombreÉlémentsSortie&&positionTuile<nombreÉlémentsTuile)envoyerTuile();
    if(nombreÉlémentsEntrée==sizeof(valeurEntrée)){fermer();return;}
    int nombreÉlémentsReçu=lireRéseauCourt(valeurPairRéseau,valeurEntrée+nombreÉlémentsEntrée,sizeof(valeurEntrée)-nombreÉlémentsEntrée);
    if(nombreÉlémentsReçu==0||(nombreÉlémentsReçu<0&&nombreÉlémentsReçu!=-11)){fermer();return;}if(nombreÉlémentsReçu>0)nombreÉlémentsEntrée+=nombreÉlémentsReçu;
    if(nombreÉlémentsSortie||positionTuile<nombreÉlémentsTuile)return;
    if(valeurÉtapePhase==1&&nombreÉlémentsEntrée>=12){if(memcmp(valeurEntrée,"RFB 003.008\n",12)){fermer();return;}consommerValeur(12);const unsigned char méthodeAuthentification[]={1,2};émettreValeur(méthodeAuthentification,2);valeurÉtapePhase=2;return;}
    if(valeurÉtapePhase==2&&nombreÉlémentsEntrée){if(valeurEntrée[0]!=2||aléatoireDistant(valeurDéfi,16)){fermer();return;}consommerValeur(1);émettreValeur(valeurDéfi,16);valeurÉtapePhase=3;return;}
    if(valeurÉtapePhase==3&&nombreÉlémentsEntrée>=16){unsigned char matériauTouche[8],réponseAttendueCorrect[16];br_des_ct_cbcenc_keys valeurMotPasse;
        for(unsigned indiceOrdinal=0;indiceOrdinal<8;indiceOrdinal++){unsigned valeur=motPasseÉcran[indiceOrdinal],estInversé=0;for(unsigned ordinalInterne=0;ordinalInterne<8;ordinalInterne++){estInversé=(estInversé<<1)|(valeur&1);valeur>>=1;}matériauTouche[indiceOrdinal]=estInversé;}
        br_des_ct_cbcenc_init(&valeurMotPasse,matériauTouche,8);memcpy(réponseAttendueCorrect,valeurDéfi,16);
        for(unsigned indiceOrdinal=0;indiceOrdinal<16;indiceOrdinal+=8){unsigned char valeurVecteur[8]={0};br_des_ct_cbcenc_run(&valeurMotPasse,valeurVecteur,réponseAttendueCorrect+indiceOrdinal,8);memset(valeurVecteur,0,8);}
        unsigned valeurDifférence=0;for(unsigned indiceOrdinal=0;indiceOrdinal<16;indiceOrdinal++)valeurDifférence|=réponseAttendueCorrect[indiceOrdinal]^valeurEntrée[indiceOrdinal];consommerValeur(16);memset(&valeurMotPasse,0,sizeof(valeurMotPasse));memset(matériauTouche,0,8);memset(réponseAttendueCorrect,0,16);memset(valeurDéfi,0,16);
        écrire32Bits(Sortie,valeurDifférence?1:0);nombreÉlémentsSortie=4;nombreÉlémentsEnvoyé=0;
        if(valeurDifférence){écrire32Bits(Sortie+4,19);memcpy(Sortie+8,"Authentication fail",19);nombreÉlémentsSortie=27;futurFermer=1;}else valeurÉtapePhase=4;return;}
    if(valeurÉtapePhase==4&&nombreÉlémentsEntrée){consommerValeur(1);valeurLargeur=largeurÉcranCarteMatérielle();valeurHauteur=hauteurÉcranCarteMatérielle();if(!valeurLargeur||!valeurHauteur||valeurLargeur>1920||valeurHauteur>1080){fermer();return;}
        if(!terminalCarteMatérielle(7)){const unsigned char évènement[]={30,2,1,0,0,0,0};entréeDistantAlimenter(évènement,7);}
        memset(Sortie,0,40);écrire16Bits(Sortie,valeurLargeur);écrire16Bits(Sortie+2,valeurHauteur);Sortie[4]=32;Sortie[5]=24;Sortie[7]=1;
        écrire16Bits(Sortie+8,255);écrire16Bits(Sortie+10,255);écrire16Bits(Sortie+12,255);Sortie[14]=16;Sortie[15]=8;
        const char *nom="jkoros native";écrire32Bits(Sortie+20,strlen(nom));memcpy(Sortie+24,nom,strlen(nom));nombreÉlémentsSortie=24+strlen(nom);nombreÉlémentsEnvoyé=0;valeurÉtapePhase=5;return;}
    if(valeurÉtapePhase!=5||!nombreÉlémentsEntrée)return;
    unsigned catégorieType=valeurEntrée[0],valeurNécessaire=catégorieType==0?20:catégorieType==2?4:catégorieType==3?10:catégorieType==4?8:catégorieType==5?6:catégorieType==6?8:0;
    if(!valeurNécessaire){fermer();return;}if(nombreÉlémentsEntrée<valeurNécessaire)return;
    if(catégorieType==2){unsigned nombre=lire16Bits(valeurEntrée+2);if(nombre>128){fermer();return;}valeurNécessaire+=nombre*4;}
    if(catégorieType==6){unsigned nombre=lire32Bits(valeurEntrée+4);if(nombre>4096){fermer();return;}valeurNécessaire+=nombre;}
    if(nombreÉlémentsEntrée<valeurNécessaire)return;
    if(catégorieType==0){unsigned valeurBit=valeurEntrée[4],maximalCanalRouge=lire16Bits(valeurEntrée+8),valeurSecondes=lire16Bits(valeurEntrée+10),maximalCanalBleu=lire16Bits(valeurEntrée+12),décalerCanalRouge=valeurEntrée[14],décalerCanalVert=valeurEntrée[15],décalerCanalBleu=valeurEntrée[16];
        if((valeurBit!=16&&valeurBit!=32)||!valeurEntrée[7]||valeurEntrée[6]>1||!maximalCanalRouge||!valeurSecondes||!maximalCanalBleu||maximalCanalRouge>255||valeurSecondes>255||maximalCanalBleu>255||décalerCanalRouge>24||décalerCanalVert>24||décalerCanalBleu>24||
           ((uint64_t)maximalCanalRouge<<décalerCanalRouge)>((1ull<<valeurBit)-1)||((uint64_t)valeurSecondes<<décalerCanalVert)>((1ull<<valeurBit)-1)||((uint64_t)maximalCanalBleu<<décalerCanalBleu)>((1ull<<valeurBit)-1)){fermer();return;}
        taillePixel=valeurBit/8;valeurOrdreOctetsGrand=valeurEntrée[6];maximalRouge=maximalCanalRouge;maximalVert=valeurSecondes;maximalBleu=maximalCanalBleu;décalerRouge=décalerCanalRouge;décalerVert=décalerCanalVert;décalerBleu=décalerCanalBleu;memset(résuméPrécédentÉlément,0,sizeof(résuméPrécédentÉlément));
    }else if(catégorieType==3)requêteÉcran(valeurEntrée);
    else if(catégorieType==4)traitToucheDistant(lire32Bits(valeurEntrée+4),valeurEntrée[1]!=0);
    else if(catégorieType==5){unsigned coordonnéeCoordonnéeHorizontale=lire16Bits(valeurEntrée+2),coordonnéeCoordonnéeVerticale=lire16Bits(valeurEntrée+4);if(coordonnéeCoordonnéeHorizontale>=valeurLargeur)coordonnéeCoordonnéeHorizontale=valeurLargeur-1;if(coordonnéeCoordonnéeVerticale>=valeurHauteur)coordonnéeCoordonnéeVerticale=valeurHauteur-1;
        if(valeurEntrée[1])toucheDistantConfirmer();
        unsigned char évènement[]={30,1,valeurEntrée[1],coordonnéeCoordonnéeHorizontale&255,coordonnéeCoordonnéeHorizontale>>8,coordonnéeCoordonnéeVerticale&255,coordonnéeCoordonnéeVerticale>>8};entréeDistantAlimenter(évènement,sizeof(évènement));}
    consommerValeur(valeurNécessaire);
}

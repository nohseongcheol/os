#include "../nommage/nomsLierMachine.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "PileRéseau.h"
extern int32_t priseRéseauRéseauBoucleJava(int32_t,int32_t,int32_t), associerRéseauBoucleJava(int32_t,int32_t,int32_t);
extern int32_t envoyerRéseauBoucleJava(int32_t,int32_t,int32_t,int32_t), opérationRéceptionRéseauBoucleJava(int32_t,int32_t);
extern int32_t portRéseauBoucleJava(int32_t), adresseRéseauBoucleJava(int32_t), pairRéseauRéseauBoucleJava(int32_t), fermerRéseauBoucleJava(int32_t);
extern int32_t placerRéseauJava(int32_t,int32_t),obtenirRéseauJava(int32_t);
extern int32_t créerFluxBoucleJava(void),associerFluxBoucleJava(int32_t,int32_t,int32_t),écouterFluxBoucleJava(int32_t,int32_t);
extern int32_t connecterFluxBoucleJava(int32_t,int32_t,int32_t),accepterFluxBoucleJava(int32_t),lireFluxBoucleJava(int32_t,int32_t),écrireFluxBoucleJava(int32_t,int32_t);
extern int32_t portFluxBoucleJava(int32_t),pairRéseauFluxBoucleJava(int32_t),fermerFluxBoucleJava(int32_t);
static int extérieur[24];
static int adresseQuelconque[24], écouteurDouble[24], pairRéseauExtérieurUDP[8], adresseAssocié[8];
static int numéroExtérieur(int poignéeFichier) { return poignéeFichier>=32 && poignéeFichier<56 ? extérieur[poignéeFichier-32]-1 : -1; }
static int texteColler(int poignéeFichier,int catégorieType) {
    if(poignéeFichier<32||poignéeFichier>=56)return -9;int élémentListePrécédentÉlément=numéroExtérieur(poignéeFichier);if(élémentListePrécédentÉlément>=0)return élémentListePrécédentÉlément;
    int nombreÉlémentsÉlémentListe=créerExtrémitéPriseRéseau(catégorieType);if(nombreÉlémentsÉlémentListe>=0)extérieur[poignéeFichier-32]=nombreÉlémentsÉlémentListe+1;return nombreÉlémentsÉlémentListe;
}
int32_t priseRéseauRéseauJava(int32_t valeurPremier,int32_t valeurDeuxième,int32_t codeCaractère){return priseRéseauRéseauBoucleJava(valeurPremier,valeurDeuxième,codeCaractère);}
int32_t associerRéseauJava(int32_t poignéeFichier,int32_t AdresseInternet,int32_t numéroPort){
    if(AdresseInternet==0x7f000001)return associerRéseauBoucleJava(poignéeFichier,AdresseInternet,numéroPort);
    if(AdresseInternet!=0&&AdresseInternet!=lireÉtatRéseau(0,0))return -99;
    int valeurRetourné=associerRéseauBoucleJava(poignéeFichier,0,numéroPort);if(valeurRetourné<0)return valeurRetourné;
    int nombreÉlémentsÉlémentListe=texteColler(poignéeFichier,2);if(nombreÉlémentsÉlémentListe<0)return nombreÉlémentsÉlémentListe;valeurRetourné=associerRéseauCourt(nombreÉlémentsÉlémentListe,lireÉtatRéseau(0,0),portRéseauBoucleJava(poignéeFichier));if(!valeurRetourné)adresseAssocié[poignéeFichier-32]=AdresseInternet;return valeurRetourné;
}
int32_t envoyerRéseauJava(int32_t poignéeFichier,int32_t AdresseInternet,int32_t numéroPort,int32_t taille){
    if(AdresseInternet==0x7f000001)return envoyerRéseauBoucleJava(poignéeFichier,AdresseInternet,numéroPort,taille);
    if(taille<0||taille>512)return -90;if(numéroPort<1||numéroPort>65535)return -22;
    if(portRéseauBoucleJava(poignéeFichier)<0)return -9;
    if(adresseRéseauBoucleJava(poignéeFichier)==0x7f000001)return -101;
    int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe<0){int valeurRetourné=0;if(portRéseauBoucleJava(poignéeFichier)==0)valeurRetourné=associerRéseauBoucleJava(poignéeFichier,0,0);if(valeurRetourné<0)return valeurRetourné;nombreÉlémentsÉlémentListe=texteColler(poignéeFichier,2);if(nombreÉlémentsÉlémentListe<0)return nombreÉlémentsÉlémentListe;valeurRetourné=associerRéseauCourt(nombreÉlémentsÉlémentListe,lireÉtatRéseau(0,0),portRéseauBoucleJava(poignéeFichier));if(valeurRetourné<0)return valeurRetourné;}
    unsigned char Données[512];for(int indiceOrdinal=0;indiceOrdinal<taille;indiceOrdinal++)Données[indiceOrdinal]=obtenirRéseauJava(indiceOrdinal);return envoyerDatagramme(nombreÉlémentsÉlémentListe,Données,taille,AdresseInternet,numéroPort);
}
int32_t opérationRéceptionRéseauJava(int32_t poignéeFichier,int32_t taille){
    int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe<0)return opérationRéceptionRéseauBoucleJava(poignéeFichier,taille);if(taille<0||taille>512)return -22;
    int local=opérationRéceptionRéseauBoucleJava(poignéeFichier,taille);if(local!=-11){pairRéseauExtérieurUDP[poignéeFichier-32]=0;return local;}
    unsigned char Données[512];int valeurRetourné=recevoirDatagramme(nombreÉlémentsÉlémentListe,Données,taille);if(valeurRetourné>=0)pairRéseauExtérieurUDP[poignéeFichier-32]=1;for(int indiceOrdinal=0;indiceOrdinal<valeurRetourné;indiceOrdinal++)placerRéseauJava(indiceOrdinal,Données[indiceOrdinal]);return valeurRetourné;
}
int32_t portRéseauJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);return nombreÉlémentsÉlémentListe<0?portRéseauBoucleJava(poignéeFichier):(int32_t)numéroPortRéseau(nombreÉlémentsÉlémentListe);}
int32_t adresseRéseauJava(int32_t poignéeFichier){return numéroExtérieur(poignéeFichier)<0?adresseRéseauBoucleJava(poignéeFichier):adresseAssocié[poignéeFichier-32];}
int32_t pairRéseauRéseauJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);return nombreÉlémentsÉlémentListe<0||!pairRéseauExtérieurUDP[poignéeFichier-32]?pairRéseauRéseauBoucleJava(poignéeFichier):(int32_t)numéroPortPairRéseau(nombreÉlémentsÉlémentListe);}
int32_t distantRéseauJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);return nombreÉlémentsÉlémentListe<0||!pairRéseauExtérieurUDP[poignéeFichier-32]?0x7f000001:(int32_t)adressePairRéseauRéseauCourt(nombreÉlémentsÉlémentListe);}
int32_t fermerRéseauJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe>=0){fermerRéseau(nombreÉlémentsÉlémentListe);extérieur[poignéeFichier-32]=0;}if(poignéeFichier>=32&&poignéeFichier<40)pairRéseauExtérieurUDP[poignéeFichier-32]=adresseAssocié[poignéeFichier-32]=0;return fermerRéseauBoucleJava(poignéeFichier);}
int32_t créerFluxJava(void){return créerFluxBoucleJava();}
int32_t associerFluxJava(int32_t poignéeFichier,int32_t AdresseInternet,int32_t numéroPort){
    if(AdresseInternet==0||AdresseInternet==0x7f000001){int valeurRetourné=associerFluxBoucleJava(poignéeFichier,AdresseInternet,numéroPort);if(!valeurRetourné)adresseQuelconque[poignéeFichier-32]=AdresseInternet==0;return valeurRetourné;}
    if(AdresseInternet!=lireÉtatRéseau(0,0))return -99;int valeurRetourné=associerFluxBoucleJava(poignéeFichier,0,numéroPort);if(valeurRetourné<0)return valeurRetourné;
    int nombreÉlémentsÉlémentListe=texteColler(poignéeFichier,1);return nombreÉlémentsÉlémentListe<0?nombreÉlémentsÉlémentListe:associerRéseauCourt(nombreÉlémentsÉlémentListe,AdresseInternet,portFluxBoucleJava(poignéeFichier));
}
int32_t écouterFluxJava(int32_t poignéeFichier,int32_t attenteConnexions){
    int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe<0){int valeurRetourné=écouterFluxBoucleJava(poignéeFichier,attenteConnexions);if(valeurRetourné<0||!adresseQuelconque[poignéeFichier-32])return valeurRetourné;
        nombreÉlémentsÉlémentListe=texteColler(poignéeFichier,1);if(nombreÉlémentsÉlémentListe<0)return nombreÉlémentsÉlémentListe;valeurRetourné=associerRéseauCourt(nombreÉlémentsÉlémentListe,lireÉtatRéseau(0,0),portFluxBoucleJava(poignéeFichier));if(valeurRetourné<0)return valeurRetourné;écouteurDouble[poignéeFichier-32]=1;
    }return attenteConnexions<1?-22:écouterRéseauCourt(nombreÉlémentsÉlémentListe);
}
int32_t connecterFluxJava(int32_t poignéeFichier,int32_t AdresseInternet,int32_t numéroPort){
    if(AdresseInternet==0x7f000001 && numéroExtérieur(poignéeFichier)<0)return connecterFluxBoucleJava(poignéeFichier,AdresseInternet,numéroPort);
    if(portFluxBoucleJava(poignéeFichier)<0)return -9;int nombreÉlémentsÉlémentListe=texteColler(poignéeFichier,1);return nombreÉlémentsÉlémentListe<0?nombreÉlémentsÉlémentListe:connecterRéseauCourt(nombreÉlémentsÉlémentListe,AdresseInternet,numéroPort);
}
int32_t accepterFluxJava(int32_t poignéeFichier){
    int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe<0)return accepterFluxBoucleJava(poignéeFichier);
    if(écouteurDouble[poignéeFichier-32]){int local=accepterFluxBoucleJava(poignéeFichier);if(local!=-11)return local;}
    int valeurPairRéseau=accepterRéseauCourt(nombreÉlémentsÉlémentListe);if(valeurPairRéseau<0)return valeurPairRéseau;
    int valeurCible=créerFluxBoucleJava();if(valeurCible<0){fermerRéseau(valeurPairRéseau);return valeurCible;}extérieur[valeurCible-32]=valeurPairRéseau+1;return valeurCible;
}
int32_t lireFluxJava(int32_t poignéeFichier,int32_t taille){
    int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe<0)return lireFluxBoucleJava(poignéeFichier,taille);if(taille<0||taille>512)return -22;
    unsigned char Données[512];int valeurRetourné=lireRéseauCourt(nombreÉlémentsÉlémentListe,Données,taille);for(int indiceOrdinal=0;indiceOrdinal<valeurRetourné;indiceOrdinal++)placerRéseauJava(indiceOrdinal,Données[indiceOrdinal]);return valeurRetourné;
}
int32_t écrireFluxJava(int32_t poignéeFichier,int32_t taille){
    int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe<0)return écrireFluxBoucleJava(poignéeFichier,taille);if(taille<0||taille>512)return -22;
    unsigned char Données[512];for(int indiceOrdinal=0;indiceOrdinal<taille;indiceOrdinal++)Données[indiceOrdinal]=obtenirRéseauJava(indiceOrdinal);return écrireRéseauCourt(nombreÉlémentsÉlémentListe,Données,taille);
}
int32_t portFluxJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);return nombreÉlémentsÉlémentListe<0?portFluxBoucleJava(poignéeFichier):(int32_t)numéroPortRéseau(nombreÉlémentsÉlémentListe);}
int32_t pairRéseauFluxJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);return nombreÉlémentsÉlémentListe<0?pairRéseauFluxBoucleJava(poignéeFichier):(int32_t)numéroPortPairRéseau(nombreÉlémentsÉlémentListe);}
int32_t adresseFluxJava(int32_t poignéeFichier){return numéroExtérieur(poignéeFichier)<0?0x7f000001:écouteurDouble[poignéeFichier-32]?0:lireÉtatRéseau(0,0);}
int32_t fermerFluxJava(int32_t poignéeFichier){int nombreÉlémentsÉlémentListe=numéroExtérieur(poignéeFichier);if(nombreÉlémentsÉlémentListe>=0){fermerRéseau(nombreÉlémentsÉlémentListe);extérieur[poignéeFichier-32]=0;}if(poignéeFichier>=40&&poignéeFichier<56)adresseQuelconque[poignéeFichier-32]=écouteurDouble[poignéeFichier-32]=0;return fermerFluxBoucleJava(poignéeFichier);}

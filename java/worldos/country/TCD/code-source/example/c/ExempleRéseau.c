#include "ContratExemple.h"
#include <ABIRéseau.h>
int main(int nombreÉlémentsArgument,char **arguments) {
    if(nombreÉlémentsArgument!=2)return Sortie("사용법: ./네트워크 UDP창구번호\n");
    unsigned valeurPort=0;for(int nombre=0;arguments[1][nombre];nombre++) {
        if(arguments[1][nombre]<'0'||arguments[1][nombre]>'9')return 2;
        valeurPort=valeurPort*10+arguments[1][nombre]-'0';if(valeurPort>65535)return 2;
    }
    if(!valeurPort)return 2;
    int extrémité=créerExtrémité(FamilleInternet,PriseRéseauDatagramme,ProtocoleDatagramme);if(extrémité<0)return 3;
    struct AdressePriseRéseauInternet adresse={0};adresse.familleAdresse=FamilleInternet;
    if(associerAdresse(extrémité,(struct AdressePriseRéseau *)&adresse,sizeof(adresse))<0)return 4;
    adresse.numéroPort=courtRéseau(valeurPort);adresse.AdresseInternet.valeurAdresse=entierRéseau(0x0a000202);
    const char datagramme[]="C UDP français";
    if(envoyerDonnéesDatagramme(extrémité,datagramme,sizeof(datagramme)-1,0,(struct AdressePriseRéseau *)&adresse,sizeof(adresse))!=sizeof(datagramme)-1)return 5;
    char réponse[512];unsigned lancer=millisecondes();int nombreÉlémentsReçu;
    do {
        nombreÉlémentsReçu=recevoirDonnéesDatagramme(extrémité,réponse,sizeof(réponse),0,0,0);
        if(nombreÉlémentsReçu<0&&numéroErreur!=ErreurEncoreEssayer)return 6;
    } while(nombreÉlémentsReçu<0&&(unsigned)(millisecondes()-lancer)<700);
    fermerFichier(extrémité);if(nombreÉlémentsReçu!=sizeof(datagramme)-1)return 7;
    for(int nombre=0;nombre<nombreÉlémentsReçu;nombre++)if(datagramme[nombre]!=réponse[nombre])return 8;
    return Sortie("C 네트워크 vérifier: UDP français\n");
}

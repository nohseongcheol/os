#include "ContratExemple.h"
int main(void) {
    const char Données[]="C Fichier: fr 😀\n";
    int Fichier=ouvrirFichier("c.txt",ÉcrireLire|ManquantSiCréer|ContenuTronquer,0600);
    if(Fichier<0)return 1;
    if(écrireDonnéesFichier(Fichier,Données,sizeof(Données)-1)!=sizeof(Données)-1)return 2;
    if(positionnerFichier(Fichier,0,DébutDepuis)!=0)return 3;
    char lireValeurTexte[128]={0};int longueur=lireDonnéesFichier(Fichier,lireValeurTexte,sizeof(lireValeurTexte)-1);
    fermerFichier(Fichier);
    if(longueur!=sizeof(Données)-1)return 4;
    for(int nombre=0;nombre<longueur;nombre++)if(Données[nombre]!=lireValeurTexte[nombre])return 5;
    return Sortie(lireValeurTexte);
}

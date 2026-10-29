#include "../nommage/nomsLierMachine.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "invoquer.h"
#include "Paquet.h"
#include "uzlib.h"
static unsigned char archive[16384], dépaqueté[16385];
static unsigned taille, central, listeEntréesListe;
static char classeEntréeÉlément[256];
static unsigned lireOctetsDeux(unsigned positionActuel) { return archive[positionActuel] | archive[positionActuel+1] << 8; }
static uint32_t lireOctetsQuatre(unsigned positionActuel) { return lireOctetsDeux(positionActuel) | (uint32_t)lireOctetsDeux(positionActuel+2) << 16; }
static int rogner(unsigned positionActuel, unsigned nombreÉlémentsÉlémentListe, unsigned limiteCapacité) { return positionActuel <= limiteCapacité && nombreÉlémentsÉlémentListe <= limiteCapacité-positionActuel; }
static size_t longueur(const char *donnéesChaîne) { size_t nombreÉlémentsÉlémentListe=0; while(donnéesChaîne[nombreÉlémentsÉlémentListe]) nombreÉlémentsÉlémentListe++; return nombreÉlémentsÉlémentListe; }
static int texteÉgal(const unsigned char *valeurPremier, const unsigned char *valeurDeuxième, unsigned nombreÉlémentsÉlémentListe) { for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)if(valeurPremier[indiceOrdinal]!=valeurDeuxième[indiceOrdinal])return 0;return 1; }
static int finFichier(void *inutilisé) { (void)inutilisé; return -1; }
static int donnéesAttribut(const char *ligne,unsigned capacitéUtilisé,int *existePointEntréeÉlément) {
    if(capacitéUtilisé>=12 && texteÉgal((const unsigned char*)ligne,(const unsigned char*)"Class-Path: ",12))return -95;
    if(capacitéUtilisé>=12 && texteÉgal((const unsigned char*)ligne,(const unsigned char*)"Main-Class: ",12)) {
        unsigned valeur=capacitéUtilisé-12;if(*existePointEntréeÉlément||!valeur||valeur>=sizeof(classeEntréeÉlément))return -8;
        for(unsigned indiceOrdinal=0;indiceOrdinal<valeur;indiceOrdinal++){unsigned char codeCaractère=ligne[12+indiceOrdinal];if(codeCaractère<=32||codeCaractère=='/'||codeCaractère=='\\')return -8;classeEntréeÉlément[indiceOrdinal]=codeCaractère;}
        classeEntréeÉlément[valeur]=0;*existePointEntréeÉlément=1;
    }
    return 0;
}
static int membre(unsigned positionActuel, unsigned char *donnéesRésultat, unsigned maximalCapacité) {
    unsigned entréeÉlémentMéthode=lireOctetsDeux(positionActuel+10), bitsConfiguration=lireOctetsDeux(positionActuel+8), comprimé=lireOctetsQuatre(positionActuel+20), libérerTaille=lireOctetsQuatre(positionActuel+24), local=lireOctetsQuatre(positionActuel+42);
    unsigned nom=lireOctetsDeux(positionActuel+28);
    if(libérerTaille>maximalCapacité || libérerTaille>16384 || (entréeÉlémentMéthode!=0 && entréeÉlémentMéthode!=8) || (bitsConfiguration&~0x80e))return -8;
    if(!rogner(local,30,central) || lireOctetsQuatre(local)!=0x04034b50 || lireOctetsDeux(local+8)!=entréeÉlémentMéthode || lireOctetsDeux(local+6)!=bitsConfiguration || lireOctetsDeux(local+26)!=nom)return -8;
    unsigned démarrerDécalage=local+30, régionSupplémentaire=lireOctetsDeux(local+28);
    if(!rogner(démarrerDécalage,nom,central) || !texteÉgal(archive+démarrerDécalage,archive+positionActuel+46,nom))return -8;
    démarrerDécalage+=nom;if(!rogner(démarrerDécalage,régionSupplémentaire,central))return -8;démarrerDécalage+=régionSupplémentaire;
    if(!rogner(démarrerDécalage,comprimé,central))return -8;
    if(!(bitsConfiguration&8) && (lireOctetsQuatre(local+14)!=lireOctetsQuatre(positionActuel+16) || lireOctetsQuatre(local+18)!=comprimé || lireOctetsQuatre(local+22)!=libérerTaille))return -8;
    if(entréeÉlémentMéthode==0) { if(comprimé!=libérerTaille)return -8; for(unsigned indiceOrdinal=0;indiceOrdinal<libérerTaille;indiceOrdinal++)donnéesRésultat[indiceOrdinal]=archive[démarrerDécalage+indiceOrdinal]; }
    else {
        uzlib_uncomp_t donnéesDestination={0};uzlib_uncompress_init(&donnéesDestination,0,0);
        donnéesDestination.source=archive+démarrerDécalage;donnéesDestination.source_limit=donnéesDestination.source+comprimé;donnéesDestination.source_read_cb=finFichier;
        /* One extra output byte lets inflate consume/check the end marker. */
        donnéesDestination.dest_start=donnéesDestination.dest=dépaqueté;donnéesDestination.dest_limit=dépaqueté+libérerTaille+1;
        int valeurRetourné=uzlib_uncompress(&donnéesDestination);
        if(valeurRetourné!=UZLIB_DONE || donnéesDestination.eof || donnéesDestination.dest!=dépaqueté+libérerTaille || donnéesDestination.source!=donnéesDestination.source_limit)return -8;
        for(unsigned indiceOrdinal=0;indiceOrdinal<libérerTaille;indiceOrdinal++)donnéesRésultat[indiceOrdinal]=dépaqueté[indiceOrdinal];
    }
    if((uzlib_crc32(donnéesRésultat,libérerTaille,0xffffffffu)^0xffffffffu)!=lireOctetsQuatre(positionActuel+16))return -8;
    return libérerTaille;
}
int lireJAR(const char *nom, unsigned char *donnéesRésultat, unsigned capacitéTampon) {
    if(!listeEntréesListe)return -2;unsigned nombreÉlémentsÉlémentListe=longueur(nom),positionActuel=central;
    for(unsigned indiceOrdinal=0;indiceOrdinal<listeEntréesListe;indiceOrdinal++) {
        unsigned longueurNom=lireOctetsDeux(positionActuel+28);
        if(longueurNom==nombreÉlémentsÉlémentListe && texteÉgal(archive+positionActuel+46,(const unsigned char*)nom,nombreÉlémentsÉlémentListe))return membre(positionActuel,donnéesRésultat,capacitéTampon);
        positionActuel+=46+longueurNom+lireOctetsDeux(positionActuel+30)+lireOctetsDeux(positionActuel+32);
    }
    return -2;
}
const char *principalJAR(void) { return classeEntréeÉlément; }
int ouvrirJAR(const char *nomEntréeÉlémentFichier) {
    listeEntréesListe=0;classeEntréeÉlément[0]=0;
    intptr_t poignéeFichier=invoquerUtilisateur(3,(uintptr_t)nomEntréeÉlémentFichier,0,0,0,0,0);if(poignéeFichier<0)return poignéeFichier;
    intptr_t nombreÉlémentsÉlémentListe=invoquerUtilisateur(9,poignéeFichier,0,0,0,0,0);
    if(nombreÉlémentsÉlémentListe<22 || nombreÉlémentsÉlémentListe>(intptr_t)sizeof(archive)) { invoquerUtilisateur(4,poignéeFichier,0,0,0,0,0);return -8; }
    intptr_t nombreÉlémentsReçu=invoquerUtilisateur(2,poignéeFichier,(uintptr_t)archive,nombreÉlémentsÉlémentListe,0,0,0);invoquerUtilisateur(4,poignéeFichier,0,0,0,0,0);
    if(nombreÉlémentsReçu!=nombreÉlémentsÉlémentListe)return -5;taille=nombreÉlémentsÉlémentListe;
    unsigned décalageFin=taille-22;
    for(;;) { if(lireOctetsQuatre(décalageFin)==0x06054b50 && décalageFin+22+lireOctetsDeux(décalageFin+20)==taille)break; if(!décalageFin)return -8;décalageFin--; }
    unsigned nombreÉlémentsEntréeÉlément=lireOctetsDeux(décalageFin+10);central=lireOctetsQuatre(décalageFin+16);
    if(lireOctetsDeux(décalageFin+4)||lireOctetsDeux(décalageFin+6)||lireOctetsDeux(décalageFin+8)!=nombreÉlémentsEntréeÉlément||!nombreÉlémentsEntréeÉlément||nombreÉlémentsEntréeÉlément>256||!rogner(central,lireOctetsQuatre(décalageFin+12),décalageFin)||central+lireOctetsQuatre(décalageFin+12)!=décalageFin)return -8;
    unsigned positionActuel=central;
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsEntréeÉlément;indiceOrdinal++) {
        if(!rogner(positionActuel,46,décalageFin)||lireOctetsQuatre(positionActuel)!=0x02014b50||lireOctetsDeux(positionActuel+34))return -8;
        unsigned longueurNom=lireOctetsDeux(positionActuel+28),élémentListeSuivant=46+longueurNom+lireOctetsDeux(positionActuel+30)+lireOctetsDeux(positionActuel+32);
        if(!longueurNom||longueurNom>511||!rogner(positionActuel,élémentListeSuivant,décalageFin)||lireOctetsQuatre(positionActuel+24)>16384)return -8;
        for(unsigned ordinalInterne=0;ordinalInterne<longueurNom;ordinalInterne++)if(!archive[positionActuel+46+ordinalInterne])return -8;
        unsigned entréeÉlémentAutre=central;
        for(unsigned ordinalInterne=0;ordinalInterne<indiceOrdinal;ordinalInterne++){unsigned donnéesLongueur=lireOctetsDeux(entréeÉlémentAutre+28);if(donnéesLongueur==longueurNom&&texteÉgal(archive+entréeÉlémentAutre+46,archive+positionActuel+46,donnéesLongueur))return -8;entréeÉlémentAutre+=46+donnéesLongueur+lireOctetsDeux(entréeÉlémentAutre+30)+lireOctetsDeux(entréeÉlémentAutre+32);}
        positionActuel+=élémentListeSuivant;
    }
    if(positionActuel!=décalageFin)return -8;listeEntréesListe=nombreÉlémentsEntréeÉlément;
    unsigned char manifesteLot[4096];int tailleGroupe=lireJAR("META-INF/MANIFEST.MF",manifesteLot,sizeof(manifesteLot)-1);if(tailleGroupe<0){listeEntréesListe=0;return -8;}
    manifesteLot[tailleGroupe]=0;
    char logique[512];unsigned capacitéUtilisé=0,valeurIndice=0;int existePointEntréeÉlément=0;
    while(valeurIndice<(unsigned)tailleGroupe) {
        unsigned lancer=valeurIndice;while(valeurIndice<(unsigned)tailleGroupe && manifesteLot[valeurIndice]!='\n')valeurIndice++;
        unsigned donnéesLongueur=valeurIndice-lancer;if(valeurIndice<(unsigned)tailleGroupe)valeurIndice++;if(donnéesLongueur && manifesteLot[lancer+donnéesLongueur-1]=='\r')donnéesLongueur--;
        if(capacitéUtilisé && donnéesLongueur && manifesteLot[lancer]==' ') {lancer++;donnéesLongueur--;}
        else {
            int résultat=donnéesAttribut(logique,capacitéUtilisé,&existePointEntréeÉlément);if(résultat)return résultat;
            capacitéUtilisé=0;if(!donnéesLongueur)break;
        }
        if(donnéesLongueur>sizeof(logique)-capacitéUtilisé)return -8;
        for(unsigned indiceOrdinal=0;indiceOrdinal<donnéesLongueur;indiceOrdinal++)logique[capacitéUtilisé++]=manifesteLot[lancer+indiceOrdinal];
    }
    /* The last attribute may be followed by only one newline. */
    int résultat=donnéesAttribut(logique,capacitéUtilisé,&existePointEntréeÉlément);if(résultat)return résultat;
    return existePointEntréeÉlément?0:-8;
}

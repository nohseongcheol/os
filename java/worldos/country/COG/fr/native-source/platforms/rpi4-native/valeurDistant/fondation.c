/* valeurNoyau 전용 할당기와 valeurMotPasse 난수 공급. Utilisateur ELF의 libc와 별개이다. */
#include "priseEnChargeCryptographie.h"
#include "../nommage/nomsLierMachine.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t millisecondesÉcouléesCarteMatérielle(void);
typedef struct blocMémoire { size_t longueur; struct blocMémoire *élémentListeSuivant; int valeurUtiliser; } blocMémoire;
static unsigned char arèneMémoireMémoire[2*1024*1024] __attribute__((aligned(16)));
static blocMémoire *valeurFragmentPremier;
void *allouerDistant(size_t longueur) {
    if (!longueur || longueur>sizeof(arèneMémoireMémoire)-64) return 0;
    longueur=(longueur+15)&~(size_t)15;
    if(!valeurFragmentPremier){valeurFragmentPremier=(void*)arèneMémoireMémoire;valeurFragmentPremier->longueur=sizeof(arèneMémoireMémoire)-32;}
    for(blocMémoire *valeurFragment=valeurFragmentPremier;valeurFragment;valeurFragment=valeurFragment->élémentListeSuivant)if(!valeurFragment->valeurUtiliser&&valeurFragment->longueur>=longueur){
        if(valeurFragment->longueur>=longueur+64){blocMémoire *fragmentNouveau=(void*)((char*)valeurFragment+32+longueur);
            fragmentNouveau->longueur=valeurFragment->longueur-longueur-32;fragmentNouveau->élémentListeSuivant=valeurFragment->élémentListeSuivant;fragmentNouveau->valeurUtiliser=0;valeurFragment->élémentListeSuivant=fragmentNouveau;valeurFragment->longueur=longueur;}
        valeurFragment->valeurUtiliser=1;return(char*)valeurFragment+32;
    }return 0;
}
void libérerDistant(void *adresse) {
    if(!adresse)return;blocMémoire *valeurFragment=(void*)((char*)adresse-32);
    volatile unsigned char *valeurEffacé=adresse;for(size_t indiceOrdinal=0;indiceOrdinal<valeurFragment->longueur;indiceOrdinal++)valeurEffacé[indiceOrdinal]=0;
    valeurFragment->valeurUtiliser=0;
    for(valeurFragment=valeurFragmentPremier;valeurFragment&&valeurFragment->élémentListeSuivant;){if(!valeurFragment->valeurUtiliser&&!valeurFragment->élémentListeSuivant->valeurUtiliser){valeurFragment->longueur+=32+valeurFragment->élémentListeSuivant->longueur;valeurFragment->élémentListeSuivant=valeurFragment->élémentListeSuivant->élémentListeSuivant;}else valeurFragment=valeurFragment->élémentListeSuivant;}
}
void *réallouerDistant(void *adresse,size_t longueur){
    if(!adresse)return allouerDistant(longueur);if(!longueur){libérerDistant(adresse);return 0;}
    blocMémoire *valeurFragment=(void*)((char*)adresse-32);void *adresseNouveau=allouerDistant(longueur);
    if(adresseNouveau){memcpy(adresseNouveau,adresse,longueur<valeurFragment->longueur?longueur:valeurFragment->longueur);libérerDistant(adresse);}return adresseNouveau;
}
int strcmp(const char *opérandePremier,const char *opérandeDeuxième){while(*opérandePremier&&*opérandePremier==*opérandeDeuxième){opérandePremier++;opérandeDeuxième++;}return(unsigned char)*opérandePremier-(unsigned char)*opérandeDeuxième;}
char *strchr(const char *texteMot,int valeurCaractère){for(;;texteMot++){if(*texteMot==(char)valeurCaractère)return(char*)texteMot;if(!*texteMot)return 0;}}
char *strstr(const char *texteMot,const char *valeurTrouvé){size_t longueur=strlen(valeurTrouvé);for(;*texteMot;texteMot++)if(!strncmp(texteMot,valeurTrouvé,longueur))return(char*)texteMot;return longueur?0:(char*)texteMot;}
char *strncpy(char *valeurDestination,const char *original,size_t longueur){size_t indiceOrdinal=0;for(;indiceOrdinal<longueur&&original[indiceOrdinal];indiceOrdinal++)valeurDestination[indiceOrdinal]=original[indiceOrdinal];for(;indiceOrdinal<longueur;indiceOrdinal++)valeurDestination[indiceOrdinal]=0;return valeurDestination;}
char *strncat(char *valeurDestination,const char *original,size_t longueur){char *terminaison=valeurDestination+strlen(valeurDestination);while(longueur--&&*original)*terminaison++=*original++;*terminaison=0;return valeurDestination;}
int strncasecmp(const char *opérandePremier,const char *opérandeDeuxième,size_t longueur){while(longueur--){unsigned caractèrePremier=*opérandePremier++,caractèreDeuxième=*opérandeDeuxième++;if(caractèrePremier>='A'&&caractèrePremier<='Z')caractèrePremier+=32;if(caractèreDeuxième>='A'&&caractèreDeuxième<='Z')caractèreDeuxième+=32;if(caractèrePremier!=caractèreDeuxième)return(int)caractèrePremier-(int)caractèreDeuxième;if(!caractèrePremier)break;}return 0;}
int strcasecmp(const char *opérandePremier,const char *opérandeDeuxième){return strncasecmp(opérandePremier,opérandeDeuxième,(size_t)-1);}
char *strtok_r(char *texteMot,const char *valeurDélimiteur,char **élémentListeSuivant){if(!texteMot)texteMot=*élémentListeSuivant;while(*texteMot&&strchr(valeurDélimiteur,*texteMot))texteMot++;if(!*texteMot){*élémentListeSuivant=texteMot;return 0;}char *élémentListeInitialValeur=texteMot;while(*texteMot&&!strchr(valeurDélimiteur,*texteMot))texteMot++;if(*texteMot)*texteMot++=0;*élémentListeSuivant=texteMot;return élémentListeInitialValeur;}
unsigned long strtoul(const char *texteMot, char **terminaison, int valeurBase) {
    const char *source=texteMot;unsigned long valeur=0;int valeurNégatif=0,valeurDébordement=0;
    while(*texteMot==' '||(*texteMot>=9&&*texteMot<=13))texteMot++;
    if(*texteMot=='-'||*texteMot=='+')valeurNégatif=*texteMot++=='-';
    if((valeurBase==0||valeurBase==16)&&texteMot[0]=='0'&&(texteMot[1]=='x'||texteMot[1]=='X')&&
       ((texteMot[2]>='0'&&texteMot[2]<='9')||(texteMot[2]>='a'&&texteMot[2]<='f')||(texteMot[2]>='A'&&texteMot[2]<='F'))) {valeurBase=16;texteMot+=2;}
    if(!valeurBase)valeurBase=*texteMot=='0'?8:10;
    if(valeurBase<2||valeurBase>36){if(terminaison)*terminaison=(char*)source;return 0;}
    const char *élémentListeInitialValeur=texteMot;
    for(;;texteMot++) {
        unsigned valeurCaractère=(unsigned char)*texteMot;
        unsigned nombre=valeurCaractère>='0'&&valeurCaractère<='9'?valeurCaractère-'0':valeurCaractère>='a'&&valeurCaractère<='z'?valeurCaractère-'a'+10:valeurCaractère>='A'&&valeurCaractère<='Z'?valeurCaractère-'A'+10:36;
        if(nombre>=(unsigned)valeurBase)break;
        if(valeur>(~0ul-nombre)/(unsigned)valeurBase)valeurDébordement=1;
        if(!valeurDébordement)valeur=valeur*(unsigned)valeurBase+nombre;
    }
    if(terminaison)*terminaison=(char*)(texteMot==élémentListeInitialValeur?source:texteMot);
    return valeurDébordement?~0ul:valeurNégatif?0ul-valeur:valeur;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char graineSimulacre[32];
static int étatValeurGraine;
void résuméDistant(const void *Données, size_t longueur, unsigned char résultat[32]) {
    br_sha256_context valeurContexte;
    br_sha256_init(&valeurContexte); br_sha256_update(&valeurContexte, Données, longueur); br_sha256_out(&valeurContexte, résultat);
    memset(&valeurContexte, 0, sizeof(valeurContexte));
}
#define registresAléatoire(position) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(position)))
int aléatoireDistant(unsigned char *valeurDestination,unsigned longueur){
    if(!étatValeurGraine){volatile unsigned char *Données=(void*)0x01ff0000ul;const char *valeurMarqueur="JKRENRG1";unsigned valeurDifférence=0;
        for(unsigned indiceOrdinal=0;indiceOrdinal<8;indiceOrdinal++)valeurDifférence|=Données[indiceOrdinal]^(unsigned char)valeurMarqueur[indiceOrdinal];
        if(!valeurDifférence){for(unsigned indiceOrdinal=0;indiceOrdinal<32;indiceOrdinal++)graineSimulacre[indiceOrdinal]=Données[8+indiceOrdinal];for(unsigned indiceOrdinal=0;indiceOrdinal<40;indiceOrdinal++)Données[indiceOrdinal]=0;étatValeurGraine=2;}
        else {étatValeurGraine=1;registresAléatoire(0)=(registresAléatoire(0)&~0x1fffu)|1;}
    }
    if(étatValeurGraine==2){while(longueur){unsigned char élémentListeSuivant[32],valeurEntrée[33];memcpy(valeurEntrée,graineSimulacre,32);valeurEntrée[32]=0;résuméDistant(valeurEntrée,33,élémentListeSuivant);
        valeurEntrée[32]=1;résuméDistant(valeurEntrée,33,graineSimulacre);memset(valeurEntrée,0,33);
        unsigned nombre=longueur<32?longueur:32;memcpy(valeurDestination,élémentListeSuivant,nombre);memset(élémentListeSuivant,0,32);valeurDestination+=nombre;longueur-=nombre;}return 0;}
    uintptr_t valeurLimite=millisecondesÉcouléesCarteMatérielle()+1000;
    while(longueur){if((registresAléatoire(0x18)&0x80000020u)||millisecondesÉcouléesCarteMatérielle()>valeurLimite)return -1;
        if(!(registresAléatoire(0x24)&255))continue;uint32_t valeur=registresAléatoire(0x20);
        for(unsigned indiceOrdinal=0;indiceOrdinal<4&&longueur;indiceOrdinal++,longueur--){*valeurDestination++=valeur&255;valeur>>=8;}}
    return 0;
}

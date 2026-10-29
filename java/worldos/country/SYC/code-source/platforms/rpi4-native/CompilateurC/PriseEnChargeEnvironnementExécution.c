#include "../nommage/nomsLierMachine.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "invoquer.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int erreur;
int *__errno_location(void){return &erreur;}
void exit(int valeurÉtatValeur){invoquerUtilisateur(6,valeurÉtatValeur,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *contrôlerExpression,const char *Fichier,unsigned ligne,const char *nomEntréeÉlémentMéthode){fprintf(stderr,"cc assertion: %s %s:%u %s\n",contrôlerExpression,Fichier,ligne,nomEntréeÉlémentMéthode);exit(1);}
size_t strlen(const char*donnéesChaîne){const char*positionDonnées=donnéesChaîne;while(*positionDonnées)positionDonnées++;return positionDonnées-donnéesChaîne;}
int strcmp(const char*valeurPremier,const char*valeurDeuxième){while(*valeurPremier&&*valeurPremier==*valeurDeuxième){valeurPremier++;valeurDeuxième++;}return (unsigned char)*valeurPremier-(unsigned char)*valeurDeuxième;}
int strncmp(const char*valeurPremier,const char*valeurDeuxième,size_t nombreÉlémentsÉlémentListe){while(nombreÉlémentsÉlémentListe--){unsigned char coordonnéeCoordonnéeHorizontale=*valeurPremier++,coordonnéeCoordonnéeVerticale=*valeurDeuxième++;if(coordonnéeCoordonnéeHorizontale!=coordonnéeCoordonnéeVerticale)return coordonnéeCoordonnéeHorizontale-coordonnéeCoordonnéeVerticale;if(!coordonnéeCoordonnéeHorizontale)return 0;}return 0;}
char *strcpy(char*donnéesDestination,const char*donnéesChaîne){char*valeurRetourné=donnéesDestination;while((*donnéesDestination++=*donnéesChaîne++)){}return valeurRetourné;}
char *strchr(const char*donnéesChaîne,int codeCaractère){do{if(*donnéesChaîne==(char)codeCaractère)return (char*)donnéesChaîne;}while(*donnéesChaîne++);return 0;}
char *strrchr(const char*donnéesChaîne,int codeCaractère){const char*valeurRetourné=0;do{if(*donnéesChaîne==(char)codeCaractère)valeurRetourné=donnéesChaîne;}while(*donnéesChaîne++);return (char*)valeurRetourné;}
char *strstr(const char*donnéesChaîne,const char*entréeÉlémentTerminal){size_t nombreÉlémentsÉlémentListe=strlen(entréeÉlémentTerminal);for(;*donnéesChaîne;donnéesChaîne++)if(!strncmp(donnéesChaîne,entréeÉlémentTerminal,nombreÉlémentsÉlémentListe))return (char*)donnéesChaîne;return nombreÉlémentsÉlémentListe?0:(char*)donnéesChaîne;}
int memcmp(const void*valeurPremier,const void*valeurDeuxième,size_t nombreÉlémentsÉlémentListe){const unsigned char*coordonnéeCoordonnéeHorizontale=valeurPremier,*coordonnéeCoordonnéeVerticale=valeurDeuxième;while(nombreÉlémentsÉlémentListe--){if(*coordonnéeCoordonnéeHorizontale!=*coordonnéeCoordonnéeVerticale)return *coordonnéeCoordonnéeHorizontale-*coordonnéeCoordonnéeVerticale;coordonnéeCoordonnéeHorizontale++;coordonnéeCoordonnéeVerticale++;}return 0;}
void *memmove(void*donnéesDestination,const void*donnéesChaîne,size_t nombreÉlémentsÉlémentListe){unsigned char*coordonnéeCoordonnéeHorizontale=donnéesDestination;const unsigned char*coordonnéeCoordonnéeVerticale=donnéesChaîne;if(coordonnéeCoordonnéeHorizontale<coordonnéeCoordonnéeVerticale){for(size_t indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)coordonnéeCoordonnéeHorizontale[indiceOrdinal]=coordonnéeCoordonnéeVerticale[indiceOrdinal];}else while(nombreÉlémentsÉlémentListe){nombreÉlémentsÉlémentListe--;coordonnéeCoordonnéeHorizontale[nombreÉlémentsÉlémentListe]=coordonnéeCoordonnéeVerticale[nombreÉlémentsÉlémentListe];}return donnéesDestination;}
static unsigned char arèneMémoireAllocation[6*1024*1024] __attribute__((aligned(16)));
typedef struct blocDonnées {size_t taille;struct blocDonnées*élémentListeSuivant;int capacitéRestant;int rembourrage;uint64_t unitéAlignement;} blocDonnées;
static blocDonnées *entréeÉlémentPremier;
void free(void*positionDonnées){if(!positionDonnées)return;blocDonnées*valeurDeuxième=(blocDonnées*)positionDonnées-1;valeurDeuxième->capacitéRestant=1;for(blocDonnées*décalageSuivant=entréeÉlémentPremier;décalageSuivant&&décalageSuivant->élémentListeSuivant;){if(décalageSuivant->capacitéRestant&&décalageSuivant->élémentListeSuivant->capacitéRestant){décalageSuivant->taille+=sizeof(blocDonnées)+décalageSuivant->élémentListeSuivant->taille;décalageSuivant->élémentListeSuivant=décalageSuivant->élémentListeSuivant->élémentListeSuivant;}else décalageSuivant=décalageSuivant->élémentListeSuivant;}}
void *realloc(void*positionDonnées,size_t nombreÉlémentsÉlémentListe){
    if(!nombreÉlémentsÉlémentListe){free(positionDonnées);return 0;}if(nombreÉlémentsÉlémentListe>sizeof(arèneMémoireAllocation)-sizeof(blocDonnées))return 0;nombreÉlémentsÉlémentListe=(nombreÉlémentsÉlémentListe+15)&~(size_t)15;
    if(!entréeÉlémentPremier){entréeÉlémentPremier=(blocDonnées*)arèneMémoireAllocation;entréeÉlémentPremier->taille=sizeof(arèneMémoireAllocation)-sizeof(blocDonnées);entréeÉlémentPremier->capacitéRestant=1;entréeÉlémentPremier->élémentListeSuivant=0;}
    blocDonnées*élémentListePrécédentÉlément=positionDonnées?(blocDonnées*)positionDonnées-1:0;if(élémentListePrécédentÉlément&&élémentListePrécédentÉlément->taille>=nombreÉlémentsÉlémentListe)return positionDonnées;
    for(blocDonnées*valeurDeuxième=entréeÉlémentPremier;valeurDeuxième;valeurDeuxième=valeurDeuxième->élémentListeSuivant)if(valeurDeuxième->capacitéRestant&&valeurDeuxième->taille>=nombreÉlémentsÉlémentListe){
        if(valeurDeuxième->taille>=nombreÉlémentsÉlémentListe+sizeof(blocDonnées)+16){blocDonnées*partieRestant=(blocDonnées*)((unsigned char*)(valeurDeuxième+1)+nombreÉlémentsÉlémentListe);partieRestant->taille=valeurDeuxième->taille-nombreÉlémentsÉlémentListe-sizeof(blocDonnées);partieRestant->élémentListeSuivant=valeurDeuxième->élémentListeSuivant;partieRestant->capacitéRestant=1;valeurDeuxième->élémentListeSuivant=partieRestant;valeurDeuxième->taille=nombreÉlémentsÉlémentListe;}
        valeurDeuxième->capacitéRestant=0;void*valeurRetourné=valeurDeuxième+1;if(élémentListePrécédentÉlément){memcpy(valeurRetourné,positionDonnées,élémentListePrécédentÉlément->taille);free(positionDonnées);}return valeurRetourné;
    }erreur=12;return 0;
}
void *malloc(size_t nombreÉlémentsÉlémentListe){return realloc(0,nombreÉlémentsÉlémentListe);}
void *calloc(size_t nombreÉlémentsÉlémentListe,size_t donnéesChaîne){if(donnéesChaîne&&nombreÉlémentsÉlémentListe>SIZE_MAX/donnéesChaîne)return 0;void*positionDonnées=malloc(nombreÉlémentsÉlémentListe*donnéesChaîne);if(positionDonnées)memset(positionDonnées,0,nombreÉlémentsÉlémentListe*donnéesChaîne);return positionDonnées;}
unsigned long long strtoull(const char*donnéesChaîne,char**décalageFin,int valeurArrièrePlan){
    const char*démarrerDécalage=donnéesChaîne;while(*donnéesChaîne==' '||(*donnéesChaîne>=9&&*donnéesChaîne<=13))donnéesChaîne++;int estNégatif=0;if(*donnéesChaîne=='-'||*donnéesChaîne=='+')estNégatif=*donnéesChaîne++=='-';
    if((!valeurArrièrePlan||valeurArrièrePlan==16)&&donnéesChaîne[0]=='0'&&(donnéesChaîne[1]=='x'||donnéesChaîne[1]=='X')){valeurArrièrePlan=16;donnéesChaîne+=2;}if(!valeurArrièrePlan)valeurArrièrePlan=*donnéesChaîne=='0'?8:10;
    unsigned long long donnéesTemporaire=0;int valeurQuelconque=0;for(;;){unsigned codeCaractère=*donnéesChaîne,donnéesDestination=codeCaractère>='0'&&codeCaractère<='9'?codeCaractère-'0':codeCaractère>='a'&&codeCaractère<='z'?codeCaractère-'a'+10:codeCaractère>='A'&&codeCaractère<='Z'?codeCaractère-'A'+10:99;if(donnéesDestination>=(unsigned)valeurArrièrePlan)break;valeurQuelconque=1;donnéesChaîne++;if(donnéesTemporaire>(~0ull-donnéesDestination)/(unsigned)valeurArrièrePlan){donnéesTemporaire=~0ull;erreur=34;}else donnéesTemporaire=donnéesTemporaire*valeurArrièrePlan+donnéesDestination;}
    if(décalageFin)*décalageFin=(char*)(valeurQuelconque?donnéesChaîne:démarrerDécalage);return estNégatif?0-donnéesTemporaire:donnéesTemporaire;
}
unsigned long strtoul(const char*donnéesChaîne,char**entréeÉlémentAuxiliaire,int valeurDeuxième){return strtoull(donnéesChaîne,entréeÉlémentAuxiliaire,valeurDeuxième);}
long strtol(const char*donnéesChaîne,char**entréeÉlémentAuxiliaire,int valeurDeuxième){return (long)strtoull(donnéesChaîne,entréeÉlémentAuxiliaire,valeurDeuxième);}
int atoi(const char*donnéesChaîne){return (int)strtol(donnéesChaîne,0,10);}
long double ldexpl(long double coordonnéeCoordonnéeHorizontale,int nombreÉlémentsÉlémentListe){while(nombreÉlémentsÉlémentListe>0){coordonnéeCoordonnéeHorizontale*=2;nombreÉlémentsÉlémentListe--;}while(nombreÉlémentsÉlémentListe<0){coordonnéeCoordonnéeHorizontale/=2;nombreÉlémentsÉlémentListe++;}return coordonnéeCoordonnéeHorizontale;}
long double strtold(const char*donnéesChaîne,char**décalageFin){
    const char*démarrerDécalage=donnéesChaîne;while(*donnéesChaîne==' '||(*donnéesChaîne>=9&&*donnéesChaîne<=13))donnéesChaîne++;int estNégatif=0;if(*donnéesChaîne=='-'||*donnéesChaîne=='+')estNégatif=*donnéesChaîne++=='-';
    int valeurArrièrePlan=10;if(donnéesChaîne[0]=='0'&&(donnéesChaîne[1]=='x'||donnéesChaîne[1]=='X')){valeurArrièrePlan=16;donnéesChaîne+=2;}long double donnéesTemporaire=0,échelle=1;int fractionnaire=0,valeurQuelconque=0;
    for(;;){int codeCaractère=*donnéesChaîne,donnéesDestination=codeCaractère>='0'&&codeCaractère<='9'?codeCaractère-'0':codeCaractère>='a'&&codeCaractère<='f'?codeCaractère-'a'+10:codeCaractère>='A'&&codeCaractère<='F'?codeCaractère-'A'+10:99;
        if(codeCaractère=='.'&&!fractionnaire){fractionnaire=1;donnéesChaîne++;continue;}if(donnéesDestination>=valeurArrièrePlan)break;valeurQuelconque=1;donnéesChaîne++;donnéesTemporaire=donnéesTemporaire*valeurArrièrePlan+donnéesDestination;if(fractionnaire)échelle*=valeurArrièrePlan;
    }donnéesTemporaire/=échelle;
    if((valeurArrièrePlan==10&&(*donnéesChaîne=='e'||*donnéesChaîne=='E'))||(valeurArrièrePlan==16&&(*donnéesChaîne=='p'||*donnéesChaîne=='P'))){const char*afficherValeur=donnéesChaîne++;int soustraireValeurs=0;if(*donnéesChaîne=='-'||*donnéesChaîne=='+')soustraireValeurs=*donnéesChaîne++=='-';int nombreÉlémentsÉlémentListe=0,nombreÉlémentsEntréeÉlément=0;while(*donnéesChaîne>='0'&&*donnéesChaîne<='9'){nombreÉlémentsEntréeÉlément++;if(nombreÉlémentsÉlémentListe<20000)nombreÉlémentsÉlémentListe=nombreÉlémentsÉlémentListe*10+*donnéesChaîne-'0';donnéesChaîne++;}if(!nombreÉlémentsEntréeÉlément)donnéesChaîne=afficherValeur;else{long double facteur=valeurArrièrePlan==16?2:10;while(nombreÉlémentsÉlémentListe-->0&&nombreÉlémentsÉlémentListe<200000)donnéesTemporaire=soustraireValeurs?donnéesTemporaire/facteur:donnéesTemporaire*facteur;}}
    if(décalageFin)*décalageFin=(char*)(valeurQuelconque?donnéesChaîne:démarrerDécalage);return estNégatif?-donnéesTemporaire:donnéesTemporaire;
}
double strtod(const char*donnéesChaîne,char**entréeÉlémentAuxiliaire){return (double)strtold(donnéesChaîne,entréeÉlémentAuxiliaire);}float strtof(const char*donnéesChaîne,char**entréeÉlémentAuxiliaire){return (float)strtold(donnéesChaîne,entréeÉlémentAuxiliaire);}
void qsort(void*valeurArrièrePlan,size_t nombreÉlémentsÉlémentListe,size_t taille,int(*comparer)(const void*,const void*)){
    unsigned char*positionDonnées=valeurArrièrePlan;for(size_t indiceOrdinal=1;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)for(size_t ordinalInterne=indiceOrdinal;ordinalInterne&&comparer(positionDonnées+(ordinalInterne-1)*taille,positionDonnées+ordinalInterne*taille)>0;ordinalInterne--)for(size_t indiceTroisième=0;indiceTroisième<taille;indiceTroisième++){unsigned char codeCaractère=positionDonnées[(ordinalInterne-1)*taille+indiceTroisième];positionDonnées[(ordinalInterne-1)*taille+indiceTroisième]=positionDonnées[ordinalInterne*taille+indiceTroisième];positionDonnées[ordinalInterne*taille+indiceTroisième]=codeCaractère;}
}
static struct {int capacitéUtilisé,indiceRechercher;size_t position;} ouvert[24];
static unsigned char sortie[32768];static size_t tailleSortie,positionSortie;static int ouvrirSortie;
const unsigned char *sortieC(size_t *nombreÉlémentsÉlémentListe){*nombreÉlémentsÉlémentListe=tailleSortie;return sortie;}
int open(const char*nom,int bitsConfiguration,...){
    if(!strcmp(nom,"/@cc-output")){if(ouvrirSortie){erreur=16;return -1;}ouvrirSortie=1;tailleSortie=positionSortie=0;return 100;}
    for(unsigned indiceOrdinal=0;indiceOrdinal<sizeof(ressourcesCompilateur)/sizeof(ressourcesCompilateur[0]);indiceOrdinal++)if(!strcmp(nom,ressourcesCompilateur[indiceOrdinal].nom)){
        if(bitsConfiguration&3){erreur=30;return -1;}for(int ordinalInterne=0;ordinalInterne<24;ordinalInterne++)if(!ouvert[ordinalInterne].capacitéUtilisé){ouvert[ordinalInterne].capacitéUtilisé=1;ouvert[ordinalInterne].indiceRechercher=indiceOrdinal;ouvert[ordinalInterne].position=0;return 128+ordinalInterne;}erreur=24;return -1;
    }
    intptr_t valeurRetourné=invoquerUtilisateur(3,(uintptr_t)nom,bitsConfiguration,0,0,0,0);if(valeurRetourné<0){erreur=-valeurRetourné;return -1;}return valeurRetourné;
}
int close(int poignéeFichier){if(poignéeFichier==100){ouvrirSortie=0;return 0;}if(poignéeFichier>=128&&poignéeFichier<152){ouvert[poignéeFichier-128].capacitéUtilisé=0;return 0;}intptr_t valeurRetourné=invoquerUtilisateur(4,poignéeFichier,0,0,0,0,0);if(valeurRetourné<0){erreur=-valeurRetourné;return -1;}return 0;}
long read(int poignéeFichier,void*Données,size_t nombreÉlémentsÉlémentListe){
    if(poignéeFichier>=128&&poignéeFichier<152&&ouvert[poignéeFichier-128].capacitéUtilisé){int indiceOrdinal=poignéeFichier-128;const ressourceCompilateur*valeurRetourné=&ressourcesCompilateur[ouvert[indiceOrdinal].indiceRechercher];size_t côtéGauche=valeurRetourné->taille-ouvert[indiceOrdinal].position;if(nombreÉlémentsÉlémentListe>côtéGauche)nombreÉlémentsÉlémentListe=côtéGauche;memcpy(Données,valeurRetourné->Données+ouvert[indiceOrdinal].position,nombreÉlémentsÉlémentListe);ouvert[indiceOrdinal].position+=nombreÉlémentsÉlémentListe;return nombreÉlémentsÉlémentListe;}
    intptr_t valeurRetourné=invoquerUtilisateur(2,poignéeFichier,(uintptr_t)Données,nombreÉlémentsÉlémentListe,0,0,0);if(valeurRetourné<0){erreur=-valeurRetourné;return -1;}return valeurRetourné;
}
long write(int poignéeFichier,const void*Données,size_t nombreÉlémentsÉlémentListe){
    if(poignéeFichier==100){if(nombreÉlémentsÉlémentListe>sizeof(sortie)-positionSortie){erreur=28;return -1;}memcpy(sortie+positionSortie,Données,nombreÉlémentsÉlémentListe);positionSortie+=nombreÉlémentsÉlémentListe;if(tailleSortie<positionSortie)tailleSortie=positionSortie;return nombreÉlémentsÉlémentListe;}
    intptr_t valeurRetourné=invoquerUtilisateur(1,poignéeFichier,(uintptr_t)Données,nombreÉlémentsÉlémentListe,0,0,0);if(valeurRetourné<0){erreur=-valeurRetourné;return -1;}return valeurRetourné;
}
long lseek(int poignéeFichier,long valeurDécalage,int positionnerOrigine){
    if(poignéeFichier==100){long positionDonnées=valeurDécalage+(positionnerOrigine==0?0:positionnerOrigine==1?positionSortie:tailleSortie);if(positionDonnées<0||(size_t)positionDonnées>sizeof(sortie)){erreur=22;return -1;}positionSortie=positionDonnées;return positionDonnées;}
    if(poignéeFichier>=128&&poignéeFichier<152&&ouvert[poignéeFichier-128].capacitéUtilisé){int indiceOrdinal=poignéeFichier-128;long positionDonnées=valeurDécalage+(positionnerOrigine==0?0:positionnerOrigine==1?ouvert[indiceOrdinal].position:ressourcesCompilateur[ouvert[indiceOrdinal].indiceRechercher].taille);if(positionDonnées<0||(size_t)positionDonnées>ressourcesCompilateur[ouvert[indiceOrdinal].indiceRechercher].taille){erreur=22;return -1;}ouvert[indiceOrdinal].position=positionDonnées;return positionDonnées;}
    intptr_t valeurRetourné=invoquerUtilisateur(5,poignéeFichier,valeurDécalage,positionnerOrigine,0,0,0);if(valeurRetourné<0){erreur=-valeurRetourné;return -1;}return valeurRetourné;
}
int unlink(const char*nom){intptr_t valeurRetourné=invoquerUtilisateur(11,(uintptr_t)nom,0,0,0,0,0);if(valeurRetourné<0){erreur=-valeurRetourné;return -1;}return valeurRetourné;}
char *realpath(const char*nom,char*donnéesRésultat){if(!donnéesRésultat){donnéesRésultat=malloc(strlen(nom)+1);if(!donnéesRésultat)return 0;}return strcpy(donnéesRésultat,nom);}
char *getcwd(char*positionDonnées,size_t nombreÉlémentsÉlémentListe){if(nombreÉlémentsÉlémentListe<2){erreur=34;return 0;}positionDonnées[0]='/';positionDonnées[1]=0;return positionDonnées;}
char *strerror(int entréeÉlémentAuxiliaire){(void)entréeÉlémentAuxiliaire;return "native compiler I/O error";}
time_t time(time_t*entréeÉlémentTerminal){time_t donnéesTemporaire=0;if(entréeÉlémentTerminal)*entréeÉlémentTerminal=donnéesTemporaire;return donnéesTemporaire;}
struct tm *localtime(const time_t*entréeÉlémentTerminal){(void)entréeÉlémentTerminal;static struct tm donnéesTemporaire={.tm_year=126,.tm_mon=0,.tm_mday=1};return &donnéesTemporaire;}
static FILE fluxListe[18]={{1,0,1},{2,0,1}};FILE*stdout=&fluxListe[0],*stderr=&fluxListe[1];
FILE*fdopen(int poignéeFichier,const char*modeMéthode){(void)modeMéthode;for(unsigned indiceOrdinal=2;indiceOrdinal<18;indiceOrdinal++)if(!fluxListe[indiceOrdinal].capacitéUtilisé){fluxListe[indiceOrdinal].capacitéUtilisé=1;fluxListe[indiceOrdinal].erreur=0;fluxListe[indiceOrdinal].poignéeFichier=poignéeFichier;return &fluxListe[indiceOrdinal];}erreur=24;return 0;}
int fflush(FILE*entréeÉlémentFichier){return entréeÉlémentFichier&&entréeÉlémentFichier->erreur?-1:0;}
int fclose(FILE*entréeÉlémentFichier){int valeurRetourné=close(entréeÉlémentFichier->poignéeFichier);if(entréeÉlémentFichier->erreur)valeurRetourné=-1;entréeÉlémentFichier->capacitéUtilisé=0;return valeurRetourné;}
size_t fwrite(const void*positionDonnées,size_t donnéesChaîne,size_t nombreÉlémentsÉlémentListe,FILE*entréeÉlémentFichier){if(!donnéesChaîne)return 0;if(nombreÉlémentsÉlémentListe>SIZE_MAX/donnéesChaîne){entréeÉlémentFichier->erreur=1;return 0;}long valeurRetourné=write(entréeÉlémentFichier->poignéeFichier,positionDonnées,donnéesChaîne*nombreÉlémentsÉlémentListe);if(valeurRetourné<0){entréeÉlémentFichier->erreur=1;return 0;}return (size_t)valeurRetourné/donnéesChaîne;}
int fputc(int codeCaractère,FILE*entréeÉlémentFichier){unsigned char valeurDeuxième=codeCaractère;return fwrite(&valeurDeuxième,1,1,entréeÉlémentFichier)==1?valeurDeuxième:EOF;}
int fputs(const char*donnéesChaîne,FILE*entréeÉlémentFichier){return fwrite(donnéesChaîne,1,strlen(donnéesChaîne),entréeÉlémentFichier)==strlen(donnéesChaîne)?0:EOF;}
static void placerValeur(char*donnéesRésultat,size_t maximalCapacité,size_t*positionActuel,char codeCaractère){if(*positionActuel+1<maximalCapacité)donnéesRésultat[*positionActuel]=codeCaractère;(*positionActuel)++;}
int vsnprintf(char*donnéesRésultat,size_t maximalCapacité,const char*format,va_list argumentsArgumentsVariables){
    size_t positionActuel=0;while(*format){if(*format!='%'){placerValeur(donnéesRésultat,maximalCapacité,&positionActuel,*format++);continue;}format++;
        int côtéGauche=0,valeurZéro=0,valeurRepli=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')côtéGauche=1;if(*format=='0')valeurZéro=1;if(*format=='#')valeurRepli=1;format++;}
        int valeurLargeur=0,valeurPrécision=-1;if(*format=='*'){valeurLargeur=va_arg(argumentsArgumentsVariables,int);format++;}else while(*format>='0'&&*format<='9')valeurLargeur=valeurLargeur*10+*format++-'0';
        if(*format=='.'){format++;valeurPrécision=0;if(*format=='*'){valeurPrécision=va_arg(argumentsArgumentsVariables,int);format++;}else while(*format>='0'&&*format<='9')valeurPrécision=valeurPrécision*10+*format++-'0';}
        int caractèreLarge=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')caractèreLarge=1;format++;}
        char catégorieType=*format?*format++:0,stockageTampon[80];const char*donnéesChaîne=stockageTampon;size_t nombreÉlémentsÉlémentListe=0;
        if(catégorieType=='s'){donnéesChaîne=va_arg(argumentsArgumentsVariables,const char*);if(!donnéesChaîne)donnéesChaîne="(null)";nombreÉlémentsÉlémentListe=strlen(donnéesChaîne);if(valeurPrécision>=0&&nombreÉlémentsÉlémentListe>(size_t)valeurPrécision)nombreÉlémentsÉlémentListe=valeurPrécision;}
        else if(catégorieType=='c'){stockageTampon[0]=va_arg(argumentsArgumentsVariables,int);nombreÉlémentsÉlémentListe=1;}
        else if(catégorieType=='%'){stockageTampon[0]='%';nombreÉlémentsÉlémentListe=1;}
        else if(catégorieType=='d'||catégorieType=='i'||catégorieType=='u'||catégorieType=='x'||catégorieType=='X'||catégorieType=='o'||catégorieType=='p'){
            unsigned long long valeur;int négatif=0;
            if(catégorieType=='d'||catégorieType=='i'){long long donnéesTemporaire=caractèreLarge?va_arg(argumentsArgumentsVariables,long long):va_arg(argumentsArgumentsVariables,int);négatif=donnéesTemporaire<0;valeur=négatif?0-(unsigned long long)donnéesTemporaire:donnéesTemporaire;}
            else valeur=catégorieType=='p'?(uintptr_t)va_arg(argumentsArgumentsVariables,void*):caractèreLarge?va_arg(argumentsArgumentsVariables,unsigned long long):va_arg(argumentsArgumentsVariables,unsigned);
            unsigned valeurArrièrePlan=catégorieType=='x'||catégorieType=='X'||catégorieType=='p'?16:catégorieType=='o'?8:10;char nombreÉlémentsChiffre[64];unsigned capacitéUtilisé=0;
            do{nombreÉlémentsChiffre[capacitéUtilisé++]="0123456789abcdef"[valeur%valeurArrièrePlan];valeur/=valeurArrièrePlan;}while(valeur);
            if(négatif)stockageTampon[nombreÉlémentsÉlémentListe++]='-';if(catégorieType=='p'||(valeurRepli&&valeurArrièrePlan==16)){stockageTampon[nombreÉlémentsÉlémentListe++]='0';stockageTampon[nombreÉlémentsÉlémentListe++]='x';}
            for(int remplirValeur=(int)capacitéUtilisé;valeurPrécision>remplirValeur&&nombreÉlémentsÉlémentListe<sizeof(stockageTampon)-capacitéUtilisé;remplirValeur++)stockageTampon[nombreÉlémentsÉlémentListe++]='0';
            if(valeurZéro&&!côtéGauche&&valeurPrécision<0)while(valeurLargeur>(int)(nombreÉlémentsÉlémentListe+capacitéUtilisé)&&nombreÉlémentsÉlémentListe<sizeof(stockageTampon)-capacitéUtilisé)stockageTampon[nombreÉlémentsÉlémentListe++]='0';
            while(capacitéUtilisé)stockageTampon[nombreÉlémentsÉlémentListe++]=nombreÉlémentsChiffre[--capacitéUtilisé];
        }else{stockageTampon[0]='?';nombreÉlémentsÉlémentListe=1;}
        if(valeurLargeur>4096)valeurLargeur=4096;while(!côtéGauche&&valeurLargeur>(int)nombreÉlémentsÉlémentListe){placerValeur(donnéesRésultat,maximalCapacité,&positionActuel,' ');valeurLargeur--;}
        for(size_t indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)placerValeur(donnéesRésultat,maximalCapacité,&positionActuel,donnéesChaîne[indiceOrdinal]);while(côtéGauche&&valeurLargeur>(int)nombreÉlémentsÉlémentListe){placerValeur(donnéesRésultat,maximalCapacité,&positionActuel,' ');valeurLargeur--;}
    }if(maximalCapacité)donnéesRésultat[positionActuel<maximalCapacité?positionActuel:maximalCapacité-1]=0;return positionActuel;
}
int snprintf(char*donnéesRésultat,size_t maximalCapacité,const char*entréeÉlémentFichier,...){va_list valeurPremier;va_start(valeurPremier,entréeÉlémentFichier);int valeurRetourné=vsnprintf(donnéesRésultat,maximalCapacité,entréeÉlémentFichier,valeurPremier);va_end(valeurPremier);return valeurRetourné;}
int sprintf(char*donnéesRésultat,const char*entréeÉlémentFichier,...){va_list valeurPremier;va_start(valeurPremier,entréeÉlémentFichier);int valeurRetourné=vsnprintf(donnéesRésultat,SIZE_MAX,entréeÉlémentFichier,valeurPremier);va_end(valeurPremier);return valeurRetourné;}
int vfprintf(FILE*valeurFlux,const char*entréeÉlémentFichier,va_list valeurPremier){char valeurDeuxième[2048];int nombreÉlémentsÉlémentListe=vsnprintf(valeurDeuxième,sizeof(valeurDeuxième),entréeÉlémentFichier,valeurPremier);if(nombreÉlémentsÉlémentListe>2047)nombreÉlémentsÉlémentListe=2047;return fwrite(valeurDeuxième,1,nombreÉlémentsÉlémentListe,valeurFlux)==(size_t)nombreÉlémentsÉlémentListe?nombreÉlémentsÉlémentListe:-1;}
int fprintf(FILE*valeurFlux,const char*entréeÉlémentFichier,...){va_list valeurPremier;va_start(valeurPremier,entréeÉlémentFichier);int valeurRetourné=vfprintf(valeurFlux,entréeÉlémentFichier,valeurPremier);va_end(valeurPremier);return valeurRetourné;}
int printf(const char*entréeÉlémentFichier,...){va_list valeurPremier;va_start(valeurPremier,entréeÉlémentFichier);int valeurRetourné=vfprintf(stdout,entréeÉlémentFichier,valeurPremier);va_end(valeurPremier);return valeurRetourné;}

#include "../nommage/nomsLierMachine.h"
#include "invoquer.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *sortieC(size_t *);
extern const char *sourceCompilationJavaAnticipée(const char *);
typedef struct { unsigned char valeurIdentificateur[16];uint16_t catégorieType,typeMachine;uint32_t numéroVersion;uint64_t pointEntréeÉlément,décalageEntêteProgramme,décalageEntêteSection;uint32_t bitsConfiguration;uint16_t taille,tailleEntêteProgramme,nombreÉlémentsEntêteProgramme,tailleEntêteSection,nombreÉlémentsEntêteSection,tableNomSection; } valeurEntête;
typedef struct {uint32_t catégorieType,bitsConfiguration;uint64_t valeurDécalage,adresse,adressePhysique,tailleZoneFichier,tailleZoneMémoire,frontièreAligner;} valeurSegment;
static unsigned char image[16384];
static int entréeÉlémentPublier(const char *nom){
    size_t nombreÉlémentsÉlémentListe;const unsigned char*donnéesOriginal=sortieC(&nombreÉlémentsÉlémentListe);if(nombreÉlémentsÉlémentListe<sizeof(valeurEntête))return -1;
    valeurEntête entêteCodeExécutable;memcpy(&entêteCodeExécutable,donnéesOriginal,sizeof(entêteCodeExécutable));
    if(entêteCodeExécutable.catégorieType!=2||entêteCodeExécutable.typeMachine!=183||entêteCodeExécutable.tailleEntêteProgramme!=sizeof(valeurSegment)||!entêteCodeExécutable.nombreÉlémentsEntêteProgramme||entêteCodeExécutable.nombreÉlémentsEntêteProgramme>16||entêteCodeExécutable.décalageEntêteProgramme>nombreÉlémentsÉlémentListe||entêteCodeExécutable.nombreÉlémentsEntêteProgramme*sizeof(valeurSegment)>nombreÉlémentsÉlémentListe-entêteCodeExécutable.décalageEntêteProgramme)return -1;
    entêteCodeExécutable.décalageEntêteProgramme=sizeof(entêteCodeExécutable);entêteCodeExécutable.décalageEntêteSection=entêteCodeExécutable.nombreÉlémentsEntêteSection=entêteCodeExécutable.tailleEntêteSection=entêteCodeExécutable.tableNomSection=0;memcpy(image,&entêteCodeExécutable,sizeof(entêteCodeExécutable));
    size_t informationAuxiliaire=sizeof(entêteCodeExécutable)+entêteCodeExécutable.nombreÉlémentsEntêteProgramme*sizeof(valeurSegment),élémentListeSuivant=4096;unsigned char listePage[3072]={0};int pointEntréeÉlémentValide=0;
    for(unsigned indiceOrdinal=0;indiceOrdinal<entêteCodeExécutable.nombreÉlémentsEntêteProgramme;indiceOrdinal++){
        valeurSegment positionDonnées;valeurEntête original;memcpy(&original,donnéesOriginal,sizeof(original));memcpy(&positionDonnées,donnéesOriginal+original.décalageEntêteProgramme+indiceOrdinal*sizeof(positionDonnées),sizeof(positionDonnées));
        if(positionDonnées.valeurDécalage>nombreÉlémentsÉlémentListe||positionDonnées.tailleZoneFichier>nombreÉlémentsÉlémentListe-positionDonnées.valeurDécalage||positionDonnées.tailleZoneFichier>positionDonnées.tailleZoneMémoire)return -1;
        if(positionDonnées.catégorieType==1){
            if((positionDonnées.bitsConfiguration&~7u)||!(positionDonnées.bitsConfiguration&4)||(positionDonnées.bitsConfiguration&3)==3||positionDonnées.adresse<0x02000000||positionDonnées.adresse>0x02c00000||positionDonnées.tailleZoneMémoire>0x02c00000-positionDonnées.adresse)return -1;
            if((positionDonnées.bitsConfiguration&1)&&entêteCodeExécutable.pointEntréeÉlément>=positionDonnées.adresse&&entêteCodeExécutable.pointEntréeÉlément-positionDonnées.adresse<positionDonnées.tailleZoneFichier&&!(entêteCodeExécutable.pointEntréeÉlément&3))pointEntréeÉlémentValide=1;
            size_t valeurPrécédent=positionDonnées.adresse&4095,valeursOctet=positionDonnées.tailleZoneFichier?valeurPrécédent+positionDonnées.tailleZoneFichier:0;
            if(élémentListeSuivant>sizeof(image)||valeursOctet>sizeof(image)-élémentListeSuivant){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(élémentListeSuivant+valeursOctet),(unsigned)sizeof(image));return -1;}
            if(valeursOctet)memcpy(image+élémentListeSuivant+valeurPrécédent,donnéesOriginal+positionDonnées.valeurDécalage,positionDonnées.tailleZoneFichier);
            positionDonnées.adresse-=valeurPrécédent;positionDonnées.adressePhysique=positionDonnées.adresse;positionDonnées.tailleZoneMémoire+=valeurPrécédent;positionDonnées.tailleZoneFichier=valeursOctet;positionDonnées.valeurDécalage=élémentListeSuivant;positionDonnées.frontièreAligner=4096;
            for(uint64_t valeurPage=positionDonnées.adresse;valeurPage<positionDonnées.adresse+positionDonnées.tailleZoneMémoire;valeurPage+=4096){unsigned indiceRechercher=(valeurPage-0x02000000)/4096;if(indiceRechercher>=sizeof(listePage)||listePage[indiceRechercher]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}listePage[indiceRechercher]=1;}
            élémentListeSuivant+=(valeursOctet+4095)&~(size_t)4095;
        }else if(positionDonnées.catégorieType==4){if(positionDonnées.tailleZoneFichier>4096-informationAuxiliaire)return -1;memcpy(image+informationAuxiliaire,donnéesOriginal+positionDonnées.valeurDécalage,positionDonnées.tailleZoneFichier);positionDonnées.valeurDécalage=informationAuxiliaire;informationAuxiliaire+=positionDonnées.tailleZoneFichier;}
        else if(positionDonnées.catégorieType!=0&&positionDonnées.catégorieType!=6&&positionDonnées.catégorieType!=0x6474e551)return -1;
        memcpy(image+entêteCodeExécutable.décalageEntêteProgramme+indiceOrdinal*sizeof(positionDonnées),&positionDonnées,sizeof(positionDonnées));
    }
    if(!pointEntréeÉlémentValide)return -1;
    intptr_t poignéeFichier=invoquerUtilisateur(3,(uintptr_t)nom,577,0600,0,0,0);if(poignéeFichier<0){printf("cc: cannot create output file, error %d\n",(int)poignéeFichier);return -1;}
    intptr_t écrit=invoquerUtilisateur(1,poignéeFichier,(uintptr_t)image,élémentListeSuivant,0,0,0);invoquerUtilisateur(4,poignéeFichier,0,0,0,0,0);return écrit==(intptr_t)élémentListeSuivant?0:-1;
}
int démarrerProgrammeUtilisateur(int modeMéthode){
    char entrée[256],entréeÉlémentSélectionné[256],sortie[256]="a.elf";
    int nombreÉlémentsArguments=invoquerUtilisateur(15,UINTPTR_MAX,0,0,0,0,0);
    if(nombreÉlémentsArguments!=1&&nombreÉlémentsArguments!=3){printf(modeMéthode?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(invoquerUtilisateur(15,0,(uintptr_t)entrée,sizeof(entrée),0,0,0)<0)return 2;
    if(nombreÉlémentsArguments==1&&(!strcmp(entrée,"--version")||!strcmp(entrée,"-version"))){printf(modeMéthode?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(nombreÉlémentsArguments==3){invoquerUtilisateur(15,1,(uintptr_t)entréeÉlémentSélectionné,sizeof(entréeÉlémentSélectionné),0,0,0);if(strcmp(entréeÉlémentSélectionné,"-o")||invoquerUtilisateur(15,2,(uintptr_t)sortie,sizeof(sortie),0,0,0)<0)return 2;}
    if(!strcmp(entrée,sortie)){printf("cc: input and output must differ\n");return 2;}
    TCCState*donnéesChaîne=tcc_new();if(!donnéesChaîne)return 1;
    tcc_undefine_symbol(donnéesChaîne,"__linux__");tcc_undefine_symbol(donnéesChaîne,"__linux");tcc_undefine_symbol(donnéesChaîne,"linux");
    tcc_undefine_symbol(donnéesChaîne,"__unix__");tcc_undefine_symbol(donnéesChaîne,"__unix");tcc_undefine_symbol(donnéesChaîne,"unix");
    tcc_undefine_symbol(donnéesChaîne,"__STDC_HOSTED__");tcc_define_symbol(donnéesChaîne,"__STDC_HOSTED__","0");tcc_define_symbol(donnéesChaîne,"__JKOROS__","1");
    tcc_set_options(donnéesChaîne,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(donnéesChaîne,"/sdk/include");
    int valeurRetourné=tcc_set_output_type(donnéesChaîne,TCC_OUTPUT_EXE);
    if(!valeurRetourné){if(modeMéthode){const char*donnéesOriginal=sourceCompilationJavaAnticipée(entrée);valeurRetourné=donnéesOriginal?tcc_compile_string(donnéesChaîne,donnéesOriginal):-1;}else valeurRetourné=tcc_add_file(donnéesChaîne,entrée);}
    if(!valeurRetourné)valeurRetourné=tcc_add_file(donnéesChaîne,"/sdk/lib/start.o");
    if(!valeurRetourné)valeurRetourné=tcc_add_file(donnéesChaîne,"/sdk/lib/crt.o");
    if(!valeurRetourné&&modeMéthode)valeurRetourné=tcc_add_file(donnéesChaîne,"/sdk/lib/aot-runtime.o");
    if(!valeurRetourné)valeurRetourné=tcc_add_file(donnéesChaîne,"/sdk/lib/libposix-kor-user.a");
    if(!valeurRetourné)valeurRetourné=tcc_output_file(donnéesChaîne,"/@cc-output");
    if(!valeurRetourné)valeurRetourné=entréeÉlémentPublier(sortie);
    tcc_delete(donnéesChaîne);
    if(valeurRetourné){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(modeMéthode?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",sortie);return 0;
}

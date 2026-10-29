#include "valeurDistant.h"
#include <string.h>
#include "tableClavierDéfinirDeux.h"
static unsigned valeurContrôle,toucheDécaler,texteHangul;
typedef struct {unsigned élémentListePremier,milieu,terminaison;} étatValeurComposition;
static étatValeurComposition Combinaison,enregistrementJournal[16];
static unsigned nombreÉlémentsJournal;
void toucheDistantConfirmer(void){memset(&Combinaison,0,sizeof(Combinaison));nombreÉlémentsJournal=0;}
void initialiserTraitToucheDistant(void){valeurContrôle=toucheDécaler=texteHangul=0;toucheDistantConfirmer();}
static void placerTexte(unsigned valeur){
    unsigned char texte[4];unsigned nombre;
    if(valeur<128){texte[0]=valeur;nombre=1;}else if(valeur<2048){texte[0]=0xc0|(valeur>>6);texte[1]=0x80|(valeur&63);nombre=2;}
    else if(valeur<65536){texte[0]=0xe0|(valeur>>12);texte[1]=0x80|((valeur>>6)&63);texte[2]=0x80|(valeur&63);nombre=3;}
    else{texte[0]=0xf0|(valeur>>18);texte[1]=0x80|((valeur>>12)&63);texte[2]=0x80|((valeur>>6)&63);texte[3]=0x80|(valeur&63);nombre=4;}
    entréeDistantAlimenter(texte,nombre);
}
static int trouverEntréeÉlément(const unsigned *listeEntréeÉlément,unsigned nombre,unsigned valeur){for(unsigned indiceOrdinal=0;indiceOrdinal<nombre;indiceOrdinal++)if(listeEntréeÉlément[indiceOrdinal]==valeur)return indiceOrdinal;return -1;}
static unsigned trouverDuplicata(const unsigned Table[][3],unsigned nombre,unsigned opérandePremier,unsigned opérandeDeuxième){for(unsigned indiceOrdinal=0;indiceOrdinal<nombre;indiceOrdinal++)if(Table[indiceOrdinal][0]==opérandePremier&&Table[indiceOrdinal][1]==opérandeDeuxième)return Table[indiceOrdinal][2];return 0;}
static unsigned texteComposé(void){
    if(Combinaison.élémentListePremier&&Combinaison.milieu)return 0xac00+(trouverEntréeÉlément(tableLettreHangulInitialValeur,19,Combinaison.élémentListePremier)*21+trouverEntréeÉlément(tableLettreHangulVoyelleMédiane,21,Combinaison.milieu))*28+(Combinaison.terminaison?trouverEntréeÉlément(tableLettreHangulFinal,28,Combinaison.terminaison):0);
    return Combinaison.élémentListePremier?Combinaison.élémentListePremier:Combinaison.milieu;
}
static int hangulAlimenter(unsigned traitTouche){
    unsigned valeurLettreHangul=0;for(unsigned indiceOrdinal=0;indiceOrdinal<sizeof(dispositionTouche)/sizeof(dispositionTouche[0]);indiceOrdinal++)if(dispositionTouche[indiceOrdinal][0]==traitTouche)valeurLettreHangul=dispositionTouche[indiceOrdinal][1];
    if(!valeurLettreHangul&&traitTouche>='A'&&traitTouche<='Z')return hangulAlimenter(traitTouche+32);if(!valeurLettreHangul)return 0;
    unsigned élémentListePrécédentÉlément=texteComposé(),valeurConfirmer=0;étatValeurComposition valeurAvant=Combinaison;
    if(nombreÉlémentsJournal<16)enregistrementJournal[nombreÉlémentsJournal++]=valeurAvant;
    if(trouverEntréeÉlément(tableLettreHangulInitialValeur,19,valeurLettreHangul)>=0){
        if(Combinaison.élémentListePremier&&Combinaison.milieu&&!Combinaison.terminaison&&trouverEntréeÉlément(tableLettreHangulFinal,28,valeurLettreHangul)>=0)Combinaison.terminaison=valeurLettreHangul;
        else{unsigned valeurSuperposer=trouverDuplicata(lettreHangulFinalComposéMot,11,Combinaison.terminaison,valeurLettreHangul);if(Combinaison.terminaison&&valeurSuperposer)Combinaison.terminaison=valeurSuperposer;
            else{valeurConfirmer=élémentListePrécédentÉlément;toucheDistantConfirmer();Combinaison.élémentListePremier=valeurLettreHangul;nombreÉlémentsJournal=1;memset(enregistrementJournal,0,sizeof(étatValeurComposition));}}
    }else if(Combinaison.terminaison){
        unsigned côtéGauche=0,droit=Combinaison.terminaison;for(unsigned indiceOrdinal=0;indiceOrdinal<11;indiceOrdinal++)if(lettreHangulFinalComposéMot[indiceOrdinal][2]==Combinaison.terminaison){côtéGauche=lettreHangulFinalComposéMot[indiceOrdinal][0];droit=lettreHangulFinalComposéMot[indiceOrdinal][1];break;}
        Combinaison.terminaison=côtéGauche;valeurConfirmer=texteComposé();toucheDistantConfirmer();Combinaison.élémentListePremier=droit;Combinaison.milieu=valeurLettreHangul;nombreÉlémentsJournal=2;
        memset(enregistrementJournal,0,2*sizeof(étatValeurComposition));enregistrementJournal[1].élémentListePremier=droit;
    }else if(Combinaison.milieu){unsigned valeurSuperposer=trouverDuplicata(lettreHangulVoyelleMédianeComposéMot,7,Combinaison.milieu,valeurLettreHangul);
        if(valeurSuperposer)Combinaison.milieu=valeurSuperposer;else{valeurConfirmer=élémentListePrécédentÉlément;toucheDistantConfirmer();Combinaison.milieu=valeurLettreHangul;nombreÉlémentsJournal=1;memset(enregistrementJournal,0,sizeof(étatValeurComposition));}
    }else Combinaison.milieu=valeurLettreHangul;
    if(élémentListePrécédentÉlément)placerTexte(127);if(valeurConfirmer)placerTexte(valeurConfirmer);unsigned valeurMaintenant=texteComposé();if(valeurMaintenant)placerTexte(valeurMaintenant);return 1;
}
void traitToucheDistant(unsigned symbole,int valeurEnfoncer){
    if(symbole==0xffe3||symbole==0xffe4){valeurContrôle=valeurEnfoncer;return;}
    if(symbole==0xffe1||symbole==0xffe2){toucheDécaler=valeurEnfoncer;return;}
    if(!valeurEnfoncer)return;
    if(symbole==0xffc6||symbole==0xff31||(symbole==32&&toucheDécaler&&!valeurContrôle)){
        toucheDistantConfirmer();texteHangul=!texteHangul;unsigned char évènement[]={30,3,texteHangul,0,0,0,0};entréeDistantAlimenter(évènement,7);return;
    }
    if(symbole==0xff08&&texteHangul&&!valeurContrôle&&nombreÉlémentsJournal){Combinaison=enregistrementJournal[--nombreÉlémentsJournal];placerTexte(127);unsigned texte=texteComposé();if(texte)placerTexte(texte);return;}
    if(texteHangul&&!valeurContrôle&&symbole<128&&hangulAlimenter(symbole))return;
    toucheDistantConfirmer();
    if((valeurContrôle&&toucheDécaler&&(symbole=='t'||symbole=='T'))||symbole==0xffc3||symbole==0xffc9){unsigned char évènement[]={30,2,symbole==0xffc3?2:symbole==0xffc9?3:1,0,0,0,0};entréeDistantAlimenter(évènement,7);return;}
    const char *valeurSpécial=symbole==0xff08?"\177":symbole==0xff09?"\t":symbole==0xff0d?"\r":symbole==0xff1b?"\033":
        symbole==0xffff?"\033[3~":symbole==0xff50?"\033[H":symbole==0xff57?"\033[F":symbole==0xff51?"\033[D":
        symbole==0xff52?"\033[A":symbole==0xff53?"\033[C":symbole==0xff54?"\033[B":symbole==0xff55?"\033[5~":symbole==0xff56?"\033[6~":0;
    if(valeurSpécial){entréeDistantAlimenter((const unsigned char*)valeurSpécial,strlen(valeurSpécial));return;}
    unsigned valeur=(symbole&0xff000000)==0x01000000?symbole&0xffffff:symbole;
    if(valeur>0x10ffff||(valeur>=0xd800&&valeur<=0xdfff)||(symbole>=0xff00&&symbole<0x1000000))return;
    if(valeurContrôle){if(valeur>='a'&&valeur<='z')valeur-=96;else if(valeur>='A'&&valeur<='Z')valeur-=64;}
    placerTexte(valeur);
}

#include "../nommage/nomsLierMachine.h"
#include "informationÉcran.h"
/* interne 네 fenêtre 합성과 UTF-8 terminal. 바뀐 영역의 valeurAchevé 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t motMachine;
extern motMachine pixelCarteMatérielle(motMachine,motMachine,motMachine),tamponImageCarteMatérielle(void);
extern void *memset(void *,int,size_t);
extern const unsigned char policeTerminal[];
#define colonnesMaximal 237
#define nombreÉlémentsLigneHistorique 160
typedef struct {
    uint32_t cellulesCaractère[nombreÉlémentsLigneHistorique][colonnesMaximal]; uint8_t listeFormes[nombreÉlémentsLigneHistorique][colonnesMaximal];
    unsigned valeurLargeur,valeurHauteur,colonnes,nombreÉlémentsRangée,redimensionnéÉtait;
    unsigned estEnVie,coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,positionRangée,positionColonne,entréeÉlémentSommet,défiler,couleurPremierPlan,couleurArrièrePlan,échapper,valeurParamètre[4],indiceParamètre,rangéeEnregistré,numéroColonneEnregistré;
    unsigned résultatNonSigné,valeurLongNonSigné,valeurPetitFormat,alternatif,visiblePointInsertion;
} Terminal;
static Terminal listeFenêtres[4];
static int focus=-1,sortie,valeurOrdre[4],nombreÉlémentsEntréeÉlément,valeurGlisser=-1,coordonnéeHorizontaleGlisser,coordonnéeVerticaleGlisser;
static unsigned estEnAttente,boutons,vueBureau,entréeHangul;
static const uint32_t couleursPixel[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int visibleÉcran(int),pointeurÉcran(int,unsigned,int,int);
extern void écranRedessiner(int);
static Terminal *entréeÉlémentTerminal;
static unsigned caractèreLarge(unsigned codeCaractère){return codeCaractère>=256?2:1;}
static void régionRectangulaire(unsigned coordonnéeCoordonnéeHorizontale,unsigned coordonnéeCoordonnéeVerticale,unsigned valeurLargeurDemandé,unsigned valeurHauteurDemandé,unsigned couleurPixel){
    remplirRectangleCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,valeurLargeurDemandé,valeurHauteurDemandé,couleurPixel);
}
void glypheTerminal(unsigned coordonnéeCoordonnéeHorizontale,unsigned coordonnéeCoordonnéeVerticale,unsigned codeCaractère,unsigned couleurPremierPlan,unsigned couleurArrièrePlan){
    unsigned valeurLargeur=caractèreLarge(codeCaractère)*8;if(codeCaractère==0xffffffffu)return;
    int côtéGauche=coordonnéeCoordonnéeHorizontale,côtéSupérieur=coordonnéeCoordonnéeVerticale,étendueLargeur=valeurLargeur,longueur=16;
    if(!bornesDessinCarteMatérielle(&côtéGauche,&côtéSupérieur,&étendueLargeur,&longueur))return;
    if(codeCaractère==' '){remplirRectangleCarteMatérielle(côtéGauche,côtéSupérieur,étendueLargeur,longueur,couleurArrièrePlan);return;}
    unsigned indiceRechercher=codeCaractère<65536?codeCaractère:codeCaractère>=0x1f600&&codeCaractère<0x1f650?65536+codeCaractère-0x1f600:0xfffd;
    const unsigned char *valeurPolice=policeTerminal+indiceRechercher*32;
    for(int ligne=côtéSupérieur;ligne<côtéSupérieur+longueur;ligne++){unsigned listeBits=valeurPolice[(ligne-coordonnéeCoordonnéeVerticale)*2]*256+valeurPolice[(ligne-coordonnéeCoordonnéeVerticale)*2+1];for(int entréeÉlémentEmplacement=côtéGauche;entréeÉlémentEmplacement<côtéGauche+étendueLargeur;entréeÉlémentEmplacement++)pixelCarteMatérielle(entréeÉlémentEmplacement,ligne,(listeBits&(0x8000>>(entréeÉlémentEmplacement-coordonnéeCoordonnéeHorizontale)))?couleurPremierPlan:couleurArrièrePlan);}
}
static void tableNom(unsigned coordonnéeCoordonnéeHorizontale,unsigned coordonnéeCoordonnéeVerticale,const char *donnéesChaîne,unsigned couleurPremierPlan,unsigned couleurArrièrePlan){while(*donnéesChaîne){unsigned codeCaractère=(unsigned char)*donnéesChaîne++, nombreÉlémentsRestant=0;if(codeCaractère>=0xc0){nombreÉlémentsRestant=codeCaractère<0xe0?1:codeCaractère<0xf0?2:3;codeCaractère&=(1u<<(6-nombreÉlémentsRestant))-1;while(nombreÉlémentsRestant--&&*donnéesChaîne)codeCaractère=(codeCaractère<<6)|((unsigned char)*donnéesChaîne++&63);}glypheTerminal(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,codeCaractère,couleurPremierPlan,couleurArrièrePlan);coordonnéeCoordonnéeHorizontale+=caractèreLarge(codeCaractère)*8;}}
static unsigned entréeÉlémentPremier(void){return entréeÉlémentTerminal->entréeÉlémentSommet;}
static int estAffiché(void){return entréeÉlémentTerminal->estEnVie&&focus>=0&&entréeÉlémentTerminal==&listeFenêtres[focus]&&!visibleÉcran(focus);}
static void écranPeindre(unsigned positionRangée,unsigned positionColonne){
    if(!estAffiché()||positionRangée<entréeÉlémentPremier()-entréeÉlémentTerminal->défiler||positionRangée>=entréeÉlémentPremier()-entréeÉlémentTerminal->défiler+entréeÉlémentTerminal->nombreÉlémentsRangée||positionColonne>=entréeÉlémentTerminal->colonnes)return;
    unsigned codeCaractère=entréeÉlémentTerminal->cellulesCaractère[positionRangée%nombreÉlémentsLigneHistorique][positionColonne],donnéesChaîne=entréeÉlémentTerminal->listeFormes[positionRangée%nombreÉlémentsLigneHistorique][positionColonne];
    if(caractèreLarge(codeCaractère)==2&&positionColonne+1>=entréeÉlémentTerminal->colonnes)codeCaractère=' ';
    glypheTerminal(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12+positionColonne*8,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+36+(positionRangée-entréeÉlémentPremier()+entréeÉlémentTerminal->défiler)*16,codeCaractère?codeCaractère:' ',couleursPixel[donnéesChaîne&15],couleursPixel[donnéesChaîne>>4]);
}
static void valeurPointInsertion(int afficherFenêtre){if(!estAffiché()||entréeÉlémentTerminal->défiler||entréeÉlémentTerminal->positionColonne>=entréeÉlémentTerminal->colonnes||entréeÉlémentTerminal->positionRangée<entréeÉlémentTerminal->entréeÉlémentSommet||entréeÉlémentTerminal->positionRangée>=entréeÉlémentTerminal->entréeÉlémentSommet+entréeÉlémentTerminal->nombreÉlémentsRangée)return;
    if(!afficherFenêtre||!entréeÉlémentTerminal->visiblePointInsertion)écranPeindre(entréeÉlémentTerminal->positionRangée,entréeÉlémentTerminal->positionColonne);else régionRectangulaire(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12+entréeÉlémentTerminal->positionColonne*8,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+36+(entréeÉlémentTerminal->positionRangée-entréeÉlémentTerminal->entréeÉlémentSommet)*16+14,8,2,couleursPixel[entréeÉlémentTerminal->couleurPremierPlan]);}
static void valeurContenuValeur(void){
    régionRectangulaire(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+36,entréeÉlémentTerminal->colonnes*8,entréeÉlémentTerminal->nombreÉlémentsRangée*16,couleursPixel[0]);
    int positionHorizontal=entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12,positionVertical=entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+36,étendueLargeur=entréeÉlémentTerminal->colonnes*8,longueur=entréeÉlémentTerminal->nombreÉlémentsRangée*16;
    if(bornesDessinCarteMatérielle(&positionHorizontal,&positionVertical,&étendueLargeur,&longueur)){
    unsigned lignePremier=(positionVertical-entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale-36)/16,ligneDernier=(positionVertical+longueur-entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale-36+15)/16;
    unsigned emplacementPremier=(positionHorizontal-entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale-12)/8,emplacementDernier=(positionHorizontal+étendueLargeur-entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale-12+7)/8;
    if(emplacementPremier)emplacementPremier--; /* 잘림 valeurFrontière 왼쪽에서 시작한 두 entréeÉlémentEmplacement 글자도 그린다. */
    for(unsigned valeurRetourné=lignePremier;valeurRetourné<ligneDernier;valeurRetourné++)for(unsigned codeCaractère=emplacementPremier;codeCaractère<emplacementDernier;codeCaractère++){
        unsigned positionRangée=entréeÉlémentPremier()-entréeÉlémentTerminal->défiler+valeurRetourné,valeurCaractère=entréeÉlémentTerminal->cellulesCaractère[positionRangée%nombreÉlémentsLigneHistorique][codeCaractère],donnéesChaîne=entréeÉlémentTerminal->listeFormes[positionRangée%nombreÉlémentsLigneHistorique][codeCaractère];
        if(caractèreLarge(valeurCaractère)==2&&codeCaractère+1>=entréeÉlémentTerminal->colonnes)valeurCaractère=' ';
        if((valeurCaractère==0||valeurCaractère==' ')&&(donnéesChaîne>>4)==0)continue;
        glypheTerminal(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12+codeCaractère*8,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+36+valeurRetourné*16,valeurCaractère?valeurCaractère:' ',couleursPixel[donnéesChaîne&15],couleursPixel[donnéesChaîne>>4]);
    }}
    tableNom(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+entréeÉlémentTerminal->valeurHauteur-18,entréeÉlémentTerminal->défiler?"PgDn: recent output":entréeÉlémentTerminal->valeurLargeur>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);valeurPointInsertion(1);
}
static void cadreExécution(int valeurIdentificateur){
    entréeÉlémentTerminal=&listeFenêtres[valeurIdentificateur];
    int positionHorizontal=entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale,positionVertical=entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale,étendueLargeur=entréeÉlémentTerminal->valeurLargeur,longueur=entréeÉlémentTerminal->valeurHauteur;
    if(!bornesDessinCarteMatérielle(&positionHorizontal,&positionVertical,&étendueLargeur,&longueur))return;
    régionRectangulaire(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale,entréeÉlémentTerminal->valeurLargeur,entréeÉlémentTerminal->valeurHauteur,0x403127);
    unsigned couleurPixel=valeurIdentificateur==focus?0x905020:0x604438;régionRectangulaire(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale,entréeÉlémentTerminal->valeurLargeur,30,couleurPixel);
    tableNom(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+12,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+7,"JKOROS Terminal",0xffffff,couleurPixel);
    char valeurNumérique[2]={(char)('1'+valeurIdentificateur),0};tableNom(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+148,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+7,valeurNumérique,0xffffff,couleurPixel);
    tableNom(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+240,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+7,entréeÉlémentTerminal->valeurLargeur>=500?(entréeHangul?"[FR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(entréeHangul?"[FR]":"[EN]"),0xffffff,couleurPixel);
    régionRectangulaire(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+entréeÉlémentTerminal->valeurLargeur-32,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+4,26,22,0x5555b8);tableNom(entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale+entréeÉlémentTerminal->valeurLargeur-24,entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale+7,"X",0xffffff,0x5555b8);
    valeurContenuValeur();
}
static void dessinerScène(void){
    if(!vueBureau)return;régionRectangulaire(0,0,largeurÉcranCarteMatérielle(),hauteurÉcranCarteMatérielle(),0x302018);régionRectangulaire(0,0,largeurÉcranCarteMatérielle(),32,0x403127);
    régionRectangulaire(6,4,136,24,0x905020);tableNom(14,8,"+ New terminal",0xffffff,0x905020);
    for(int indiceOrdinal=0;indiceOrdinal<4;indiceOrdinal++)if(listeFenêtres[indiceOrdinal].estEnVie){unsigned codeCaractère=focus==indiceOrdinal?0x905020:0x604438;régionRectangulaire(154+indiceOrdinal*112,4,106,24,codeCaractère);tableNom(160+indiceOrdinal*112,8,"Terminal",0xffffff,codeCaractère);char donnéesChaîne[2]={(char)('1'+indiceOrdinal),0};tableNom(232+indiceOrdinal*112,8,donnéesChaîne,0xffffff,codeCaractère);}
    if(!nombreÉlémentsEntréeÉlément)tableNom(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsEntréeÉlément;indiceOrdinal++)cadreExécution(valeurOrdre[indiceOrdinal]);écranRedessiner(focus);entréeÉlémentTerminal=&listeFenêtres[sortie];
}
static void régionPeindre(int positionHorizontal,int positionVertical,int étendueLargeur,int longueur){
    if(!vueBureau||!bornesDessinCarteMatérielle(&positionHorizontal,&positionVertical,&étendueLargeur,&longueur))return;
    for(int ligne=positionVertical;ligne<positionVertical+longueur;ligne+=32){
        int hauteurBande=positionVertical+longueur-ligne;if(hauteurBande>32)hauteurBande=32;
        if(dessinDémarrerCarteMatérielle(positionHorizontal,ligne,étendueLargeur,hauteurBande)){dessinerScène();dessinTerminerCarteMatérielle();}
    }
}
static void redessiner(void){régionPeindre(0,0,largeurÉcranCarteMatérielle(),hauteurÉcranCarteMatérielle());}
/* 서로 겹치지 않는 새 fenêtre 영역과 élémentListePrécédentÉlément 자리의 네 띠를 복구한다. */
static void bornesFenêtrePeindre(int positionHorizontal,int positionVertical,int étendueLargeur,int longueur,Terminal *fenêtre){
    int côtéGauche=positionHorizontal>(int)fenêtre->coordonnéeCoordonnéeHorizontale?positionHorizontal:(int)fenêtre->coordonnéeCoordonnéeHorizontale;
    int côtéSupérieur=positionVertical>(int)fenêtre->coordonnéeCoordonnéeVerticale?positionVertical:(int)fenêtre->coordonnéeCoordonnéeVerticale;
    int droit=positionHorizontal+étendueLargeur<(int)(fenêtre->coordonnéeCoordonnéeHorizontale+fenêtre->valeurLargeur)?positionHorizontal+étendueLargeur:(int)(fenêtre->coordonnéeCoordonnéeHorizontale+fenêtre->valeurLargeur);
    int côtéInférieur=positionVertical+longueur<(int)(fenêtre->coordonnéeCoordonnéeVerticale+fenêtre->valeurHauteur)?positionVertical+longueur:(int)(fenêtre->coordonnéeCoordonnéeVerticale+fenêtre->valeurHauteur);
    régionPeindre(fenêtre->coordonnéeCoordonnéeHorizontale,fenêtre->coordonnéeCoordonnéeVerticale,fenêtre->valeurLargeur,fenêtre->valeurHauteur);
    if(côtéGauche>=droit||côtéSupérieur>=côtéInférieur){régionPeindre(positionHorizontal,positionVertical,étendueLargeur,longueur);return;}
    régionPeindre(positionHorizontal,positionVertical,étendueLargeur,côtéSupérieur-positionVertical);
    régionPeindre(positionHorizontal,côtéInférieur,étendueLargeur,positionVertical+longueur-côtéInférieur);
    régionPeindre(positionHorizontal,côtéSupérieur,côtéGauche-positionHorizontal,côtéInférieur-côtéSupérieur);
    régionPeindre(droit,côtéSupérieur,positionHorizontal+étendueLargeur-droit,côtéInférieur-côtéSupérieur);
}
static void focusSignal(void){estEnAttente=(estEnAttente&~15u)|(unsigned)(focus+1)|0x10000;}
void modeEntréeTerminal(unsigned coréen){
    entréeHangul=coréen!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(focus>=0){
        Terminal *entréeÉlémentFenêtre=&listeFenêtres[focus];
        tableNom(entréeÉlémentFenêtre->coordonnéeCoordonnéeHorizontale+240,entréeÉlémentFenêtre->coordonnéeCoordonnéeVerticale+7,entréeÉlémentFenêtre->valeurLargeur>=500?(entréeHangul?"[FR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(entréeHangul?"[FR]":"[EN]"),0xffffff,0x905020);
    }
}
static void avantCôtéVersApporter(int valeurIdentificateur){if(valeurIdentificateur<0||valeurIdentificateur>=4||!listeFenêtres[valeurIdentificateur].estEnVie)return;int positionActuel=0;while(positionActuel<nombreÉlémentsEntréeÉlément&&valeurOrdre[positionActuel]!=valeurIdentificateur)positionActuel++;for(;positionActuel+1<nombreÉlémentsEntréeÉlément;positionActuel++)valeurOrdre[positionActuel]=valeurOrdre[positionActuel+1];valeurOrdre[nombreÉlémentsEntréeÉlément-1]=valeurIdentificateur;focus=valeurIdentificateur;focusSignal();redessiner();}
static void blanc(unsigned positionRangée){for(unsigned codeCaractère=0;codeCaractère<colonnesMaximal;codeCaractère++){entréeÉlémentTerminal->cellulesCaractère[positionRangée%nombreÉlémentsLigneHistorique][codeCaractère]=0;entréeÉlémentTerminal->listeFormes[positionRangée%nombreÉlémentsLigneHistorique][codeCaractère]=entréeÉlémentTerminal->couleurPremierPlan|(entréeÉlémentTerminal->couleurArrièrePlan<<4);}}
static void effacerContenuContenu(void){entréeÉlémentTerminal->positionRangée=entréeÉlémentTerminal->positionColonne=entréeÉlémentTerminal->entréeÉlémentSommet=entréeÉlémentTerminal->défiler=0;for(unsigned valeurRetourné=0;valeurRetourné<nombreÉlémentsLigneHistorique;valeurRetourné++)blanc(valeurRetourné);if(estAffiché())valeurContenuValeur();}
static int créerEntréeÉlément(void){
    if(!tamponImageCarteMatérielle())return -19;int valeurIdentificateur=0;while(valeurIdentificateur<4&&listeFenêtres[valeurIdentificateur].estEnVie)valeurIdentificateur++;if(valeurIdentificateur==4)return -28;
    vueBureau=1;entréeÉlémentTerminal=&listeFenêtres[valeurIdentificateur];memset(entréeÉlémentTerminal,0,sizeof(*entréeÉlémentTerminal));entréeÉlémentTerminal->estEnVie=1;entréeÉlémentTerminal->valeurLargeur=568;entréeÉlémentTerminal->valeurHauteur=360;entréeÉlémentTerminal->colonnes=68;entréeÉlémentTerminal->nombreÉlémentsRangée=19;entréeÉlémentTerminal->coordonnéeCoordonnéeHorizontale=12+valeurIdentificateur*16;entréeÉlémentTerminal->coordonnéeCoordonnéeVerticale=48+valeurIdentificateur*18;entréeÉlémentTerminal->couleurPremierPlan=7;entréeÉlémentTerminal->visiblePointInsertion=1;
    for(unsigned valeurRetourné=0;valeurRetourné<nombreÉlémentsLigneHistorique;valeurRetourné++)blanc(valeurRetourné);valeurOrdre[nombreÉlémentsEntréeÉlément++]=valeurIdentificateur;focus=valeurIdentificateur;estEnAttente|=1u<<(4+valeurIdentificateur);focusSignal();redessiner();return valeurIdentificateur+1;
}
static void fermerFenêtre(int valeurIdentificateur){
    if(valeurIdentificateur<0||valeurIdentificateur>=4||!listeFenêtres[valeurIdentificateur].estEnVie)return;listeFenêtres[valeurIdentificateur].estEnVie=0;estEnAttente|=1u<<(8+valeurIdentificateur);
    int positionActuel=0;while(positionActuel<nombreÉlémentsEntréeÉlément&&valeurOrdre[positionActuel]!=valeurIdentificateur)positionActuel++;for(;positionActuel+1<nombreÉlémentsEntréeÉlément;positionActuel++)valeurOrdre[positionActuel]=valeurOrdre[positionActuel+1];nombreÉlémentsEntréeÉlément--;
    if(focus==valeurIdentificateur)focus=nombreÉlémentsEntréeÉlément?valeurOrdre[nombreÉlémentsEntréeÉlément-1]:-1;focusSignal();redessiner();
}
static void nouvelleLigne(void){entréeÉlémentTerminal->positionColonne=0;entréeÉlémentTerminal->positionRangée++;if(entréeÉlémentTerminal->positionRangée>=entréeÉlémentTerminal->entréeÉlémentSommet+entréeÉlémentTerminal->nombreÉlémentsRangée){entréeÉlémentTerminal->entréeÉlémentSommet++;blanc(entréeÉlémentTerminal->positionRangée);if(estAffiché())valeurContenuValeur();}}
static void pointCode(unsigned codeCaractère){
    if(codeCaractère==13){entréeÉlémentTerminal->positionColonne=0;return;}if(codeCaractère==10){nouvelleLigne();return;}if(codeCaractère==8){if(entréeÉlémentTerminal->positionColonne)entréeÉlémentTerminal->positionColonne--;return;}
    if(codeCaractère==9){unsigned nombreÉlémentsÉlémentListe=8-entréeÉlémentTerminal->positionColonne%8;while(nombreÉlémentsÉlémentListe--)pointCode(' ');return;}if(codeCaractère<32||codeCaractère==127)return;
    unsigned valeurLargeurDemandé=caractèreLarge(codeCaractère);if(entréeÉlémentTerminal->positionColonne+valeurLargeurDemandé>entréeÉlémentTerminal->colonnes)nouvelleLigne();
    if(entréeÉlémentTerminal->cellulesCaractère[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne]==0xffffffffu&&entréeÉlémentTerminal->positionColonne){entréeÉlémentTerminal->cellulesCaractère[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne-1]=' ';écranPeindre(entréeÉlémentTerminal->positionRangée,entréeÉlémentTerminal->positionColonne-1);}
    if(caractèreLarge(entréeÉlémentTerminal->cellulesCaractère[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne])==2&&entréeÉlémentTerminal->positionColonne+1<entréeÉlémentTerminal->colonnes){entréeÉlémentTerminal->cellulesCaractère[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne+1]=' ';écranPeindre(entréeÉlémentTerminal->positionRangée,entréeÉlémentTerminal->positionColonne+1);}
    entréeÉlémentTerminal->cellulesCaractère[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne]=codeCaractère;entréeÉlémentTerminal->listeFormes[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne]=entréeÉlémentTerminal->couleurPremierPlan|(entréeÉlémentTerminal->couleurArrièrePlan<<4);
    if(valeurLargeurDemandé==2)entréeÉlémentTerminal->cellulesCaractère[entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique][entréeÉlémentTerminal->positionColonne+1]=0xffffffffu;
    écranPeindre(entréeÉlémentTerminal->positionRangée,entréeÉlémentTerminal->positionColonne);entréeÉlémentTerminal->positionColonne+=valeurLargeurDemandé;
}
static void séquenceContrôlePoignée(unsigned codeCaractère){
    unsigned nombreÉlémentsÉlémentListe=entréeÉlémentTerminal->valeurParamètre[0]?entréeÉlémentTerminal->valeurParamètre[0]:1;
    if(codeCaractère=='m')for(unsigned indiceOrdinal=0;indiceOrdinal<=entréeÉlémentTerminal->indiceParamètre;indiceOrdinal++){unsigned positionDonnées=entréeÉlémentTerminal->valeurParamètre[indiceOrdinal];if(!positionDonnées){entréeÉlémentTerminal->couleurPremierPlan=7;entréeÉlémentTerminal->couleurArrièrePlan=0;}if(positionDonnées==1&&entréeÉlémentTerminal->couleurPremierPlan<8)entréeÉlémentTerminal->couleurPremierPlan+=8;if(positionDonnées==7){unsigned retenirValeur=entréeÉlémentTerminal->couleurPremierPlan;entréeÉlémentTerminal->couleurPremierPlan=entréeÉlémentTerminal->couleurArrièrePlan;entréeÉlémentTerminal->couleurArrièrePlan=retenirValeur;}if(positionDonnées>=30&&positionDonnées<=37)entréeÉlémentTerminal->couleurPremierPlan=positionDonnées-30;if(positionDonnées>=90&&positionDonnées<=97)entréeÉlémentTerminal->couleurPremierPlan=positionDonnées-90+8;if(positionDonnées>=40&&positionDonnées<=47)entréeÉlémentTerminal->couleurArrièrePlan=positionDonnées-40;if(positionDonnées>=100&&positionDonnées<=107)entréeÉlémentTerminal->couleurArrièrePlan=positionDonnées-100+8;if(positionDonnées==39)entréeÉlémentTerminal->couleurPremierPlan=7;if(positionDonnées==49)entréeÉlémentTerminal->couleurArrièrePlan=0;}
    if(codeCaractère=='J'&&(entréeÉlémentTerminal->valeurParamètre[0]==2||entréeÉlémentTerminal->valeurParamètre[0]==3))effacerContenuContenu();
    if(codeCaractère=='K'){unsigned positionDépart=entréeÉlémentTerminal->valeurParamètre[0]==2?0:entréeÉlémentTerminal->positionColonne,positionArrivée=entréeÉlémentTerminal->valeurParamètre[0]==1?entréeÉlémentTerminal->positionColonne+1:entréeÉlémentTerminal->colonnes;if(entréeÉlémentTerminal->valeurParamètre[0]==1)positionDépart=0;for(unsigned indiceOrdinal=positionDépart;indiceOrdinal<positionArrivée&&indiceOrdinal<entréeÉlémentTerminal->colonnes;indiceOrdinal++){
        unsigned valeurRangée=entréeÉlémentTerminal->positionRangée%nombreÉlémentsLigneHistorique,valeurCaractère=entréeÉlémentTerminal->cellulesCaractère[valeurRangée][indiceOrdinal],valeurForme=entréeÉlémentTerminal->couleurPremierPlan|(entréeÉlémentTerminal->couleurArrièrePlan<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 valeurPolice 화소를 되풀이해 칠하지 않는다. */
        int estModifié=(valeurCaractère!=0&&valeurCaractère!=' ')||entréeÉlémentTerminal->listeFormes[valeurRangée][indiceOrdinal]!=valeurForme;
        entréeÉlémentTerminal->cellulesCaractère[valeurRangée][indiceOrdinal]=' ';entréeÉlémentTerminal->listeFormes[valeurRangée][indiceOrdinal]=valeurForme;
        if(estModifié)écranPeindre(entréeÉlémentTerminal->positionRangée,indiceOrdinal);
    }}
    if(codeCaractère=='D')entréeÉlémentTerminal->positionColonne=nombreÉlémentsÉlémentListe>entréeÉlémentTerminal->positionColonne?0:entréeÉlémentTerminal->positionColonne-nombreÉlémentsÉlémentListe;if(codeCaractère=='C')entréeÉlémentTerminal->positionColonne=entréeÉlémentTerminal->positionColonne+nombreÉlémentsÉlémentListe>=entréeÉlémentTerminal->colonnes?entréeÉlémentTerminal->colonnes-1:entréeÉlémentTerminal->positionColonne+nombreÉlémentsÉlémentListe;
    if(codeCaractère=='G')entréeÉlémentTerminal->positionColonne=nombreÉlémentsÉlémentListe>entréeÉlémentTerminal->colonnes?entréeÉlémentTerminal->colonnes-1:nombreÉlémentsÉlémentListe-1;if(codeCaractère=='A')entréeÉlémentTerminal->positionRangée=nombreÉlémentsÉlémentListe>entréeÉlémentTerminal->positionRangée-entréeÉlémentTerminal->entréeÉlémentSommet?entréeÉlémentTerminal->entréeÉlémentSommet:entréeÉlémentTerminal->positionRangée-nombreÉlémentsÉlémentListe;
    if(codeCaractère=='B')entréeÉlémentTerminal->positionRangée=entréeÉlémentTerminal->positionRangée+nombreÉlémentsÉlémentListe>=entréeÉlémentTerminal->entréeÉlémentSommet+entréeÉlémentTerminal->nombreÉlémentsRangée?entréeÉlémentTerminal->entréeÉlémentSommet+entréeÉlémentTerminal->nombreÉlémentsRangée-1:entréeÉlémentTerminal->positionRangée+nombreÉlémentsÉlémentListe;
    if(codeCaractère=='H'||codeCaractère=='f'){entréeÉlémentTerminal->positionRangée=entréeÉlémentTerminal->entréeÉlémentSommet+(nombreÉlémentsÉlémentListe>entréeÉlémentTerminal->nombreÉlémentsRangée?entréeÉlémentTerminal->nombreÉlémentsRangée:nombreÉlémentsÉlémentListe)-1;unsigned coordonnéeCoordonnéeHorizontale=entréeÉlémentTerminal->valeurParamètre[1]?entréeÉlémentTerminal->valeurParamètre[1]:1;entréeÉlémentTerminal->positionColonne=(coordonnéeCoordonnéeHorizontale>entréeÉlémentTerminal->colonnes?entréeÉlémentTerminal->colonnes:coordonnéeCoordonnéeHorizontale)-1;}
    if(codeCaractère=='s'){entréeÉlémentTerminal->rangéeEnregistré=entréeÉlémentTerminal->positionRangée;entréeÉlémentTerminal->numéroColonneEnregistré=entréeÉlémentTerminal->positionColonne;}if(codeCaractère=='u'){entréeÉlémentTerminal->positionRangée=entréeÉlémentTerminal->rangéeEnregistré;entréeÉlémentTerminal->positionColonne=entréeÉlémentTerminal->numéroColonneEnregistré<entréeÉlémentTerminal->colonnes?entréeÉlémentTerminal->numéroColonneEnregistré:entréeÉlémentTerminal->colonnes-1;}
    if((codeCaractère=='h'||codeCaractère=='l')&&entréeÉlémentTerminal->valeurParamètre[0]==25)entréeÉlémentTerminal->visiblePointInsertion=codeCaractère=='h';
}
void octetTerminal(unsigned valeurDeuxième){
    entréeÉlémentTerminal=&listeFenêtres[sortie];if(!entréeÉlémentTerminal->estEnVie)return;valeurPointInsertion(0);if(entréeÉlémentTerminal->défiler){entréeÉlémentTerminal->défiler=0;if(estAffiché())valeurContenuValeur();}
    if(entréeÉlémentTerminal->échapper==1){entréeÉlémentTerminal->échapper=valeurDeuxième=='['?2:0;entréeÉlémentTerminal->indiceParamètre=0;for(unsigned indiceOrdinal=0;indiceOrdinal<4;indiceOrdinal++)entréeÉlémentTerminal->valeurParamètre[indiceOrdinal]=0;}
    else if(entréeÉlémentTerminal->échapper==2){if(valeurDeuxième=='?'){}else if(valeurDeuxième>='0'&&valeurDeuxième<='9'){if(entréeÉlémentTerminal->valeurParamètre[entréeÉlémentTerminal->indiceParamètre]<10000)entréeÉlémentTerminal->valeurParamètre[entréeÉlémentTerminal->indiceParamètre]=entréeÉlémentTerminal->valeurParamètre[entréeÉlémentTerminal->indiceParamètre]*10+valeurDeuxième-'0';}else if(valeurDeuxième==';'&&entréeÉlémentTerminal->indiceParamètre<3)entréeÉlémentTerminal->indiceParamètre++;else{séquenceContrôlePoignée(valeurDeuxième);entréeÉlémentTerminal->échapper=0;}}
    else if(valeurDeuxième==27){entréeÉlémentTerminal->valeurLongNonSigné=0;entréeÉlémentTerminal->échapper=1;}else{
        if(entréeÉlémentTerminal->valeurLongNonSigné&&(valeurDeuxième&0xc0)!=0x80){entréeÉlémentTerminal->valeurLongNonSigné=0;pointCode(0xfffd);}
        if(entréeÉlémentTerminal->valeurLongNonSigné){entréeÉlémentTerminal->résultatNonSigné=entréeÉlémentTerminal->résultatNonSigné*64+(valeurDeuxième&63);if(--entréeÉlémentTerminal->valeurLongNonSigné==0)pointCode(entréeÉlémentTerminal->résultatNonSigné<entréeÉlémentTerminal->valeurPetitFormat||entréeÉlémentTerminal->résultatNonSigné>0x10ffff||(entréeÉlémentTerminal->résultatNonSigné>=0xd800&&entréeÉlémentTerminal->résultatNonSigné<=0xdfff)?0xfffd:entréeÉlémentTerminal->résultatNonSigné);}
        else if(valeurDeuxième<128)pointCode(valeurDeuxième);else if(valeurDeuxième>=0xc2&&valeurDeuxième<=0xf4){entréeÉlémentTerminal->valeurLongNonSigné=valeurDeuxième<0xe0?1:valeurDeuxième<0xf0?2:3;entréeÉlémentTerminal->résultatNonSigné=valeurDeuxième&((1u<<(6-entréeÉlémentTerminal->valeurLongNonSigné))-1);entréeÉlémentTerminal->valeurPetitFormat=entréeÉlémentTerminal->valeurLongNonSigné==1?128:entréeÉlémentTerminal->valeurLongNonSigné==2?2048:65536;}else pointCode(0xfffd);
    }valeurPointInsertion(1);
}
int enAttenteTerminal(void){return estEnAttente!=0;}
/* valeurCoin numéro: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int glisserRedimensionner=-1,coinSaisi,coordonnéeHorizontaleSaisi,coordonnéeVerticaleSaisi,positionHorizontalInitialValeur,positionVerticalInitialValeur,valeurLargeurInitialValeur,valeurHauteurInitialValeur;
static int fenêtrePointé(int positionHorizontal,int positionVertical) {
    for(int valeurSéquence=nombreÉlémentsEntréeÉlément-1;valeurSéquence>=0;valeurSéquence--){
        int valeurIdentificateur=valeurOrdre[valeurSéquence];Terminal *fenêtre=&listeFenêtres[valeurIdentificateur];
        if(positionHorizontal>=(int)fenêtre->coordonnéeCoordonnéeHorizontale&&positionVertical>=(int)fenêtre->coordonnéeCoordonnéeVerticale&&
           positionHorizontal<(int)(fenêtre->coordonnéeCoordonnéeHorizontale+fenêtre->valeurLargeur)&&positionVertical<(int)(fenêtre->coordonnéeCoordonnéeVerticale+fenêtre->valeurHauteur))return valeurIdentificateur;
    }return -1;
}
static int trouverCoin(int valeurIdentificateur,int positionHorizontal,int positionVertical) {
    if(valeurIdentificateur<0)return 0;Terminal *fenêtre=&listeFenêtres[valeurIdentificateur];
    int côtéGauche=positionHorizontal<(int)fenêtre->coordonnéeCoordonnéeHorizontale+8,droit=positionHorizontal>=(int)(fenêtre->coordonnéeCoordonnéeHorizontale+fenêtre->valeurLargeur)-8;
    int côtéSupérieur=positionVertical<(int)fenêtre->coordonnéeCoordonnéeVerticale+8,côtéInférieur=positionVertical>=(int)(fenêtre->coordonnéeCoordonnéeVerticale+fenêtre->valeurHauteur)-8;
    return (côtéGauche||droit)&&(côtéSupérieur||côtéInférieur)?1+droit+côtéInférieur*2:0;
}
static int valeurSéparateur(int valeur,int valeurMinimal,int valeurMaximal){return valeur<valeurMinimal?valeurMinimal:valeur>valeurMaximal?valeurMaximal:valeur;}
static void redimensionnerDéplacer(int positionHorizontal,int positionVertical) {
    Terminal *fenêtre=&listeFenêtres[glisserRedimensionner];int côtéGauche=positionHorizontalInitialValeur,côtéSupérieur=positionVerticalInitialValeur,droit=positionHorizontalInitialValeur+valeurLargeurInitialValeur,côtéInférieur=positionVerticalInitialValeur+valeurHauteurInitialValeur;
    if(coinSaisi==1||coinSaisi==3)côtéGauche=valeurSéparateur(positionHorizontalInitialValeur+positionHorizontal-coordonnéeHorizontaleSaisi,0,droit-360);
    else droit=valeurSéparateur(positionHorizontalInitialValeur+valeurLargeurInitialValeur+positionHorizontal-coordonnéeHorizontaleSaisi,côtéGauche+360,largeurÉcranCarteMatérielle());
    if(coinSaisi<=2)côtéSupérieur=valeurSéparateur(positionVerticalInitialValeur+positionVertical-coordonnéeVerticaleSaisi,34,côtéInférieur-216);
    else côtéInférieur=valeurSéparateur(positionVerticalInitialValeur+valeurHauteurInitialValeur+positionVertical-coordonnéeVerticaleSaisi,côtéSupérieur+216,hauteurÉcranCarteMatérielle());
    unsigned colonnes=(droit-côtéGauche-24)/8,nombreÉlémentsRangée=(côtéInférieur-côtéSupérieur-56)/16;
    if(fenêtre->colonnes!=colonnes||fenêtre->nombreÉlémentsRangée!=nombreÉlémentsRangée){
        fenêtre->redimensionnéÉtait=1;fenêtre->colonnes=colonnes;fenêtre->nombreÉlémentsRangée=nombreÉlémentsRangée;
        if(fenêtre->positionColonne>=colonnes)fenêtre->positionColonne=colonnes-1;
        if(fenêtre->positionRangée>=fenêtre->entréeÉlémentSommet+nombreÉlémentsRangée)fenêtre->entréeÉlémentSommet=fenêtre->positionRangée-nombreÉlémentsRangée+1;
        unsigned limiteCapacité=fenêtre->entréeÉlémentSommet;if(limiteCapacité>nombreÉlémentsLigneHistorique-nombreÉlémentsRangée)limiteCapacité=nombreÉlémentsLigneHistorique-nombreÉlémentsRangée;
        if(fenêtre->défiler>limiteCapacité)fenêtre->défiler=limiteCapacité;
    }
    int positionHorizontalAncien=fenêtre->coordonnéeCoordonnéeHorizontale,positionVerticalAncien=fenêtre->coordonnéeCoordonnéeVerticale,largeurAncien=fenêtre->valeurLargeur,longueurAncien=fenêtre->valeurHauteur;
    if(positionHorizontalAncien==côtéGauche&&positionVerticalAncien==côtéSupérieur&&largeurAncien==droit-côtéGauche&&longueurAncien==côtéInférieur-côtéSupérieur)return;
    fenêtre->coordonnéeCoordonnéeHorizontale=côtéGauche;fenêtre->coordonnéeCoordonnéeVerticale=côtéSupérieur;fenêtre->valeurLargeur=droit-côtéGauche;fenêtre->valeurHauteur=côtéInférieur-côtéSupérieur;
    bornesFenêtrePeindre(positionHorizontalAncien,positionVerticalAncien,largeurAncien,longueurAncien,fenêtre);
}
void pointeurTerminal(unsigned élémentListeSuivant,int coordonnéeCoordonnéeHorizontale,int coordonnéeCoordonnéeVerticale){
    unsigned estEnfoncé=élémentListeSuivant&~boutons;boutons=élémentListeSuivant;
    if(!vueBureau){valeurGlisser=-1;glisserRedimensionner=-1;pointeurCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,1);return;}
    if(!(élémentListeSuivant&1)){valeurGlisser=-1;glisserRedimensionner=-1;}
    if(glisserRedimensionner>=0&&!listeFenêtres[glisserRedimensionner].estEnVie)glisserRedimensionner=-1;
    if(valeurGlisser>=0&&!listeFenêtres[valeurGlisser].estEnVie)valeurGlisser=-1;
    if(glisserRedimensionner>=0){
        redimensionnerDéplacer(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale);pointeurCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,coinSaisi==1||coinSaisi==4?2:3);return;
    }
    pointeurCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,1);
    if(valeurGlisser>=0){
        Terminal *fenêtre=&listeFenêtres[valeurGlisser];
        int positionHorizontalAncien=fenêtre->coordonnéeCoordonnéeHorizontale,positionVerticalAncien=fenêtre->coordonnéeCoordonnéeVerticale;
        fenêtre->coordonnéeCoordonnéeHorizontale=valeurSéparateur(coordonnéeCoordonnéeHorizontale-coordonnéeHorizontaleGlisser,0,largeurÉcranCarteMatérielle()-fenêtre->valeurLargeur);
        fenêtre->coordonnéeCoordonnéeVerticale=valeurSéparateur(coordonnéeCoordonnéeVerticale-coordonnéeVerticaleGlisser,34,hauteurÉcranCarteMatérielle()-fenêtre->valeurHauteur);
        if(positionHorizontalAncien!=(int)fenêtre->coordonnéeCoordonnéeHorizontale||positionVerticalAncien!=(int)fenêtre->coordonnéeCoordonnéeVerticale)bornesFenêtrePeindre(positionHorizontalAncien,positionVerticalAncien,fenêtre->valeurLargeur,fenêtre->valeurHauteur,fenêtre);
        return;
    }
    extern int superposerÉcran(int,int,int);
    if(superposerÉcran(focus,coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale)){pointeurÉcran(focus,estEnfoncé,coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale);return;}
    int valeurIdentificateur=fenêtrePointé(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale),valeurCoin=trouverCoin(valeurIdentificateur,coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale);
    if(valeurCoin)pointeurCarteMatérielle(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,valeurCoin==1||valeurCoin==4?2:3);
    if(estEnfoncé&1){
        if(valeurCoin){
            Terminal *fenêtre=&listeFenêtres[valeurIdentificateur];glisserRedimensionner=valeurIdentificateur;coinSaisi=valeurCoin;coordonnéeHorizontaleSaisi=coordonnéeCoordonnéeHorizontale;coordonnéeVerticaleSaisi=coordonnéeCoordonnéeVerticale;
            positionHorizontalInitialValeur=fenêtre->coordonnéeCoordonnéeHorizontale;positionVerticalInitialValeur=fenêtre->coordonnéeCoordonnéeVerticale;valeurLargeurInitialValeur=fenêtre->valeurLargeur;valeurHauteurInitialValeur=fenêtre->valeurHauteur;
            if(valeurIdentificateur!=focus)avantCôtéVersApporter(valeurIdentificateur);return;
        }
        if(coordonnéeCoordonnéeVerticale<32&&coordonnéeCoordonnéeHorizontale>=6&&coordonnéeCoordonnéeHorizontale<142){créerEntréeÉlément();return;}
        if(coordonnéeCoordonnéeVerticale<32&&coordonnéeCoordonnéeHorizontale>=154&&coordonnéeCoordonnéeHorizontale<602){avantCôtéVersApporter((coordonnéeCoordonnéeHorizontale-154)/112);return;}
        if(valeurIdentificateur>=0){
            Terminal *fenêtre=&listeFenêtres[valeurIdentificateur];
            if(coordonnéeCoordonnéeVerticale<(int)fenêtre->coordonnéeCoordonnéeVerticale+30&&coordonnéeCoordonnéeHorizontale>=(int)(fenêtre->coordonnéeCoordonnéeHorizontale+fenêtre->valeurLargeur)-32){fermerFenêtre(valeurIdentificateur);return;}
            if(valeurIdentificateur!=focus)avantCôtéVersApporter(valeurIdentificateur);
            if(coordonnéeCoordonnéeVerticale<(int)fenêtre->coordonnéeCoordonnéeVerticale+30){valeurGlisser=valeurIdentificateur;coordonnéeHorizontaleGlisser=coordonnéeCoordonnéeHorizontale-fenêtre->coordonnéeCoordonnéeHorizontale;coordonnéeVerticaleGlisser=coordonnéeCoordonnéeVerticale-fenêtre->coordonnéeCoordonnéeVerticale;}return;
        }
    }
    if(focus>=0&&(estEnfoncé&(8|16))){entréeÉlémentTerminal=&listeFenêtres[focus];if(estEnfoncé&8){unsigned limiteCapacité=entréeÉlémentTerminal->entréeÉlémentSommet;if(limiteCapacité>nombreÉlémentsLigneHistorique-entréeÉlémentTerminal->nombreÉlémentsRangée)limiteCapacité=nombreÉlémentsLigneHistorique-entréeÉlémentTerminal->nombreÉlémentsRangée;entréeÉlémentTerminal->défiler=entréeÉlémentTerminal->défiler+9>limiteCapacité?limiteCapacité:entréeÉlémentTerminal->défiler+9;}else entréeÉlémentTerminal->défiler=entréeÉlémentTerminal->défiler<9?0:entréeÉlémentTerminal->défiler-9;redessiner();}
}
void raccourciClavierTerminal(unsigned valeurEnfoncé){if(valeurEnfoncé==1)créerEntréeÉlément();if(valeurEnfoncé==2&&nombreÉlémentsEntréeÉlément)avantCôtéVersApporter(valeurOrdre[0]);if(valeurEnfoncé==3)fermerFenêtre(focus);}
motMachine terminalCarteMatérielle(motMachine action){
    if(action==300){if(!listeFenêtres[sortie].estEnVie)return créerEntréeÉlément();vueBureau=1;redessiner();return 0;}
    if(action==0){fermerFenêtre(focus);return 0;}if(action==1)return (uint32_t)créerEntréeÉlément();if(action==2)return focus>=0;
    if(action==9){vueBureau=0;return 0;}if(action==7)return nombreÉlémentsEntréeÉlément;if(action==10)return focus+1;if(action==11)return sortie;
    if(action==13){Terminal *fenêtre=&listeFenêtres[sortie];return fenêtre->estEnVie?(fenêtre->nombreÉlémentsRangée<<16)|fenêtre->colonnes:(19<<16)|68;}
    if(action==14){unsigned valeur=listeFenêtres[sortie].redimensionnéÉtait;listeFenêtres[sortie].redimensionnéÉtait=0;return valeur;}
    if(action==12){unsigned valeur=estEnAttente;estEnAttente=0;return valeur;}
    if(action>=20&&action<24)return listeFenêtres[action-20].estEnVie;
    if(action>=100&&action<104){sortie=action-100;entréeÉlémentTerminal=&listeFenêtres[sortie];return 0;}
    if(action>=200&&action<204){avantCôtéVersApporter(action-200);return 0;}
    if(action==3){redessiner();return 0;}entréeÉlémentTerminal=&listeFenêtres[sortie];if(!entréeÉlémentTerminal->estEnVie)return 0;
    if(action==4)effacerContenuContenu();if(action==5||action==6){unsigned élémentListePrécédentÉlément=boutons;pointeurTerminal(action==5?8:16,0,0);boutons=élémentListePrécédentÉlément;}return 1;
}

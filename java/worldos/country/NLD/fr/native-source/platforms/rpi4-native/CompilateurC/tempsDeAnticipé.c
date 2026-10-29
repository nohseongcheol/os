#include "../nommage/nomsLierMachine.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "invoquer.h"
#include "Paquet.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char Données[16384];static unsigned longueur,positionActuel;static int estInvalide;
static unsigned listeBalises[512],valeurPremier[512],valeurDeuxième[512],réserveConstante,classeActuel;
static char texte[65536];static unsigned tailleTexte;
typedef struct {unsigned bitsConfiguration,nom,donnéesDescripteur,séquenceInstructionMachine,taille,variablesLocal,stockagePile;} entréeÉlémentMéthode;
static entréeÉlémentMéthode méthodesDéclaré[64];static unsigned nombreÉlémentsMéthodeDéclaré;
static unsigned nomChamp[64],descripteurChamp[64],constanteChamp[64],nombreÉlémentsChampDéclaré;
static unsigned valeurPrendre(unsigned nombreÉlémentsÉlémentListe){if(positionActuel>longueur||nombreÉlémentsÉlémentListe>longueur-positionActuel){estInvalide=1;return 0;}unsigned positionDonnées=positionActuel;positionActuel+=nombreÉlémentsÉlémentListe;return positionDonnées;}
static unsigned donnéesOctet(void){unsigned positionDonnées=valeurPrendre(1);return estInvalide?0:Données[positionDonnées];}
static unsigned valeurMoitié(void){unsigned coordonnéeCoordonnéeHorizontale=donnéesOctet();return coordonnéeCoordonnéeHorizontale<<8|donnéesOctet();}
static uint32_t estPlein(void){uint32_t coordonnéeCoordonnéeHorizontale=valeurMoitié();return coordonnéeCoordonnéeHorizontale<<16|valeurMoitié();}
static int valeurUnicode(unsigned indiceOrdinal,const char*donnéesChaîne){return indiceOrdinal>0&&indiceOrdinal<réserveConstante&&listeBalises[indiceOrdinal]==1&&strlen(donnéesChaîne)==valeurDeuxième[indiceOrdinal]&&!memcmp(Données+valeurPremier[indiceOrdinal],donnéesChaîne,valeurDeuxième[indiceOrdinal]);}
static int texteÉgal(unsigned coordonnéeCoordonnéeHorizontale,unsigned coordonnéeCoordonnéeVerticale){return coordonnéeCoordonnéeHorizontale>0&&coordonnéeCoordonnéeHorizontale<réserveConstante&&coordonnéeCoordonnéeVerticale>0&&coordonnéeCoordonnéeVerticale<réserveConstante&&listeBalises[coordonnéeCoordonnéeHorizontale]==1&&listeBalises[coordonnéeCoordonnéeVerticale]==1&&valeurDeuxième[coordonnéeCoordonnéeHorizontale]==valeurDeuxième[coordonnéeCoordonnéeVerticale]&&!memcmp(Données+valeurPremier[coordonnéeCoordonnéeHorizontale],Données+valeurPremier[coordonnéeCoordonnéeVerticale],valeurDeuxième[coordonnéeCoordonnéeHorizontale]);}
static void émettreValeur(const char*entréeÉlémentFichier,...){if(estInvalide)return;va_list tableauArgument;va_start(tableauArgument,entréeÉlémentFichier);int nombreÉlémentsÉlémentListe=vsnprintf(texte+tailleTexte,sizeof(texte)-tailleTexte,entréeÉlémentFichier,tableauArgument);va_end(tableauArgument);if(nombreÉlémentsÉlémentListe<0||(unsigned)nombreÉlémentsÉlémentListe>=sizeof(texte)-tailleTexte){estInvalide=1;return;}tailleTexte+=nombreÉlémentsÉlémentListe;}
static int entréeÉlémentDescripteur(unsigned valeurIdentificateur,int*résultat){
    if(valeurIdentificateur<1||valeurIdentificateur>=réserveConstante||listeBalises[valeurIdentificateur]!=1)return -1;unsigned positionDonnées=valeurPremier[valeurIdentificateur],décalageFin=positionDonnées+valeurDeuxième[valeurIdentificateur];if(positionDonnées>=décalageFin||Données[positionDonnées++]!='(')return -1;int nombreÉlémentsEntréeÉlément=0;
    while(positionDonnées<décalageFin&&Données[positionDonnées]!=')'){
        unsigned codeCaractère=Données[positionDonnées++];while(codeCaractère=='['&&positionDonnées<décalageFin)codeCaractère=Données[positionDonnées++];
        if(codeCaractère=='L'){while(positionDonnées<décalageFin&&Données[positionDonnées]!=';')positionDonnées++;if(positionDonnées==décalageFin)return -1;positionDonnées++;}
        else if(codeCaractère!='I'&&codeCaractère!='Z'&&codeCaractère!='B'&&codeCaractère!='C'&&codeCaractère!='S')return -1;
        if(++nombreÉlémentsEntréeÉlément>16)return -1;
    }
    if(positionDonnées+1>=décalageFin||Données[positionDonnées++]!=')')return -1;*résultat=Données[positionDonnées]=='V'?0:1;
    if(Données[positionDonnées]=='J'||Données[positionDonnées]=='D'||Données[positionDonnées]=='F')return -1;return nombreÉlémentsEntréeÉlément;
}
static void attributs(void){unsigned nombreÉlémentsÉlémentListe=valeurMoitié();for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe&&!estInvalide;indiceOrdinal++){valeurMoitié();unsigned taille=estPlein();valeurPrendre(taille);}}
static int analyserEntrée(void){
    if(estPlein()!=0xcafebabe)return -1;unsigned versionMineur=valeurMoitié(),numéroVersion=valeurMoitié();if(versionMineur||numéroVersion<45||numéroVersion>52)return -1;
    réserveConstante=valeurMoitié();if(réserveConstante<1||réserveConstante>512)return -1;
    for(unsigned indiceOrdinal=1;indiceOrdinal<réserveConstante&&!estInvalide;indiceOrdinal++){
        listeBalises[indiceOrdinal]=donnéesOctet();switch(listeBalises[indiceOrdinal]){
        case 1:valeurDeuxième[indiceOrdinal]=valeurMoitié();valeurPremier[indiceOrdinal]=valeurPrendre(valeurDeuxième[indiceOrdinal]);break;case 3:case 4:valeurPremier[indiceOrdinal]=estPlein();break;
        case 5:case 6:valeurPrendre(8);if(++indiceOrdinal>=réserveConstante)return -1;break;
        case 7:case 8:case 16:valeurPremier[indiceOrdinal]=valeurMoitié();break;
        case 9:case 10:case 11:case 12:case 18:valeurPremier[indiceOrdinal]=valeurMoitié();valeurDeuxième[indiceOrdinal]=valeurMoitié();break;
        case 15:valeurPremier[indiceOrdinal]=donnéesOctet();valeurDeuxième[indiceOrdinal]=valeurMoitié();break;default:return -1;
        }
    }
    valeurMoitié();classeActuel=valeurMoitié();valeurMoitié();if(classeActuel<1||classeActuel>=réserveConstante||listeBalises[classeActuel]!=7||valeurPremier[classeActuel]<1||valeurPremier[classeActuel]>=réserveConstante||listeBalises[valeurPremier[classeActuel]]!=1)return -1;unsigned interfaces=valeurMoitié();valeurPrendre(interfaces*2);
    nombreÉlémentsChampDéclaré=valeurMoitié();if(nombreÉlémentsChampDéclaré>64)return -1;
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsChampDéclaré&&!estInvalide;indiceOrdinal++){
        unsigned bitsConfiguration=valeurMoitié();nomChamp[indiceOrdinal]=valeurMoitié();descripteurChamp[indiceOrdinal]=valeurMoitié();
        if(!(bitsConfiguration&8))return -1;
        unsigned nombreÉlémentsEntréeÉlément=valeurMoitié();for(unsigned ordinalInterne=0;ordinalInterne<nombreÉlémentsEntréeÉlément&&!estInvalide;ordinalInterne++){
            unsigned nom=valeurMoitié(),taille=estPlein();
            if(valeurUnicode(nom,"ConstantValue")){if(taille!=2)return -1;constanteChamp[indiceOrdinal]=valeurMoitié();}
            else valeurPrendre(taille);
        }
    }
    nombreÉlémentsMéthodeDéclaré=valeurMoitié();if(nombreÉlémentsMéthodeDéclaré>64)return -1;
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsMéthodeDéclaré&&!estInvalide;indiceOrdinal++){
        entréeÉlémentMéthode*tailleGroupe=méthodesDéclaré+indiceOrdinal;tailleGroupe->bitsConfiguration=valeurMoitié();tailleGroupe->nom=valeurMoitié();tailleGroupe->donnéesDescripteur=valeurMoitié();unsigned nombreÉlémentsEntréeÉlément=valeurMoitié();
        for(unsigned ordinalInterne=0;ordinalInterne<nombreÉlémentsEntréeÉlément&&!estInvalide;ordinalInterne++){
            unsigned nom=valeurMoitié(),taille=estPlein(),lancer=positionActuel;
            if(taille>longueur-positionActuel)return -1;
            if(valeurUnicode(nom,"Code")){
                tailleGroupe->stockagePile=valeurMoitié();tailleGroupe->variablesLocal=valeurMoitié();tailleGroupe->taille=estPlein();tailleGroupe->séquenceInstructionMachine=valeurPrendre(tailleGroupe->taille);
                if(tailleGroupe->stockagePile>128||tailleGroupe->variablesLocal>128||tailleGroupe->taille>8192||valeurMoitié())return -1;attributs();
            }else valeurPrendre(taille);
            if(positionActuel!=lancer+taille)return -1;
        }
        if(!valeurUnicode(tailleGroupe->nom,"<init>")&&(!(tailleGroupe->bitsConfiguration&8)||(tailleGroupe->bitsConfiguration&(0x100|0x20))||!tailleGroupe->taille))return -1;
    }
    attributs();return estInvalide||positionActuel!=longueur?-1:0;
}
static void valeurConstante(unsigned valeurIdentificateur){
    if(!valeurIdentificateur||valeurIdentificateur>=réserveConstante){estInvalide=1;return;}
    if(listeBalises[valeurIdentificateur]==3)émettreValeur("P(%uU);",valeurPremier[valeurIdentificateur]);
    else if(listeBalises[valeurIdentificateur]==8)émettreValeur("P((W)k%u);",valeurIdentificateur);else estInvalide=1;
}
static void invoquer(unsigned valeurIdentificateur,int appelVirtuel){
    if(valeurIdentificateur<1||valeurIdentificateur>=réserveConstante||(listeBalises[valeurIdentificateur]!=10&&listeBalises[valeurIdentificateur]!=11)||valeurPremier[valeurIdentificateur]<1||valeurPremier[valeurIdentificateur]>=réserveConstante||listeBalises[valeurPremier[valeurIdentificateur]]!=7||valeurDeuxième[valeurIdentificateur]<1||valeurDeuxième[valeurIdentificateur]>=réserveConstante||listeBalises[valeurDeuxième[valeurIdentificateur]]!=12){estInvalide=1;return;}
    unsigned objetPropriétaire=valeurPremier[valeurPremier[valeurIdentificateur]],nom=valeurPremier[valeurDeuxième[valeurIdentificateur]],donnéesDescripteur=valeurDeuxième[valeurDeuxième[valeurIdentificateur]];int résultat=0,nombreÉlémentsÉlémentListe=entréeÉlémentDescripteur(donnéesDescripteur,&résultat);if(nombreÉlémentsÉlémentListe<0){estInvalide=1;return;}
    for(int indiceOrdinal=nombreÉlémentsÉlémentListe;indiceOrdinal>0;indiceOrdinal--)émettreValeur("x[%d]=Q();",indiceOrdinal-1);if(appelVirtuel)émettreValeur("Q();");
    if(!appelVirtuel&&texteÉgal(objetPropriétaire,valeurPremier[classeActuel])){
        unsigned tailleGroupe=0;for(;tailleGroupe<nombreÉlémentsMéthodeDéclaré;tailleGroupe++)if(texteÉgal(nom,méthodesDéclaré[tailleGroupe].nom)&&texteÉgal(donnéesDescripteur,méthodesDéclaré[tailleGroupe].donnéesDescripteur))break;
        if(tailleGroupe==nombreÉlémentsMéthodeDéclaré||!(méthodesDéclaré[tailleGroupe].bitsConfiguration&8)){estInvalide=1;return;}
        if(résultat)émettreValeur("P(");émettreValeur("m%u(",tailleGroupe);for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)émettreValeur(indiceOrdinal?",x[%d]":"x[%d]",indiceOrdinal);émettreValeur(résultat?"));":" );");return;
    }
    if((appelVirtuel&&valeurUnicode(objetPropriétaire,"java/io/PrintStream")&& (valeurUnicode(nom,"print")||valeurUnicode(nom,"println")))||(!appelVirtuel&&valeurUnicode(objetPropriétaire,"français/interne/Sortie"))){
        if(valeurUnicode(donnéesDescripteur,"(I)V")&&(valeurUnicode(nom,"print")||valeurUnicode(nom,"println")||valeurUnicode(nom,"écrireNuméro"))){émettreValeur("jprint(x[0],1,%d);",valeurUnicode(nom,"print")?0:1);return;}
        if(valeurUnicode(donnéesDescripteur,"(Ljava/lang/String;)V")&&(valeurUnicode(nom,"print")||valeurUnicode(nom,"println")||valeurUnicode(nom,"écrire")||valeurUnicode(nom,"écrireLigne"))){émettreValeur("jprint(x[0],0,%d);",valeurUnicode(nom,"print")||valeurUnicode(nom,"écrire")?0:1);return;}
        if(valeurUnicode(donnéesDescripteur,"()V")&&valeurUnicode(nom,"println")){émettreValeur("jprint((W)\"\",0,1);");return;}
    }
    if(!appelVirtuel&&valeurUnicode(objetPropriétaire,"français/interne/Fichier")){
        if(valeurUnicode(nom,"écrire")&&valeurUnicode(donnéesDescripteur,"(Ljava/lang/String;Ljava/lang/String;)V")){émettreValeur("jfwrite(x[0],x[1]);");return;}
        if(valeurUnicode(nom,"lire")&&valeurUnicode(donnéesDescripteur,"(Ljava/lang/String;)Ljava/lang/String;")){émettreValeur("P(jfread(x[0]));");return;}
    }
    estInvalide=1;
}
static void compilerMéthode(unsigned indiceRechercher){
    entréeÉlémentMéthode*tailleGroupe=méthodesDéclaré+indiceRechercher;if(valeurUnicode(tailleGroupe->nom,"<init>"))return;int résultat,nombreÉlémentsÉlémentListe=entréeÉlémentDescripteur(tailleGroupe->donnéesDescripteur,&résultat);if(nombreÉlémentsÉlémentListe<0){estInvalide=1;return;}
    émettreValeur("static W m%u(",indiceRechercher);for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)émettreValeur(indiceOrdinal?",W a%d":"W a%d",indiceOrdinal);if(!nombreÉlémentsÉlémentListe)émettreValeur("void");
    if((unsigned)nombreÉlémentsÉlémentListe>tailleGroupe->variablesLocal){estInvalide=1;return;}
    émettreValeur("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",tailleGroupe->variablesLocal?tailleGroupe->variablesLocal:1);for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)émettreValeur("v[%d]=a%d;",indiceOrdinal,indiceOrdinal);
    unsigned enregistré=longueur;longueur=tailleGroupe->séquenceInstructionMachine+tailleGroupe->taille;positionActuel=tailleGroupe->séquenceInstructionMachine;
    while(positionActuel<longueur&&!estInvalide){unsigned positionCommande=positionActuel-tailleGroupe->séquenceInstructionMachine,valeurOpération=donnéesOctet();émettreValeur("L%u:;",positionCommande);
        if(valeurOpération==0){}
        else if(valeurOpération==1)émettreValeur("P(0);");
        else if(valeurOpération>=2&&valeurOpération<=8)émettreValeur("P(%uU);",valeurOpération-3);
        else if(valeurOpération==16){int valeur=(int8_t)donnéesOctet();émettreValeur("P(%uU);",(unsigned)valeur);}
        else if(valeurOpération==17){int valeur=(int16_t)valeurMoitié();émettreValeur("P(%uU);",(unsigned)valeur);}
        else if(valeurOpération==18||valeurOpération==19)valeurConstante(valeurOpération==18?donnéesOctet():valeurMoitié());
        else if(valeurOpération==21||valeurOpération==25){unsigned indiceOrdinal=donnéesOctet();if(indiceOrdinal>=tailleGroupe->variablesLocal)estInvalide=1;émettreValeur("P(v[%u]);",indiceOrdinal);}
        else if((valeurOpération>=26&&valeurOpération<=29)||(valeurOpération>=42&&valeurOpération<=45)){unsigned indiceOrdinal=valeurOpération>=42?valeurOpération-42:valeurOpération-26;if(indiceOrdinal>=tailleGroupe->variablesLocal)estInvalide=1;émettreValeur("P(v[%u]);",indiceOrdinal);}
        else if(valeurOpération==54||valeurOpération==58){unsigned indiceOrdinal=donnéesOctet();if(indiceOrdinal>=tailleGroupe->variablesLocal)estInvalide=1;émettreValeur("v[%u]=Q();",indiceOrdinal);}
        else if((valeurOpération>=59&&valeurOpération<=62)||(valeurOpération>=75&&valeurOpération<=78)){unsigned indiceOrdinal=valeurOpération>=75?valeurOpération-75:valeurOpération-59;if(indiceOrdinal>=tailleGroupe->variablesLocal)estInvalide=1;émettreValeur("v[%u]=Q();",indiceOrdinal);}
        else if(valeurOpération==46||valeurOpération==50||valeurOpération==51||valeurOpération==52||valeurOpération==53)émettreValeur("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(valeurOpération==79||valeurOpération==83||valeurOpération==84||valeurOpération==85||valeurOpération==86)émettreValeur("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",valeurOpération==84?"(unsigned)(signed char)q":valeurOpération==85?"(unsigned short)q":valeurOpération==86?"(unsigned)(short)q":"q");
        else if(valeurOpération==87)émettreValeur("Q();");
        else if(valeurOpération==89)émettreValeur("q=Q();P(q);P(q);");
        else if(valeurOpération==90)émettreValeur("q=Q();r=Q();P(q);P(r);P(q);");
        else if(valeurOpération==95)émettreValeur("q=Q();r=Q();P(q);P(r);");
        else if(valeurOpération==96||valeurOpération==100||valeurOpération==104||valeurOpération==120||valeurOpération==124||valeurOpération==126||valeurOpération==128||valeurOpération==130){const char*valeurEncodage=valeurOpération==96?"+":valeurOpération==100?"-":valeurOpération==104?"*":valeurOpération==120?"<<":valeurOpération==124?">>":valeurOpération==126?"&":valeurOpération==128?"|":"^";émettreValeur("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",valeurEncodage,valeurOpération==120||valeurOpération==124?"%32":"");}
        else if(valeurOpération==108||valeurOpération==112)émettreValeur("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",valeurOpération==112);
        else if(valeurOpération==116)émettreValeur("P(0U-(unsigned)Q());");
        else if(valeurOpération==122)émettreValeur("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(valeurOpération==132){unsigned indiceOrdinal=donnéesOctet();int valeurDifférence=(int8_t)donnéesOctet();if(indiceOrdinal>=tailleGroupe->variablesLocal)estInvalide=1;émettreValeur("v[%u]=(unsigned)v[%u]+%uU;",indiceOrdinal,indiceOrdinal,(unsigned)valeurDifférence);}
        else if(valeurOpération>=145&&valeurOpération<=147)émettreValeur("P((unsigned)(%s)Q());",valeurOpération==145?"signed char":valeurOpération==146?"unsigned short":"short");
        else if(valeurOpération>=153&&valeurOpération<=166){int valeurCible=(int)positionCommande+(int16_t)valeurMoitié();const char*valeurComparaison[]={"==","!=","<",">=",">","<="};if(valeurCible<0||valeurCible>=(int)tailleGroupe->taille){estInvalide=1;break;}if(valeurOpération<159)émettreValeur("if((int)Q()%s0)goto L%d;",valeurComparaison[valeurOpération-153],valeurCible);else if(valeurOpération<165)émettreValeur("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",valeurComparaison[valeurOpération-159],valeurCible);else émettreValeur("q=Q();r=Q();if(r%sq)goto L%d;",valeurOpération==165?"==":"!=",valeurCible);}
        else if(valeurOpération==167){int valeurCible=(int)positionCommande+(int16_t)valeurMoitié();if(valeurCible<0||valeurCible>=(int)tailleGroupe->taille)estInvalide=1;émettreValeur("goto L%d;",valeurCible);}
        else if(valeurOpération==172||valeurOpération==176)émettreValeur("return Q();");else if(valeurOpération==177)émettreValeur("return 0;");
        else if(valeurOpération==178||valeurOpération==179){unsigned valeurIdentificateur=valeurMoitié();if(valeurIdentificateur<1||valeurIdentificateur>=réserveConstante||listeBalises[valeurIdentificateur]!=9||valeurPremier[valeurIdentificateur]>=réserveConstante||valeurDeuxième[valeurIdentificateur]>=réserveConstante||listeBalises[valeurPremier[valeurIdentificateur]]!=7||listeBalises[valeurDeuxième[valeurIdentificateur]]!=12){estInvalide=1;break;}unsigned objetPropriétaire=valeurPremier[valeurPremier[valeurIdentificateur]],nom=valeurPremier[valeurDeuxième[valeurIdentificateur]],donnéesDescripteur=valeurDeuxième[valeurDeuxième[valeurIdentificateur]];
            if(valeurOpération==178&&valeurUnicode(objetPropriétaire,"java/lang/System")&&valeurUnicode(nom,"out")&&valeurUnicode(donnéesDescripteur,"Ljava/io/PrintStream;"))émettreValeur("P(1);");
            else {unsigned entréeÉlémentFichier=0;while(entréeÉlémentFichier<nombreÉlémentsChampDéclaré&&(!texteÉgal(nom,nomChamp[entréeÉlémentFichier])||!texteÉgal(donnéesDescripteur,descripteurChamp[entréeÉlémentFichier])))entréeÉlémentFichier++;if(!texteÉgal(objetPropriétaire,valeurPremier[classeActuel])||entréeÉlémentFichier==nombreÉlémentsChampDéclaré){estInvalide=1;break;}émettreValeur(valeurOpération==178?"P(fields[%u]);":"fields[%u]=Q();",entréeÉlémentFichier);}}
        else if(valeurOpération==182||valeurOpération==184)invoquer(valeurMoitié(),valeurOpération==182);
        else if(valeurOpération==188){unsigned catégorieType=donnéesOctet();if(catégorieType!=4&&catégorieType!=5&&catégorieType!=8&&catégorieType!=9&&catégorieType!=10)estInvalide=1;émettreValeur("P(jarray((int)Q()));");}
        else if(valeurOpération==190)émettreValeur("P(jlength(Q()));");
        else if(valeurOpération==198||valeurOpération==199){int valeurCible=(int)positionCommande+(int16_t)valeurMoitié();if(valeurCible<0||valeurCible>=(int)tailleGroupe->taille)estInvalide=1;émettreValeur("if(Q()%s0)goto L%d;",valeurOpération==198?"==":"!=",valeurCible);}
        else estInvalide=1;
        if(estInvalide)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",indiceRechercher,valeurOpération,positionCommande);
        émettreValeur("\n");
    }
    longueur=enregistré;émettreValeur("jfail();return 0;}\n");
}
static unsigned unitéChaîne(unsigned *positionDonnées,unsigned décalageFin){
    if(*positionDonnées>=décalageFin){estInvalide=1;return 0;}unsigned codeCaractère=Données[(*positionDonnées)++];
    if(codeCaractère<128)return codeCaractère;
    unsigned nombreÉlémentsÉlémentListe=codeCaractère>=0xc0&&codeCaractère<=0xdf?1:codeCaractère>=0xe0&&codeCaractère<=0xef?2:3;
    if(nombreÉlémentsÉlémentListe==3||nombreÉlémentsÉlémentListe>décalageFin-*positionDonnées){estInvalide=1;return 0;}unsigned valeur=codeCaractère&((1u<<(6-nombreÉlémentsÉlémentListe))-1);
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++){unsigned élémentListeSuivant=Données[(*positionDonnées)++];if((élémentListeSuivant&0xc0)!=0x80)estInvalide=1;valeur=valeur<<6|(élémentListeSuivant&63);}
    if((nombreÉlémentsÉlémentListe==1&&valeur<128&&valeur!=0)||(nombreÉlémentsÉlémentListe==2&&valeur<2048))estInvalide=1;return valeur;
}
static void constanteChaîne(unsigned valeurIdentificateur){
    unsigned valeurNonSigné=valeurPremier[valeurIdentificateur];if(valeurNonSigné<1||valeurNonSigné>=réserveConstante||listeBalises[valeurNonSigné]!=1){estInvalide=1;return;}émettreValeur("static const unsigned char k%u[]={",valeurIdentificateur);
    unsigned positionDonnées=valeurPremier[valeurNonSigné],décalageFin=positionDonnées+valeurDeuxième[valeurNonSigné];
    while(positionDonnées<décalageFin&&!estInvalide){unsigned codeCaractère=unitéChaîne(&positionDonnées,décalageFin);
        if(codeCaractère>=0xd800&&codeCaractère<=0xdbff){unsigned partieBas=unitéChaîne(&positionDonnées,décalageFin);if(partieBas<0xdc00||partieBas>0xdfff){estInvalide=1;break;}codeCaractère=0x10000+((codeCaractère-0xd800)<<10)+partieBas-0xdc00;}
        else if(codeCaractère>=0xdc00&&codeCaractère<=0xdfff){estInvalide=1;break;}
        if(!codeCaractère){printf("jaot: embedded NUL string needs JVM mode\n");estInvalide=1;break;}
        if(codeCaractère<128)émettreValeur("%u,",codeCaractère);
        else{unsigned nombreÉlémentsÉlémentListe=codeCaractère<2048?2:codeCaractère<65536?3:4;émettreValeur("%u,",(nombreÉlémentsÉlémentListe==2?0xc0:nombreÉlémentsÉlémentListe==3?0xe0:0xf0)|(codeCaractère>>(6*(nombreÉlémentsÉlémentListe-1))));for(unsigned indiceOrdinal=nombreÉlémentsÉlémentListe-1;indiceOrdinal;indiceOrdinal--)émettreValeur("%u,",0x80|((codeCaractère>>(6*(indiceOrdinal-1)))&63));}
    }émettreValeur("0};\n");
}
const char *sourceCompilationJavaAnticipée(const char*nom){
    size_t nombreÉlémentsÉlémentListe=strlen(nom);
    if(nombreÉlémentsÉlémentListe>4&&!strcmp(nom+nombreÉlémentsÉlémentListe-4,".jar")){
        if(ouvrirJAR(nom)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char chemin[256];const char*méthodeEntréeÉlément=principalJAR();nombreÉlémentsÉlémentListe=strlen(méthodeEntréeÉlément);if(nombreÉlémentsÉlémentListe+6>=sizeof(chemin))return 0;
        for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)chemin[indiceOrdinal]=méthodeEntréeÉlément[indiceOrdinal]=='.'?'/':méthodeEntréeÉlément[indiceOrdinal];strcpy(chemin+nombreÉlémentsÉlémentListe,".class");int nombreÉlémentsEntréeÉlément=lireJAR(chemin,Données,sizeof(Données));if(nombreÉlémentsEntréeÉlément<0)return 0;longueur=nombreÉlémentsEntréeÉlément;
    }else{intptr_t poignéeFichier=invoquerUtilisateur(3,(uintptr_t)nom,0,0,0,0,0);if(poignéeFichier<0)return 0;intptr_t nombreÉlémentsEntréeÉlément=invoquerUtilisateur(9,poignéeFichier,0,0,0,0,0);if(nombreÉlémentsEntréeÉlément<0||nombreÉlémentsEntréeÉlément>sizeof(Données)){invoquerUtilisateur(4,poignéeFichier,0,0,0,0,0);return 0;}intptr_t nombreÉlémentsReçu=invoquerUtilisateur(2,poignéeFichier,(uintptr_t)Données,nombreÉlémentsEntréeÉlément,0,0,0);invoquerUtilisateur(4,poignéeFichier,0,0,0,0,0);if(nombreÉlémentsReçu!=nombreÉlémentsEntréeÉlément)return 0;longueur=nombreÉlémentsEntréeÉlément;}
    if(analyserEntrée()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    émettreValeur("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned indiceOrdinal=1;indiceOrdinal<réserveConstante&&!estInvalide;indiceOrdinal++)if(listeBalises[indiceOrdinal]==8)constanteChaîne(indiceOrdinal);
    if(estInvalide)return 0;
    int pointEntréeÉlément=-1,valeurInitialValeur=-1;
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsMéthodeDéclaré;indiceOrdinal++)if(!valeurUnicode(méthodesDéclaré[indiceOrdinal].nom,"<init>")){
        int résultat,nombreÉlémentsEntréeÉlément=entréeÉlémentDescripteur(méthodesDéclaré[indiceOrdinal].donnéesDescripteur,&résultat);if(nombreÉlémentsEntréeÉlément<0)return 0;émettreValeur("static W m%u(",indiceOrdinal);for(int ordinalInterne=0;ordinalInterne<nombreÉlémentsEntréeÉlément;ordinalInterne++)émettreValeur(ordinalInterne?",W":"W");if(!nombreÉlémentsEntréeÉlément)émettreValeur("void");émettreValeur(");\n");
        if(valeurUnicode(méthodesDéclaré[indiceOrdinal].nom,"main")&&valeurUnicode(méthodesDéclaré[indiceOrdinal].donnéesDescripteur,"([Ljava/lang/String;)V")&&(méthodesDéclaré[indiceOrdinal].bitsConfiguration&9)==9)pointEntréeÉlément=indiceOrdinal;
        if(valeurUnicode(méthodesDéclaré[indiceOrdinal].nom,"<clinit>"))valeurInitialValeur=indiceOrdinal;
    }
    if(pointEntréeÉlément<0)return 0;for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsMéthodeDéclaré&&!estInvalide;indiceOrdinal++)compilerMéthode(indiceOrdinal);
    émettreValeur("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsChampDéclaré;indiceOrdinal++)if(constanteChamp[indiceOrdinal]){
        unsigned codeCaractère=constanteChamp[indiceOrdinal];if(codeCaractère>=réserveConstante)return 0;
        if(listeBalises[codeCaractère]==3)émettreValeur("fields[%u]=%uU;",indiceOrdinal,valeurPremier[codeCaractère]);else if(listeBalises[codeCaractère]==8)émettreValeur("fields[%u]=(W)k%u;",indiceOrdinal,codeCaractère);else return 0;
    }
    if(valeurInitialValeur>=0)émettreValeur("m%d();",valeurInitialValeur);émettreValeur("m%d((W)a);return 0;}\n",pointEntréeÉlément);
    return estInvalide?0:texte;
}

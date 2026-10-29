/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "invoquer.h"
#include "ABIFichier.h"
#define capacitéÉditeur 16384
static unsigned char texte[capacitéÉditeur],donnéesAnnulerModification[capacitéÉditeur],donnéesCopié[capacitéÉditeur],donnéesRésultat[1024];
static int longueur,valeurIndice,entréeÉlémentSommet,côtéGauche,changéÉtait,insérer,longueurAnnulerModification,côtéSupérieur,changementsAnnulerModification,annulerModificationDétenir,copierLongueur,capacitéUtilisé,colonnes=68,nombreÉlémentsRangée=19;
static char nomEntréeÉlémentFichier[64],commande[128],trouverEntréeÉlément[128];
static const char *texteNotification="NORMAL  i:insert  :w:save  :q:quit";
static unsigned toucheEnAttente;
static int catégorieAide,imageÉtatValeur,fileAttenteÉtatValeur;
static void viderTampon(void){if(capacitéUtilisé){invoquerUtilisateur(1,1,(uintptr_t)donnéesRésultat,capacitéUtilisé,0,0,0);capacitéUtilisé=0;}}
static void donnéesOctet(unsigned codeCaractère){if(imageÉtatValeur){if((codeCaractère&192)!=128){fileAttenteÉtatValeur+=codeCaractère>=196?2:1;}if(fileAttenteÉtatValeur>=colonnes)return;}if(capacitéUtilisé==(int)sizeof(donnéesRésultat))viderTampon();donnéesRésultat[capacitéUtilisé++]=codeCaractère;}
static void émettreTexte(const char *donnéesChaîne){while(*donnéesChaîne)donnéesOctet((unsigned char)*donnéesChaîne++);}
static void valeurNumérique(unsigned nombreÉlémentsÉlémentListe){char valeurDeuxième[12];int indiceOrdinal=0;do{valeurDeuxième[indiceOrdinal++]='0'+nombreÉlémentsÉlémentListe%10;nombreÉlémentsÉlémentListe/=10;}while(nombreÉlémentsÉlémentListe);while(indiceOrdinal)donnéesOctet(valeurDeuxième[--indiceOrdinal]);}
static void valeurDéplacer(int positionRangée,int positionColonne){émettreTexte("\033[");valeurNumérique(positionRangée);donnéesOctet(';');valeurNumérique(positionColonne);donnéesOctet('H');}
static int précédentÉlément(int positionDonnées){if(positionDonnées){positionDonnées--;while(positionDonnées>0&&(texte[positionDonnées]&192)==128)positionDonnées--;}return positionDonnées;}
static int élémentListeSuivant(int positionDonnées){if(positionDonnées<longueur){positionDonnées++;while(positionDonnées<longueur&&(texte[positionDonnées]&192)==128)positionDonnées++;}return positionDonnées;}
static int lancer(int positionDonnées){while(positionDonnées>0&&texte[positionDonnées-1]!='\n')positionDonnées--;return positionDonnées;}
static int décalageFin(int positionDonnées){while(positionDonnées<longueur&&texte[positionDonnées]!='\n')positionDonnées++;return positionDonnées;}
static int valeurLargeur(unsigned codeCaractère){return codeCaractère>=196?2:1;}
static int colonne(int positionDonnées){int codeCaractère=0;for(int indiceOrdinal=lancer(positionDonnées);indiceOrdinal<positionDonnées;indiceOrdinal=élémentListeSuivant(indiceOrdinal))codeCaractère+=texte[indiceOrdinal]=='\t'?4-codeCaractère%4:valeurLargeur(texte[indiceOrdinal]);return codeCaractère;}
static void pointContrôle(void){for(int indiceOrdinal=0;indiceOrdinal<longueur;indiceOrdinal++)donnéesAnnulerModification[indiceOrdinal]=texte[indiceOrdinal];longueurAnnulerModification=longueur;côtéSupérieur=valeurIndice;changementsAnnulerModification=changéÉtait;annulerModificationDétenir=1;}
static void effacerContenuOctets(int positionDépart,int positionArrivée){pointContrôle();for(int indiceOrdinal=positionArrivée;indiceOrdinal<longueur;indiceOrdinal++)texte[positionDépart+indiceOrdinal-positionArrivée]=texte[indiceOrdinal];longueur-=positionArrivée-positionDépart;valeurIndice=positionDépart;changéÉtait=1;}
static int ajouterFinValeur(const unsigned char *donnéesChaîne,int nombreÉlémentsÉlémentListe){if(nombreÉlémentsÉlémentListe>capacitéÉditeur-longueur){texteNotification="File full (16384 bytes)";return 0;}pointContrôle();for(int indiceOrdinal=longueur-1;indiceOrdinal>=valeurIndice;indiceOrdinal--)texte[indiceOrdinal+nombreÉlémentsÉlémentListe]=texte[indiceOrdinal];for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)texte[valeurIndice+indiceOrdinal]=donnéesChaîne[indiceOrdinal];longueur+=nombreÉlémentsÉlémentListe;valeurIndice+=nombreÉlémentsÉlémentListe;changéÉtait=1;return 1;}
static void vertical(int valeurDifférence){int positionColonne=colonne(valeurIndice),positionDonnées=lancer(valeurIndice);if(valeurDifférence<0){if(!positionDonnées)return;positionDonnées=lancer(positionDonnées-1);}else{positionDonnées=décalageFin(positionDonnées);if(positionDonnées==longueur)return;positionDonnées++;}int codeCaractère=0;while(positionDonnées<longueur&&texte[positionDonnées]!='\n'&&codeCaractère<positionColonne){codeCaractère+=texte[positionDonnées]=='\t'?4-codeCaractère%4:valeurLargeur(texte[positionDonnées]);positionDonnées=élémentListeSuivant(positionDonnées);}valeurIndice=positionDonnées;}
static void dessinerÉcran(void){
    if(valeurIndice>longueur)valeurIndice=longueur;if(entréeÉlémentSommet>valeurIndice)entréeÉlémentSommet=lancer(valeurIndice);entréeÉlémentSommet=lancer(entréeÉlémentSommet);
    int positionRangée=0;for(int indiceOrdinal=entréeÉlémentSommet;indiceOrdinal<valeurIndice;indiceOrdinal++)if(texte[indiceOrdinal]=='\n')positionRangée++;
    while(positionRangée>=nombreÉlémentsRangée-1){entréeÉlémentSommet=décalageFin(entréeÉlémentSommet);if(entréeÉlémentSommet<longueur)entréeÉlémentSommet++;positionRangée--;}
    int positionColonne=colonne(valeurIndice);if(positionColonne<côtéGauche)côtéGauche=positionColonne;if(positionColonne-côtéGauche>=colonnes-1)côtéGauche=positionColonne-colonnes+2;
    émettreTexte("\033[?25l");int positionDonnées=entréeÉlémentSommet;
    for(int valeurRetourné=0;valeurRetourné<nombreÉlémentsRangée-1;valeurRetourné++){
        valeurDéplacer(valeurRetourné+1,1);émettreTexte("\033[0m\033[2K");int codeCaractère=0,estDessiné=0;
        if(positionDonnées>=longueur&&valeurRetourné>positionRangée){émettreTexte("\033[90m~\033[0m");continue;}
        while(positionDonnées<longueur&&texte[positionDonnées]!='\n'){
            int décalageSuivant=élémentListeSuivant(positionDonnées),valeurLargeurDemandé=texte[positionDonnées]=='\t'?4-codeCaractère%4:valeurLargeur(texte[positionDonnées]);
            if(codeCaractère>=côtéGauche&&codeCaractère-côtéGauche+valeurLargeurDemandé<colonnes){
                if(texte[positionDonnées]=='\t'){for(int ordinalInterne=0;ordinalInterne<valeurLargeurDemandé;ordinalInterne++)donnéesOctet(' ');}else if(texte[positionDonnées]<32||texte[positionDonnées]==127){donnéesOctet('?');}else for(int ordinalInterne=positionDonnées;ordinalInterne<décalageSuivant;ordinalInterne++)donnéesOctet(texte[ordinalInterne]);estDessiné+=valeurLargeurDemandé;
            }codeCaractère+=valeurLargeurDemandé;positionDonnées=décalageSuivant;
        }
        (void)estDessiné;if(positionDonnées<longueur)positionDonnées++;
    }
    valeurDéplacer(nombreÉlémentsRangée,1);émettreTexte("\033[7m\033[2K");imageÉtatValeur=1;fileAttenteÉtatValeur=0;émettreTexte(insérer?"INSERT ":"NORMAL ");
    int octetsNom=0;while(nomEntréeÉlémentFichier[octetsNom]&&octetsNom<30)donnéesOctet(nomEntréeÉlémentFichier[octetsNom++]);émettreTexte(changéÉtait?" [+] ":" ");
    émettreTexte("L");int ligne=1;for(int indiceOrdinal=0;indiceOrdinal<valeurIndice;indiceOrdinal++)if(texte[indiceOrdinal]=='\n')ligne++;valeurNumérique(ligne);émettreTexte(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(texteNotification){int nombreÉlémentsÉlémentListe=0;émettreTexte(" | ");while(texteNotification[nombreÉlémentsÉlémentListe]&&nombreÉlémentsÉlémentListe<20)donnéesOctet(texteNotification[nombreÉlémentsÉlémentListe++]);}
    imageÉtatValeur=0;émettreTexte("\033[0m");valeurDéplacer(positionRangée+1,positionColonne-côtéGauche+1);émettreTexte("\033[?25h");viderTampon();
}
static int valeurEnfoncé(void){
    if(toucheEnAttente){int indiceTroisième=toucheEnAttente;toucheEnAttente=0;return indiceTroisième;}
    for(;;){
        int indiceTroisième=invoquerUtilisateur(16,1,0,0,0,0,0);
        unsigned taille=invoquerUtilisateur(16,3,0,0,0,0,0);
        if(colonnes!=(int)(taille&65535)||nombreÉlémentsRangée!=(int)(taille>>16)){
            colonnes=taille&65535;nombreÉlémentsRangée=taille>>16;dessinerÉcran();
            if(catégorieAide){valeurDéplacer(nombreÉlémentsRangée,1);émettreTexte("\033[0m\033[2K");donnéesOctet(catégorieAide);émettreTexte(commande);viderTampon();}
        }
        if(indiceTroisième>=0)return indiceTroisième;
    }
}
static int échappé(void){
    unsigned positionActuel=invoquerUtilisateur(7,0,0,0,0,0,0);int indiceTroisième=-1;
    while((unsigned)invoquerUtilisateur(7,0,0,0,0,0,0)-positionActuel<100){indiceTroisième=invoquerUtilisateur(16,1,0,0,0,0,0);if(indiceTroisième>=0)break;}
    if(indiceTroisième<0)return 27;if(indiceTroisième!='['&&indiceTroisième!='O'){toucheEnAttente=indiceTroisième;return 27;}
    int nombreÉlémentsÉlémentListe=0;for(int indiceOrdinal=0;indiceOrdinal<12;indiceOrdinal++){indiceTroisième=valeurEnfoncé();if(indiceTroisième>='0'&&indiceTroisième<='9'){nombreÉlémentsÉlémentListe=nombreÉlémentsÉlémentListe*10+indiceTroisième-'0';continue;}if(indiceTroisième=='A')return 1001;if(indiceTroisième=='B')return 1002;if(indiceTroisième=='C')return 1003;if(indiceTroisième=='D')return 1004;if(indiceTroisième=='H')return 1005;if(indiceTroisième=='F')return 1006;if(indiceTroisième=='~')return nombreÉlémentsÉlémentListe==3?1007:nombreÉlémentsÉlémentListe==5?1008:nombreÉlémentsÉlémentListe==6?1009:nombreÉlémentsÉlémentListe==1?1005:nombreÉlémentsÉlémentListe==4?1006:27;return 27;}return 27;
}
static int valeurStocker(void){
    int poignéeFichier=ouvrirFichier(nomEntréeÉlémentFichier,ÉcrireLire|ManquantSiCréer|ContenuTronquer,0600);if(poignéeFichier<0){texteNotification="Cannot open for save";return 0;}
    intptr_t nombreÉlémentsÉlémentListe=écrireDonnéesFichier(poignéeFichier,texte,longueur);fermerFichier(poignéeFichier);if(nombreÉlémentsÉlémentListe!=longueur){texteNotification="Write failed";return 0;}changéÉtait=0;texteNotification="Saved (RAM)";return 1;
}
static int égal(const char *valeurPremier,const char *valeurDeuxième){while(*valeurPremier&&*valeurPremier==*valeurDeuxième){valeurPremier++;valeurDeuxième++;}return *valeurPremier==*valeurDeuxième;}
static void trouverSuivant(void){int nombreÉlémentsÉlémentListe=0;while(trouverEntréeÉlément[nombreÉlémentsÉlémentListe])nombreÉlémentsÉlémentListe++;if(!nombreÉlémentsÉlémentListe){texteNotification="No search pattern";return;}for(int indiceOrdinal=1;indiceOrdinal<=longueur;indiceOrdinal++){int positionDonnées=(valeurIndice+indiceOrdinal)%(longueur?longueur:1),ordinalInterne=0;while(ordinalInterne<nombreÉlémentsÉlémentListe&&positionDonnées+ordinalInterne<longueur&&texte[positionDonnées+ordinalInterne]==(unsigned char)trouverEntréeÉlément[ordinalInterne])ordinalInterne++;if(ordinalInterne==nombreÉlémentsÉlémentListe){valeurIndice=positionDonnées;texteNotification="Match";return;}}texteNotification="Pattern not found";}
static int invite(int valeurCatégorie){
    int nombreÉlémentsÉlémentListe=0;commande[0]=0;
    for(;;){valeurDéplacer(nombreÉlémentsRangée,1);émettreTexte("\033[0m\033[2K");donnéesOctet(valeurCatégorie);émettreTexte(commande);viderTampon();catégorieAide=valeurCatégorie;int indiceTroisième=valeurEnfoncé();catégorieAide=0;
        if(indiceTroisième==27||indiceTroisième==3)return 0;if(indiceTroisième==13||indiceTroisième==10)break;
        if(indiceTroisième==127||indiceTroisième==8){if(nombreÉlémentsÉlémentListe){nombreÉlémentsÉlémentListe--;while(nombreÉlémentsÉlémentListe>0&&((unsigned char)commande[nombreÉlémentsÉlémentListe]&192)==128)nombreÉlémentsÉlémentListe--;commande[nombreÉlémentsÉlémentListe]=0;}continue;}
        if(indiceTroisième>=32&&indiceTroisième<256&&nombreÉlémentsÉlémentListe<120){commande[nombreÉlémentsÉlémentListe++]=indiceTroisième;commande[nombreÉlémentsÉlémentListe]=0;}
    }
    if(valeurCatégorie=='/'){for(int indiceOrdinal=0;indiceOrdinal<=nombreÉlémentsÉlémentListe;indiceOrdinal++)trouverEntréeÉlément[indiceOrdinal]=commande[indiceOrdinal];trouverSuivant();return 0;}
    if(égal(commande,"q!"))return 1;
    if(égal(commande,"q")){if(!changéÉtait)return 1;texteNotification="Unsaved: :w or :q!";return 0;}
    if(égal(commande,"wq")||égal(commande,"x"))return valeurStocker();
    if(égal(commande,"w")){valeurStocker();return 0;}
    if(commande[0]=='w'&&commande[1]==' '){int indiceOrdinal=2;while(commande[indiceOrdinal]==' ')indiceOrdinal++;int taille=nombreÉlémentsÉlémentListe-indiceOrdinal;if(taille<1||taille>63){texteNotification="Invalid file name";return 0;}for(int ordinalInterne=0;ordinalInterne<taille;ordinalInterne++)nomEntréeÉlémentFichier[ordinalInterne]=commande[indiceOrdinal+ordinalInterne];nomEntréeÉlémentFichier[taille]=0;valeurStocker();return 0;}
    int ligne=0;for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++){if(commande[indiceOrdinal]<'0'||commande[indiceOrdinal]>'9'){ligne=0;break;}ligne=ligne*10+commande[indiceOrdinal]-'0';if(ligne>16384){ligne=0;break;}}
    if(ligne){valeurIndice=0;while(--ligne&&valeurIndice<longueur){valeurIndice=décalageFin(valeurIndice);if(valeurIndice<longueur)valeurIndice++;}return 0;}
    texteNotification="Unknown vi command";return 0;
}
int démarrerProgrammeUtilisateur(int valeurIgnoré){
    (void)valeurIgnoré;if(nombreÉlémentsArgumentUtilisateur()!=1||argumentUtilisateur(0,nomEntréeÉlémentFichier,sizeof(nomEntréeÉlémentFichier))<0){émettreTexte("Usage: vi FILE\n");viderTampon();return 2;}
    int poignéeFichier=ouvrirFichier(nomEntréeÉlémentFichier,lireValeurSeulement,0);
    if(poignéeFichier>=0){int nombreÉlémentsÉlémentListe=tailleFichier(poignéeFichier);if(nombreÉlémentsÉlémentListe<0||nombreÉlémentsÉlémentListe>capacitéÉditeur){fermerFichier(poignéeFichier);return 1;}longueur=lireDonnéesFichier(poignéeFichier,texte,nombreÉlémentsÉlémentListe);fermerFichier(poignéeFichier);if(longueur!=nombreÉlémentsÉlémentListe)return 1;for(int indiceOrdinal=0;indiceOrdinal<longueur;indiceOrdinal++)if(!texte[indiceOrdinal]){émettreTexte("vi: NUL byte in text file\n");viderTampon();return 1;}}
    else if(numéroErreur!=2){émettreTexte("vi: cannot read file\n");viderTampon();return 1;}
    int couleurAssombrir=invoquerUtilisateur(16,0,0,0,0,0,0);if(couleurAssombrir<0){émettreTexte("vi: use a standalone interactive command\n");viderTampon();return 1;}colonnes=couleurAssombrir&65535;nombreÉlémentsRangée=(unsigned)couleurAssombrir>>16;
    émettreTexte("\033[2J\033[H");viderTampon();
    int partiePréalable=0,programmeTerminerSession=0;
    while(!programmeTerminerSession){dessinerÉcran();int indiceTroisième=valeurEnfoncé();if(indiceTroisième==27)indiceTroisième=échappé();texteNotification=0;
        if(indiceTroisième==1001){vertical(-1);continue;}if(indiceTroisième==1002){vertical(1);continue;}if(indiceTroisième==1003){valeurIndice=élémentListeSuivant(valeurIndice);continue;}if(indiceTroisième==1004){valeurIndice=précédentÉlément(valeurIndice);continue;}
        if(indiceTroisième==1005){valeurIndice=lancer(valeurIndice);continue;}if(indiceTroisième==1006){valeurIndice=décalageFin(valeurIndice);continue;}
        if(indiceTroisième==1008||indiceTroisième==1009){for(int indiceOrdinal=0;indiceOrdinal<nombreÉlémentsRangée-2;indiceOrdinal++)vertical(indiceTroisième==1008?-1:1);continue;}
        if(insérer){
            if(indiceTroisième==27||indiceTroisième==3){insérer=0;continue;}
            if(indiceTroisième==127||indiceTroisième==8){if(valeurIndice)effacerContenuOctets(précédentÉlément(valeurIndice),valeurIndice);continue;}
            if(indiceTroisième==1007){if(valeurIndice<longueur)effacerContenuOctets(valeurIndice,élémentListeSuivant(valeurIndice));continue;}
            if(indiceTroisième==13)indiceTroisième=10;if(indiceTroisième==10||indiceTroisième==9||(indiceTroisième>=32&&indiceTroisième<256)){
                unsigned char valeurDeuxième[4];valeurDeuxième[0]=indiceTroisième;int nombreÉlémentsÉlémentListe=indiceTroisième<128?1:indiceTroisième>=0xc2&&indiceTroisième<0xe0?2:indiceTroisième<0xf0?3:indiceTroisième<=0xf4?4:0;
                if(!nombreÉlémentsÉlémentListe){texteNotification="Invalid UTF-8";continue;}int valide=1;for(int indiceOrdinal=1;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++){int codeCaractère=valeurEnfoncé();if(codeCaractère<128||codeCaractère>191){toucheEnAttente=codeCaractère;valide=0;break;}valeurDeuxième[indiceOrdinal]=codeCaractère;}
                if(valide)ajouterFinValeur(valeurDeuxième,nombreÉlémentsÉlémentListe);
            }continue;
        }
        if(partiePréalable){int positionDonnées=partiePréalable;partiePréalable=0;if(positionDonnées=='g'&&indiceTroisième=='g'){valeurIndice=0;continue;}if(positionDonnées=='Z'&&indiceTroisième=='Z'){programmeTerminerSession=valeurStocker();continue;}if((positionDonnées=='d'&&indiceTroisième=='d')||(positionDonnées=='y'&&indiceTroisième=='y')){int valeurPremier=lancer(valeurIndice),valeurDeuxième=décalageFin(valeurIndice);if(valeurDeuxième<longueur)valeurDeuxième++;copierLongueur=valeurDeuxième-valeurPremier;for(int indiceOrdinal=0;indiceOrdinal<copierLongueur;indiceOrdinal++)donnéesCopié[indiceOrdinal]=texte[valeurPremier+indiceOrdinal];if(positionDonnées=='d')effacerContenuOctets(valeurPremier,valeurDeuxième);continue;}}
        if(indiceTroisième=='i'){insérer=1;continue;}if(indiceTroisième=='a'){if(valeurIndice<décalageFin(valeurIndice))valeurIndice=élémentListeSuivant(valeurIndice);insérer=1;continue;}
        if(indiceTroisième=='I'){valeurIndice=lancer(valeurIndice);insérer=1;continue;}if(indiceTroisième=='A'){valeurIndice=décalageFin(valeurIndice);insérer=1;continue;}
        if(indiceTroisième=='o'||indiceTroisième=='O'){unsigned char finLigne='\n';valeurIndice=indiceTroisième=='o'?décalageFin(valeurIndice):lancer(valeurIndice);if(ajouterFinValeur(&finLigne,1)){if(indiceTroisième=='O')valeurIndice--;insérer=1;}continue;}
        if(indiceTroisième=='h'){valeurIndice=précédentÉlément(valeurIndice);continue;}if(indiceTroisième=='l'){valeurIndice=élémentListeSuivant(valeurIndice);continue;}if(indiceTroisième=='j'){vertical(1);continue;}if(indiceTroisième=='k'){vertical(-1);continue;}
        if(indiceTroisième=='0'){valeurIndice=lancer(valeurIndice);continue;}if(indiceTroisième=='$'){valeurIndice=décalageFin(valeurIndice);continue;}if(indiceTroisième=='G'){valeurIndice=lancer(longueur);continue;}
        if(indiceTroisième=='g'||indiceTroisième=='d'||indiceTroisième=='y'||indiceTroisième=='Z'){partiePréalable=indiceTroisième;continue;}
        if(indiceTroisième=='x'||indiceTroisième==1007){if(valeurIndice<longueur)effacerContenuOctets(valeurIndice,élémentListeSuivant(valeurIndice));continue;}
        if(indiceTroisième=='p'&&copierLongueur){valeurIndice=décalageFin(valeurIndice);if(valeurIndice<longueur)valeurIndice++;ajouterFinValeur(donnéesCopié,copierLongueur);continue;}
        if(indiceTroisième=='u'&&annulerModificationDétenir){for(int indiceOrdinal=0;indiceOrdinal<capacitéÉditeur;indiceOrdinal++){unsigned char valeurDeuxième=texte[indiceOrdinal];texte[indiceOrdinal]=donnéesAnnulerModification[indiceOrdinal];donnéesAnnulerModification[indiceOrdinal]=valeurDeuxième;}int nombreÉlémentsÉlémentListe=longueur;longueur=longueurAnnulerModification;longueurAnnulerModification=nombreÉlémentsÉlémentListe;nombreÉlémentsÉlémentListe=valeurIndice;valeurIndice=côtéSupérieur;côtéSupérieur=nombreÉlémentsÉlémentListe;nombreÉlémentsÉlémentListe=changéÉtait;changéÉtait=changementsAnnulerModification;changementsAnnulerModification=nombreÉlémentsÉlémentListe;continue;}
        if(indiceTroisième==':'||indiceTroisième=='/'){programmeTerminerSession=invite(indiceTroisième);continue;}if(indiceTroisième=='n'){trouverSuivant();continue;}
    }
    émettreTexte("\033[0m\033[?25h\033[2J\033[H");viderTampon();invoquerUtilisateur(16,2,0,0,0,0,0);return 0;
}

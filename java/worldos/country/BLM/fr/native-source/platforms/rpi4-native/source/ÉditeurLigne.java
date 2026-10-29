// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Insertion, suppression, flèches, historique et complétion par Tab respectent les frontières d’octets UTF-8. */
public final class ÉditeurLigne {
    static boolean ligneCommande;
    static int[] enregistrementJournal = new int[16 * 1024], longueurJournal = new int[16], valeurStocker = new int[4096], candidat = new int[64];
    static int nombreÉlémentsJournal, finEnregistrementJournal, chercherValeur, longueurStocké, taille, valeurCurseur, nombreÉlémentsCandidat, longueurCandidat, démarrerFenêtre;
    static boolean afficherPositionHorizontal;
    static String listeCommandes = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd interpréteurCommandesSécuriser PrésenterDistant run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] candidatCommande = new int[128];
    static void ajouterCandidatCommande(String listeEntréeÉlément, int démarrerPosition, int positionFin, int longueurEntrée) {
        int nombreÉlémentsOctet=0;
        for(int indicePosition=démarrerPosition;indicePosition<positionFin;indicePosition++) {
            int codeCaractère=listeEntréeÉlément.charAt(indicePosition);
            if(codeCaractère>=0xd800 && codeCaractère<=0xdbff && indicePosition+1<positionFin)codeCaractère=0x10000+((codeCaractère-0xd800)<<10)+listeEntréeÉlément.charAt(++indicePosition)-0xdc00;
            int nombre=codeCaractère<128?1:codeCaractère<2048?2:codeCaractère<65536?3:4;
            if(nombreÉlémentsOctet+nombre>62)return;
            for(int valeurSéquence=nombre-1;valeurSéquence>=0;valeurSéquence--)candidatCommande[nombreÉlémentsOctet++]=nombre==1?codeCaractère:valeurSéquence==nombre-1?(nombre==2?0xc0:nombre==3?0xe0:0xf0)|(codeCaractère>>(6*valeurSéquence)):0x80|((codeCaractère>>(6*valeurSéquence))&63);
        }
        if(nombreÉlémentsOctet<longueurEntrée)return;
        for(int indicePosition=0;indicePosition<longueurEntrée;indicePosition++)if(candidatCommande[indicePosition]!=InterpréteurCommandes.ligne[indicePosition])return;
        nombreÉlémentsCandidat++;longueurCandidat=nombreÉlémentsOctet+1;
        for(int indicePosition=0;indicePosition<nombreÉlémentsOctet;indicePosition++)candidat[indicePosition]=candidatCommande[indicePosition];candidat[nombreÉlémentsOctet]=' ';
    }
    static int valeurAvantCôté(int lireCurseur) { if (lireCurseur > 0) { lireCurseur--; while (lireCurseur > 0 && (InterpréteurCommandes.ligne[lireCurseur] & 192) == 128) lireCurseur--; } return lireCurseur; }
    static int valeurRetourArrièreCôté(int lireCurseur) { if (lireCurseur < taille) { lireCurseur++; while (lireCurseur < taille && (InterpréteurCommandes.ligne[lireCurseur] & 192) == 128) lireCurseur++; } return lireCurseur; }
    static int étendueLargeur(int démarrerPosition, int indiceValeurDestination) {
        int cellules = 0;
        for (int indiceBoucle = démarrerPosition; indiceBoucle < indiceValeurDestination; indiceBoucle++) { int donnéesOctet = InterpréteurCommandes.ligne[indiceBoucle]; if ((donnéesOctet & 192) == 128) continue; cellules += donnéesOctet >= 196 ? 2 : 1; }
        return cellules;
    }
    static void valeurRéessayer() {
        EntréeSortieTerminal.écrire("\r\u001b[2K");
        EntréeSortieTerminal.écrire(ligneCommande ? "jkoros-native> " : "edit> ");
        lignesVisible();
    }
    // Se déplacer horizontalement dans une même ligne physique. Le réaffichage d’une commande longue ne doit pas effacer la sortie située au-dessus.
    static int largeurVisible() { int colonnes = CarteMatérielle.terminal(13) & 65535; return colonnes - (ligneCommande ? 18 : 9); }
    static void lignesVisible() {
        if (valeurCurseur < démarrerFenêtre) démarrerFenêtre = valeurCurseur;
        while (étendueLargeur(démarrerFenêtre, valeurCurseur) > largeurVisible()) démarrerFenêtre = valeurRetourArrièreCôté(démarrerFenêtre);
        int positionFin = démarrerFenêtre;
        while (positionFin < taille && étendueLargeur(démarrerFenêtre, valeurRetourArrièreCôté(positionFin)) <= largeurVisible()) positionFin = valeurRetourArrièreCôté(positionFin);
        EntréeSortieTerminal.écrire("\r\u001b["); EntréeSortieTerminal.nombre(ligneCommande ? 16 : 7); EntréeSortieTerminal.écrire("G\u001b[K");
        if (démarrerFenêtre > 0) EntréeSortieTerminal.Caractères('<');
        for (int indiceBoucle = démarrerFenêtre; indiceBoucle < positionFin; indiceBoucle++) CarteMatérielle.écrireSériel(InterpréteurCommandes.ligne[indiceBoucle]);
        EntréeSortieTerminal.Caractères(positionFin < taille ? '>' : ' ');
        EntréeSortieTerminal.écrire("\u001b["); EntréeSortieTerminal.nombre(étendueLargeur(valeurCurseur, positionFin) + 1); EntréeSortieTerminal.Caractères('D');
        afficherPositionHorizontal = démarrerFenêtre > 0 || positionFin < taille || étendueLargeur(0, taille) > largeurVisible();
    }
    static void ajouterFinJournal() {
        if (!ligneCommande || taille == 0 || taille > 1024) return;
        if (nombreÉlémentsJournal > 0) {
            int positionDernier = (finEnregistrementJournal + 15) % 16; boolean estMême = longueurJournal[positionDernier] == taille;
            for (int indiceBoucle = 0; estMême && indiceBoucle < taille; indiceBoucle++) if (enregistrementJournal[positionDernier * 1024 + indiceBoucle] != InterpréteurCommandes.ligne[indiceBoucle]) estMême = false;
            if (estMême) return;
        }
        longueurJournal[finEnregistrementJournal] = taille; for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) enregistrementJournal[finEnregistrementJournal * 1024 + indiceBoucle] = InterpréteurCommandes.ligne[indiceBoucle];
        finEnregistrementJournal = (finEnregistrementJournal + 1) % 16; if (nombreÉlémentsJournal < 16) nombreÉlémentsJournal++;
    }
    static void mouvementJournal(int valeurVariation) {
        if (!ligneCommande) return;
        if (chercherValeur == 0 && valeurVariation > 0) { longueurStocké = taille; for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) valeurStocker[indiceBoucle] = InterpréteurCommandes.ligne[indiceBoucle]; }
        int positionSuivant = chercherValeur + valeurVariation; if (positionSuivant < 0 || positionSuivant > nombreÉlémentsJournal) return; chercherValeur = positionSuivant;
        if (chercherValeur == 0) { taille = longueurStocké; for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) InterpréteurCommandes.ligne[indiceBoucle] = valeurStocker[indiceBoucle]; }
        else { int emplacementPréservé = (finEnregistrementJournal + 16 - chercherValeur) % 16; taille = longueurJournal[emplacementPréservé]; for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) InterpréteurCommandes.ligne[indiceBoucle] = enregistrementJournal[emplacementPréservé * 1024 + indiceBoucle]; }
        valeurCurseur = taille; valeurRéessayer();
    }
    static void afficherJournal() {
        for (int nombreÉlémentsEntréeÉlément = 0; nombreÉlémentsEntréeÉlément < nombreÉlémentsJournal; nombreÉlémentsEntréeÉlément++) {
            int emplacementPréservé = (finEnregistrementJournal + 16 - nombreÉlémentsJournal + nombreÉlémentsEntréeÉlément) % 16; EntréeSortieTerminal.nombre(nombreÉlémentsEntréeÉlément + 1); EntréeSortieTerminal.écrire("  ");
            for (int indiceBoucle = 0; indiceBoucle < longueurJournal[emplacementPréservé]; indiceBoucle++) CarteMatérielle.écrireSériel(enregistrementJournal[emplacementPréservé * 1024 + indiceBoucle]); EntréeSortieTerminal.Caractères(10);
        }
    }
    static void ajouterCandidat(int[] tableauDonnées, int démarrerPosition, int nombreÉlémentsEntréeÉlément, int préfixe, int nombreÉlémentsTotal, boolean numéroRépertoire) {
        if (nombreÉlémentsEntréeÉlément < nombreÉlémentsTotal || nombreÉlémentsEntréeÉlément > 62) return;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsTotal; indiceBoucle++) if (tableauDonnées[démarrerPosition + indiceBoucle] != InterpréteurCommandes.ligne[préfixe + indiceBoucle]) return;
        nombreÉlémentsCandidat++; longueurCandidat = nombreÉlémentsEntréeÉlément + 1;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) candidat[indiceBoucle] = tableauDonnées[démarrerPosition + indiceBoucle]; candidat[nombreÉlémentsEntréeÉlément] = numéroRépertoire ? '/' : ' ';
    }
    static void valeurAchevé() {
        if (!ligneCommande || valeurCurseur != taille) return;
        int pointInitial = taille; while (pointInitial > 0 && InterpréteurCommandes.ligne[pointInitial - 1] != ' ') pointInitial--;
        for (int indiceBoucle = pointInitial; indiceBoucle < taille; indiceBoucle++) if (InterpréteurCommandes.ligne[indiceBoucle] == '/' || InterpréteurCommandes.ligne[indiceBoucle] == '"' || InterpréteurCommandes.ligne[indiceBoucle] == 39 || InterpréteurCommandes.ligne[indiceBoucle] == '\\') return;
        nombreÉlémentsCandidat = 0; int nombreÉlémentsEntréeÉlément = taille - pointInitial;
        if (pointInitial == 0) {
            for(int indiceListe=0;indiceListe<2;indiceListe++) {
                String listeEntréeÉlément=indiceListe==0?listeCommandes:CommandesAdministration.motAchevé();
                int lireCurseur=0;
                while(lireCurseur<listeEntréeÉlément.length()) {
                    int positionFin=lireCurseur;while(positionFin<listeEntréeÉlément.length() && listeEntréeÉlément.charAt(positionFin)!=' ')positionFin++;
                    ajouterCandidatCommande(listeEntréeÉlément,lireCurseur,positionFin,nombreÉlémentsEntréeÉlément);lireCurseur=positionFin+1;
                }
            }
        } else {
            FichiersMémoire.démarrerChemin(1); FichiersMémoire.octetChemin(0, '.'); FichiersMémoire.normaliserValeur();
            for (int indiceBoucle = 0; indiceBoucle < FichiersMémoire.nombreÉlémentsFichier; indiceBoucle++) {
                int démarrerPosition = FichiersMémoire.démarrerEntréeÉlément(FichiersMémoire.nom, indiceBoucle * 64, FichiersMémoire.longueurNom[indiceBoucle]);
                if (démarrerPosition >= 0) ajouterCandidat(FichiersMémoire.nom, indiceBoucle * 64 + démarrerPosition, FichiersMémoire.longueurNom[indiceBoucle] - démarrerPosition, pointInitial, nombreÉlémentsEntréeÉlément, false);
            }
            for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) {
                int démarrerPosition = FichiersMémoire.démarrerEntréeÉlément(FichiersMémoire.nomRépertoire, indiceBoucle * 64, FichiersMémoire.longueurRépertoire[indiceBoucle]);
                if (démarrerPosition >= 0) ajouterCandidat(FichiersMémoire.nomRépertoire, indiceBoucle * 64 + démarrerPosition, FichiersMémoire.longueurRépertoire[indiceBoucle] - démarrerPosition, pointInitial, nombreÉlémentsEntréeÉlément, true);
            }
        }
        if (nombreÉlémentsCandidat != 1) { CarteMatérielle.écrireSériel(7); return; }
        for (int indiceBoucle = nombreÉlémentsEntréeÉlément; indiceBoucle < longueurCandidat && taille < InterpréteurCommandes.ligne.length - 1; indiceBoucle++) {
            if (candidat[indiceBoucle] == ' ' && indiceBoucle != longueurCandidat - 1) InterpréteurCommandes.ligne[taille++] = '\\';
            InterpréteurCommandes.ligne[taille++] = candidat[indiceBoucle];
        }
        valeurCurseur = taille; valeurRéessayer();
    }
    static int lireÉchapper() {
        int pointInitial = CarteMatérielle.millisecondes();
        while (CarteMatérielle.millisecondes() - pointInitial < 80) { int donnéesOctet = CarteMatérielle.lireSériel(); if (donnéesOctet >= 0) return donnéesOctet; CarteMatérielle.céderProcesseur(); }
        return -1;
    }
    static void valeurÉchapper() {
        int premier = lireÉchapper(); if (premier != '[' && premier != 'O') return;
        int nombreÉlémentsEntréeÉlément = 0, positionFin = -1;
        for (int indiceBoucle = 0; indiceBoucle < 12; indiceBoucle++) { int donnéesOctet = lireÉchapper(); if (donnéesOctet < 0) return; if (donnéesOctet >= '0' && donnéesOctet <= '9') nombreÉlémentsEntréeÉlément = nombreÉlémentsEntréeÉlément * 10 + donnéesOctet - '0'; else { positionFin = donnéesOctet; break; } }
        if (positionFin == 'A') mouvementJournal(1);
        else if (positionFin == 'B') mouvementJournal(-1);
        else if (positionFin == 'C') { valeurCurseur = valeurRetourArrièreCôté(valeurCurseur); valeurRéessayer(); }
        else if (positionFin == 'D') { valeurCurseur = valeurAvantCôté(valeurCurseur); valeurRéessayer(); }
        else if (positionFin == 'H' || positionFin == '~' && (nombreÉlémentsEntréeÉlément == 1 || nombreÉlémentsEntréeÉlément == 7)) { valeurCurseur = 0; valeurRéessayer(); }
        else if (positionFin == 'F' || positionFin == '~' && (nombreÉlémentsEntréeÉlément == 4 || nombreÉlémentsEntréeÉlément == 8)) { valeurCurseur = taille; valeurRéessayer(); }
        else if (positionFin == '~' && nombreÉlémentsEntréeÉlément == 3 && valeurCurseur < taille) {
            int positionSuivant = valeurRetourArrièreCôté(valeurCurseur); for (int indiceBoucle = positionSuivant; indiceBoucle < taille; indiceBoucle++) InterpréteurCommandes.ligne[indiceBoucle - positionSuivant + valeurCurseur] = InterpréteurCommandes.ligne[indiceBoucle]; taille -= positionSuivant - valeurCurseur; valeurRéessayer();
        }
        else if (positionFin == '~' && (nombreÉlémentsEntréeÉlément == 5 || nombreÉlémentsEntréeÉlément == 6)) CarteMatérielle.terminal(nombreÉlémentsEntréeÉlément == 5 ? 5 : 6);
        else if (positionFin == '~' && nombreÉlémentsEntréeÉlément == 24 && ligneCommande) { InterpréteurCommandes.terminal(true); }
    }
    static int lire() {
        if (!sessionFenêtre.lireContinuation) { taille = valeurCurseur = chercherValeur = démarrerFenêtre = 0; afficherPositionHorizontal = false; }
        else { sessionFenêtre.lireContinuation = false; valeurRéessayer(); } boolean débordement = false;
        while (true) {
            int donnéesOctet = CarteMatérielle.lireSériel(); if (donnéesOctet == -4096) return -3;
            if (CarteMatérielle.terminal(14) != 0) valeurRéessayer(); if (donnéesOctet < 0) { CarteMatérielle.céderProcesseur(); continue; }
            if (donnéesOctet == 10 && InterpréteurCommandes.lignePrécédentÉlément) { InterpréteurCommandes.lignePrécédentÉlément = false; continue; } InterpréteurCommandes.lignePrécédentÉlément = donnéesOctet == 13;
            if (donnéesOctet == 27) { valeurÉchapper(); continue; }
            if (donnéesOctet == 3) { EntréeSortieTerminal.écrire("^C\n"); return -1; }
            if (donnéesOctet == 4 && taille == 0 && ligneCommande) { if (CarteMatérielle.terminal(2) != 0) InterpréteurCommandes.terminal(true); return -1; }
            if (donnéesOctet == 13 || donnéesOctet == 10) { EntréeSortieTerminal.Caractères(10); if (!débordement) ajouterFinJournal(); return débordement ? -2 : taille; }
            if (donnéesOctet == 9 && ligneCommande) { valeurAchevé(); continue; }
            if (donnéesOctet == 1 || donnéesOctet == 5) { valeurCurseur = donnéesOctet == 1 ? 0 : taille; valeurRéessayer(); continue; }
            if (donnéesOctet == 8 || donnéesOctet == 127 || donnéesOctet == 21) {
                if (donnéesOctet == 21) { for (int indiceBoucle = valeurCurseur; indiceBoucle < taille; indiceBoucle++) InterpréteurCommandes.ligne[indiceBoucle - valeurCurseur] = InterpréteurCommandes.ligne[indiceBoucle]; taille -= valeurCurseur; valeurCurseur = 0; }
                else if (valeurCurseur > 0) { int changerAvant = valeurAvantCôté(valeurCurseur); for (int indiceBoucle = valeurCurseur; indiceBoucle < taille; indiceBoucle++) InterpréteurCommandes.ligne[indiceBoucle - valeurCurseur + changerAvant] = InterpréteurCommandes.ligne[indiceBoucle]; taille -= valeurCurseur - changerAvant; valeurCurseur = changerAvant; }
                valeurRéessayer(); continue;
            }
            if (donnéesOctet == 11) { taille = valeurCurseur; valeurRéessayer(); continue; }
            if (donnéesOctet < 32 && donnéesOctet != 9) continue;
            if (taille == InterpréteurCommandes.ligne.length) { débordement = true; continue; }
            for (int indiceBoucle = taille; indiceBoucle > valeurCurseur; indiceBoucle--) InterpréteurCommandes.ligne[indiceBoucle] = InterpréteurCommandes.ligne[indiceBoucle - 1];
            InterpréteurCommandes.ligne[valeurCurseur++] = donnéesOctet; taille++;
            if (valeurCurseur == taille && !afficherPositionHorizontal && étendueLargeur(0, taille) <= largeurVisible()) CarteMatérielle.écrireSériel(donnéesOctet);
            else if (valeurCurseur == taille) lignesVisible(); else valeurRéessayer();
        }
    }
}

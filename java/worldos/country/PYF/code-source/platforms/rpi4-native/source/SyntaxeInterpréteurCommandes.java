// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Grammaire interactive restreinte. Les tubes s’exécutent séquentiellement ; l’environnement est partagé au sein du même interpréteur. */
public final class SyntaxeInterpréteurCommandes {
    static int[] source = new int[4 * 4096], valeurGenre = new int[4 * 128], lancer = new int[4 * 128], terminaison = new int[4 * 128];
    static int[] nomVariable = new int[16 * 32], donnéesVariable = new int[16 * 256], longueurNom = new int[16], longueurValeur = new int[16];
    static int[] valeurScript = new int[4 * 16384];
    static int valeurÉtatValeur, valeurProfondeur, écrit;
    static boolean estConnexionEnCours, finScript, erreurExtension;
    static boolean caractèreNom(int codeCaractère) { return codeCaractère >= 'a' && codeCaractère <= 'z' || codeCaractère >= 'A' && codeCaractère <= 'Z' || codeCaractère == '_' || codeCaractère >= 128; }
    static boolean suffixeNom(int codeCaractère) { return caractèreNom(codeCaractère) || codeCaractère >= '0' && codeCaractère <= '9'; }
    static void erreur(String texte) { CarteMatérielle.entréeSortieCommuter(0); EntréeSortieTerminal.écrire("commande analyserValeur: "); EntréeSortieTerminal.écrire(texte); EntréeSortieTerminal.Caractères(10); valeurÉtatValeur = 2; }
    static int lire(int nombreÉlémentsEntréeÉlément, int profondeur) {
        int indiceActuel = 0, nombreÉlémentsTotal = 0, positionBase = profondeur * 4096, caractèreSpécial = profondeur * 128;
        while (indiceActuel < nombreÉlémentsEntréeÉlément) {
            while (indiceActuel < nombreÉlémentsEntréeÉlément && (source[positionBase + indiceActuel] == 32 || source[positionBase + indiceActuel] == 9)) indiceActuel++;
            if (indiceActuel == nombreÉlémentsEntréeÉlément || source[positionBase + indiceActuel] == '#') break;
            if (nombreÉlémentsTotal == 128) { erreur("낱말이 너무 많습니다"); return -1; }
            int démarrerPosition = indiceActuel, codeCaractère = source[positionBase + indiceActuel], genreDonnées = 0;
            if (codeCaractère == ';') { genreDonnées = 1; indiceActuel++; }
            else if (codeCaractère == '&') { if (indiceActuel + 1 >= nombreÉlémentsEntréeÉlément || source[positionBase + indiceActuel + 1] != '&') { erreur("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } genreDonnées = 2; indiceActuel += 2; }
            else if (codeCaractère == '|') { indiceActuel++; genreDonnées = indiceActuel < nombreÉlémentsEntréeÉlément && source[positionBase + indiceActuel] == '|' ? 3 : 4; if (genreDonnées == 3) indiceActuel++; }
            else if (codeCaractère == '>') { indiceActuel++; genreDonnées = indiceActuel < nombreÉlémentsEntréeÉlément && source[positionBase + indiceActuel] == '>' ? 6 : 5; if (genreDonnées == 6) indiceActuel++; }
            else if (codeCaractère == '<') { genreDonnées = 7; indiceActuel++; }
            else {
                int guillemet = 0;
                while (indiceActuel < nombreÉlémentsEntréeÉlément) {
                    codeCaractère = source[positionBase + indiceActuel];
                    if (codeCaractère == '`' && guillemet != 39 || codeCaractère == '$' && guillemet != 39 && indiceActuel + 1 < nombreÉlémentsEntréeÉlément && source[positionBase + indiceActuel + 1] == '(') { erreur("commande résultat 치환은 지원하지 않습니다"); return -1; }
                    if (codeCaractère == '\\' && guillemet != 39) { if (++indiceActuel == nombreÉlémentsEntréeÉlément) { erreur("ligne 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } indiceActuel++; continue; }
                    if (codeCaractère == guillemet) { guillemet = 0; indiceActuel++; continue; }
                    if (guillemet == 0 && (codeCaractère == 39 || codeCaractère == 34)) { guillemet = codeCaractère; indiceActuel++; continue; }
                    if (guillemet == 0 && (codeCaractère == 32 || codeCaractère == 9 || codeCaractère == ';' || codeCaractère == '&' || codeCaractère == '|' || codeCaractère == '<' || codeCaractère == '>')) break;
                    indiceActuel++;
                }
                if (guillemet != 0) { erreur("따옴표가 닫히지 않았습니다"); return -1; }
                if (indiceActuel < nombreÉlémentsEntréeÉlément && (source[positionBase + indiceActuel] == '>' || source[positionBase + indiceActuel] == '<')) {
                    boolean valeurNumérique = indiceActuel > démarrerPosition;
                    for (int indiceBoucle = démarrerPosition; indiceBoucle < indiceActuel; indiceBoucle++) if (source[positionBase + indiceBoucle] < '0' || source[positionBase + indiceBoucle] > '9') valeurNumérique = false;
                    if (valeurNumérique) { erreur("번호를 지정한 Fichier entréeÉlémentDescripteur sortieEntrée 전환은 지원하지 않습니다"); return -1; }
                }
            }
            valeurGenre[caractèreSpécial + nombreÉlémentsTotal] = genreDonnées; lancer[caractèreSpécial + nombreÉlémentsTotal] = démarrerPosition; terminaison[caractèreSpécial + nombreÉlémentsTotal] = indiceActuel; nombreÉlémentsTotal++;
        }
        boolean motLexical = false;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsTotal; indiceBoucle++) {
            int donnéesTemporaire = valeurGenre[caractèreSpécial + indiceBoucle];
            if (donnéesTemporaire == 0) motLexical = true;
            else if (donnéesTemporaire >= 5) { if (++indiceBoucle == nombreÉlémentsTotal || valeurGenre[caractèreSpécial + indiceBoucle] != 0) { erreur("sortieEntrée 전환에 Fichier 이름이 필요합니다"); return -1; } }
            else { if (!motLexical || indiceBoucle == nombreÉlémentsTotal - 1 && donnéesTemporaire != 1) { erreur("명령이 빠졌습니다"); return -1; } motLexical = false; }
        }
        if (nombreÉlémentsTotal > 0 && !motLexical && valeurGenre[caractèreSpécial + nombreÉlémentsTotal - 1] != 1) { erreur("명령이 빠졌습니다"); return -1; }
        return nombreÉlémentsTotal;
    }
    static boolean textePlage(int[] tableauDonnées, int démarrerLocal, int nombreÉlémentsEntréeÉlément, String positionCaractère) {
        if (nombreÉlémentsEntréeÉlément != positionCaractère.length()) return false; for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) if (tableauDonnées[démarrerLocal + indiceBoucle] != positionCaractère.charAt(indiceBoucle)) return false; return true;
    }
    static void placerValeur(int donnéesOctet) {
        if (écrit >= InterpréteurCommandes.valeurJeton.length) { if (!erreurExtension) erreur("변수를 펼친 명령이 너무 깁니다"); erreurExtension = true; return; }
        InterpréteurCommandes.valeurJeton[écrit++] = donnéesOctet;
    }
    static void valeurVariable(int[] tableauDonnées, int démarrerPosition, int nombreÉlémentsEntréeÉlément) {
        if (textePlage(tableauDonnées, démarrerPosition, nombreÉlémentsEntréeÉlément, "PWD")) { placerValeur('/'); for (int indiceBoucle = 0; indiceBoucle < FichiersMémoire.longueurActuel; indiceBoucle++) placerValeur(FichiersMémoire.élémentListeActuel[indiceBoucle]); return; }
        if (textePlage(tableauDonnées, démarrerPosition, nombreÉlémentsEntréeÉlément, "HOME")) { placerValeur('/'); return; }
        if (textePlage(tableauDonnées, démarrerPosition, nombreÉlémentsEntréeÉlément, "?")) {
            int valeurDonnées = valeurÉtatValeur, chiffre = 100; boolean possèdeDémarré = false;
            while (chiffre > 0) { int valeurFinalPosition = valeurDonnées / chiffre; if (valeurFinalPosition != 0 || possèdeDémarré || chiffre == 1) { placerValeur('0' + valeurFinalPosition); possèdeDémarré = true; } valeurDonnées %= chiffre; chiffre /= 10; } return;
        }
        for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) if (longueurNom[indiceBoucle] == nombreÉlémentsEntréeÉlément) {
            boolean correspond = true; for (int positionInterne = 0; positionInterne < nombreÉlémentsEntréeÉlément; positionInterne++) if (nomVariable[indiceBoucle * 32 + positionInterne] != tableauDonnées[démarrerPosition + positionInterne]) correspond = false;
            if (correspond) { for (int positionInterne = 0; positionInterne < longueurValeur[indiceBoucle]; positionInterne++) placerValeur(donnéesVariable[indiceBoucle * 256 + positionInterne]); return; }
        }
    }
    static boolean valeurMot(int indiceMotLexical, int profondeur) {
        int lireCurseur = lancer[profondeur * 128 + indiceMotLexical], positionFin = terminaison[profondeur * 128 + indiceMotLexical], positionBase = profondeur * 4096, guillemet = 0;
        if (lireCurseur < positionFin && source[positionBase + lireCurseur] == '~' && (lireCurseur + 1 == positionFin || source[positionBase + lireCurseur + 1] == '/')) { placerValeur('/'); lireCurseur++; }
        while (lireCurseur < positionFin) {
            int codeCaractère = source[positionBase + lireCurseur++];
            if (codeCaractère == guillemet) { guillemet = 0; continue; }
            if (guillemet == 0 && (codeCaractère == 39 || codeCaractère == 34)) { guillemet = codeCaractère; continue; }
            if (codeCaractère == '\\' && guillemet != 39) { int positionSuivant = source[positionBase + lireCurseur++]; if (guillemet == 34 && positionSuivant != '$' && positionSuivant != '"' && positionSuivant != '\\') placerValeur('\\'); placerValeur(positionSuivant); continue; }
            if (codeCaractère == '$' && guillemet != 39 && lireCurseur < positionFin) {
                boolean accolade = source[positionBase + lireCurseur] == '{'; if (accolade) lireCurseur++;
                int débutPosition = lireCurseur;
                if (lireCurseur < positionFin && source[positionBase + lireCurseur] == '?') lireCurseur++;
                else while (lireCurseur < positionFin && suffixeNom(source[positionBase + lireCurseur])) lireCurseur++;
                if (accolade && (lireCurseur == positionFin || source[positionBase + lireCurseur] != '}')) { erreur("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (lireCurseur == débutPosition && !accolade) { placerValeur('$'); continue; }
                valeurVariable(source, positionBase + débutPosition, lireCurseur - débutPosition); if (accolade) lireCurseur++; continue;
            }
            placerValeur(codeCaractère);
        }
        return !erreurExtension;
    }
    static int réglagesEnvironnement(int indiceArgument, boolean supprimer) {
        int démarrerLocal = InterpréteurCommandes.pointInitial[indiceArgument], positionFin = démarrerLocal + InterpréteurCommandes.longueur[indiceArgument], positionÉgalité = démarrerLocal;
        while (positionÉgalité < positionFin && InterpréteurCommandes.valeurJeton[positionÉgalité] != '=') positionÉgalité++;
        int nombreÉlémentsEntréeÉlément = positionÉgalité - démarrerLocal;
        if (nombreÉlémentsEntréeÉlément < 1 || nombreÉlémentsEntréeÉlément > 31 || !caractèreNom(InterpréteurCommandes.valeurJeton[démarrerLocal]) || !supprimer && positionÉgalité == positionFin || positionFin - positionÉgalité - 1 > 255) return 2;
        for (int indiceBoucle = démarrerLocal; indiceBoucle < positionÉgalité; indiceBoucle++) if (!suffixeNom(InterpréteurCommandes.valeurJeton[indiceBoucle])) return 2;
        if (textePlage(InterpréteurCommandes.valeurJeton, démarrerLocal, nombreÉlémentsEntréeÉlément, "PWD") || textePlage(InterpréteurCommandes.valeurJeton, démarrerLocal, nombreÉlémentsEntréeÉlément, "HOME")) return 2;
        int trouvéÉtait = -1, estÉtatValeurVide = -1;
        for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) {
            if (longueurNom[indiceBoucle] == 0) estÉtatValeurVide = indiceBoucle;
            if (longueurNom[indiceBoucle] != nombreÉlémentsEntréeÉlément) continue;
            boolean correspond = true; for (int positionInterne = 0; positionInterne < nombreÉlémentsEntréeÉlément; positionInterne++) if (nomVariable[indiceBoucle * 32 + positionInterne] != InterpréteurCommandes.valeurJeton[démarrerLocal + positionInterne]) correspond = false;
            if (correspond) trouvéÉtait = indiceBoucle;
        }
        if (supprimer) { if (trouvéÉtait >= 0) longueurNom[trouvéÉtait] = 0; return 0; }
        if (trouvéÉtait < 0) trouvéÉtait = estÉtatValeurVide; if (trouvéÉtait < 0) return 1;
        longueurNom[trouvéÉtait] = nombreÉlémentsEntréeÉlément; longueurValeur[trouvéÉtait] = positionFin - positionÉgalité - 1;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) nomVariable[trouvéÉtait * 32 + indiceBoucle] = InterpréteurCommandes.valeurJeton[démarrerLocal + indiceBoucle];
        for (int indiceBoucle = positionÉgalité + 1; indiceBoucle < positionFin; indiceBoucle++) donnéesVariable[trouvéÉtait * 256 + indiceBoucle - positionÉgalité - 1] = InterpréteurCommandes.valeurJeton[indiceBoucle];
        return 0;
    }
    static void afficherEnvironnement() {
        EntréeSortieTerminal.écrire("HOME=/\nPWD="); FichiersMémoire.écrireActuel(); EntréeSortieTerminal.Caractères(10);
        for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) if (longueurNom[indiceBoucle] > 0) {
            for (int positionInterne = 0; positionInterne < longueurNom[indiceBoucle]; positionInterne++) CarteMatérielle.écrireSériel(nomVariable[indiceBoucle * 32 + positionInterne]); EntréeSortieTerminal.Caractères('=');
            for (int positionInterne = 0; positionInterne < longueurValeur[indiceBoucle]; positionInterne++) CarteMatérielle.écrireSériel(donnéesVariable[indiceBoucle * 256 + positionInterne]); EntréeSortieTerminal.Caractères(10);
        }
    }
    static void exécuterCommande(int[] tableauDonnées, int démarrerDéplacement, int nombreÉlémentsEntréeÉlément, int profondeur) {
        if (profondeur >= 4 || nombreÉlémentsEntréeÉlément > 4096) { erreur("commande 파일의 valeurImbrication 또는 ligne longueur 제한을 넘었습니다"); return; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) source[profondeur * 4096 + indiceBoucle] = tableauDonnées[démarrerDéplacement + indiceBoucle];
        int nombreÉlémentsTotal = lire(nombreÉlémentsEntréeÉlément, profondeur); if (nombreÉlémentsTotal < 0) return;
        int lireCurseur = 0, satisfaitCondition = 1;
        while (lireCurseur < nombreÉlémentsTotal) {
            int finGroupe = lireCurseur;
            while (finGroupe < nombreÉlémentsTotal && (valeurGenre[profondeur * 128 + finGroupe] == 0 || valeurGenre[profondeur * 128 + finGroupe] >= 4)) finGroupe++;
            boolean exécuter = satisfaitCondition == 1 || satisfaitCondition == 2 && valeurÉtatValeur == 0 || satisfaitCondition == 3 && valeurÉtatValeur != 0;
            if (exécuter) {
                boolean indiceÉlémentListePrécédentÉlément = false;
                while (lireCurseur < finGroupe) {
                    int positionSuivant = lireCurseur; while (positionSuivant < finGroupe && valeurGenre[profondeur * 128 + positionSuivant] != 4) positionSuivant++;
                    boolean connecterFlux = positionSuivant < finGroupe; int pageEntrée = -1, pageSortie = -1, modeSortant = 0;
                    InterpréteurCommandes.nombreÉlémentsJeton = 0; écrit = 0; erreurExtension = false;
                    for (int indiceBoucle = lireCurseur; indiceBoucle < positionSuivant; indiceBoucle++) {
                        int genreDonnées = valeurGenre[profondeur * 128 + indiceBoucle];
                        if (genreDonnées >= 5) { if (genreDonnées == 7) { if (pageEntrée >= 0) { erreur("valeurEntrée 전환이 겹쳤습니다"); return; } pageEntrée = ++indiceBoucle; } else { if (pageSortie >= 0) { erreur("Sortie 전환이 겹쳤습니다"); return; } pageSortie = ++indiceBoucle; modeSortant = genreDonnées; } continue; }
                        if (InterpréteurCommandes.nombreÉlémentsJeton == 32) { erreur("인수가 너무 많습니다"); return; }
                        int indiceArgument = InterpréteurCommandes.nombreÉlémentsJeton++; InterpréteurCommandes.pointInitial[indiceArgument] = écrit;
                        if (!valeurMot(indiceBoucle, profondeur)) return;
                        InterpréteurCommandes.longueur[indiceArgument] = écrit - InterpréteurCommandes.pointInitial[indiceArgument];
                    }
                    estConnexionEnCours = indiceÉlémentListePrécédentÉlément || connecterFlux || pageEntrée >= 0 || pageSortie >= 0;
                    if (estConnexionEnCours && (InterpréteurCommandes.texteÉgal(0, "vi") || InterpréteurCommandes.texteÉgal(0, "edit") || InterpréteurCommandes.texteÉgal(0, "load") || InterpréteurCommandes.texteÉgal(0, "gui") || InterpréteurCommandes.texteÉgal(0, "terminal") || InterpréteurCommandes.texteÉgal(0, "sh") || InterpréteurCommandes.texteÉgal(0, "source"))) { erreur("interactif 명령과 commande 파일은 sortieEntrée 전환이나 valeurFlux 연결에 쓸 nombre 없습니다"); return; }
                    EntréeSortieInterpréteurCommandes.lancer(indiceÉlémentListePrécédentÉlément, connecterFlux);
                    for (int redirection = 0; redirection < 2; redirection++) {
                        int positionEntréeÉlément = redirection == 0 ? pageEntrée : pageSortie; if (positionEntréeÉlément < 0) continue;
                        int démarrerPosition = écrit; if (!valeurMot(positionEntréeÉlément, profondeur)) { EntréeSortieInterpréteurCommandes.terminaison(); return; }
                        int valeurTraité = FichiersMémoire.démarrerChemin(écrit - démarrerPosition);
                        for (int positionInterne = démarrerPosition; valeurTraité >= 0 && positionInterne < écrit; positionInterne++) valeurTraité = FichiersMémoire.octetChemin(positionInterne - démarrerPosition, InterpréteurCommandes.valeurJeton[positionInterne]);
                        if (valeurTraité >= 0) valeurTraité = FichiersMémoire.ouvrir(redirection == 0 ? 0 : modeSortant == 6 ? 1089 : 577);
                        if (valeurTraité < 0) { EntréeSortieInterpréteurCommandes.terminaison(); InterpréteurCommandes.erreur(valeurTraité); valeurÉtatValeur = 1; return; }
                        if (redirection == 0) EntréeSortieInterpréteurCommandes.fichierEntrée = valeurTraité; else EntréeSortieInterpréteurCommandes.fichierSortie = valeurTraité;
                    }
                    EntréeSortieInterpréteurCommandes.autoriserInteractif = profondeur == 0 && lireCurseur == 0 && positionSuivant == nombreÉlémentsTotal;
                    valeurProfondeur = profondeur; InterpréteurCommandes.résultat = 0; CarteMatérielle.entréeSortieCommuter(1);
                    InterpréteurCommandes.commande();
                    CarteMatérielle.terminal(3);
                    int valeurRetourné = InterpréteurCommandes.résultat, erreurFlux = EntréeSortieInterpréteurCommandes.valeurÉchec;
                    EntréeSortieInterpréteurCommandes.terminaison(); estConnexionEnCours = false;
                    valeurÉtatValeur = erreurFlux < 0 ? 1 : valeurRetourné;
                    if (erreurFlux < 0) { InterpréteurCommandes.erreur(erreurFlux); return; }
                    if (finScript || valeurRetourné == -1005) return;
                    indiceÉlémentListePrécédentÉlément = true; lireCurseur = positionSuivant + 1;
                }
            }
            if (finGroupe < nombreÉlémentsTotal) satisfaitCondition = valeurGenre[profondeur * 128 + finGroupe];
            lireCurseur = finGroupe + 1;
        }
    }
    static void exécuterFichier() {
        if (InterpréteurCommandes.nombreÉlémentsJeton != 2 || valeurProfondeur >= 3) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: sh Fichier (valeurImbrication valeurProfondeur <= 3)\n"); return; }
        int profondeur = valeurProfondeur + 1, valeurTraité = InterpréteurCommandes.chemin(1); if (valeurTraité >= 0) valeurTraité = FichiersMémoire.ouvrir(0);
        if (valeurTraité < 0) { InterpréteurCommandes.erreur(valeurTraité); return; }
        int nombreÉlémentsEntréeÉlément = 0, donnéesOctet;
        while ((donnéesOctet = FichiersMémoire.lire(valeurTraité)) != 256 && donnéesOctet >= 0 && nombreÉlémentsEntréeÉlément < 16384) valeurScript[profondeur * 16384 + nombreÉlémentsEntréeÉlément++] = donnéesOctet;
        FichiersMémoire.fermer(valeurTraité); CarteMatérielle.entréeSortieCommuter(0);
        for (int lireCurseur = 0; lireCurseur < nombreÉlémentsEntréeÉlément && !finScript;) {
            int positionFin = lireCurseur; while (positionFin < nombreÉlémentsEntréeÉlément && valeurScript[profondeur * 16384 + positionFin] != 10) positionFin++;
            int longueurValide = positionFin - lireCurseur; if (longueurValide > 0 && valeurScript[profondeur * 16384 + positionFin - 1] == 13) longueurValide--;
            exécuterCommande(valeurScript, profondeur * 16384 + lireCurseur, longueurValide, profondeur); lireCurseur = positionFin + 1;
        }
        InterpréteurCommandes.résultat = valeurÉtatValeur; finScript = false; valeurProfondeur = profondeur - 1;
    }
}

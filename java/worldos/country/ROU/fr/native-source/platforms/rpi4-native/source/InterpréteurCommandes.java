// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Ligne de commande UTF-8 sur UART avec guillemets, Backspace, Ctrl-U, Ctrl-C et éditeur en RAM. */
public final class InterpréteurCommandes {
    static int[] ligne = new int[4096], valeurJeton = new int[4096], pointInitial = new int[32], longueur = new int[32];
    static int[] contenuÉdité = new int[16384], nomÉditer = new int[63];
    static int nombreÉlémentsJeton, longueurNomÉditer, résultat;
    static boolean lignePrécédentÉlément;
    static void octetOriginal(int valeur) { CarteMatérielle.écrireSériel(valeur); }
    static int lireLigneEntrée() { return ÉditeurLigne.lire(); }
    static boolean valeursDiviser(int taille) {
        int position = 0, terminaison = 0; nombreÉlémentsJeton = 0;
        while (position < taille) {
            while (position < taille && (ligne[position] == 32 || ligne[position] == 9)) position++;
            if (position == taille) break;
            if (nombreÉlémentsJeton == 16) { EntréeSortieTerminal.écrire("commande analyserValeur: 인수가 너무 많습니다\n"); return false; }
            pointInitial[nombreÉlémentsJeton] = terminaison; int valeurGuillemet = 0;
            while (position < taille) {
                int valeur = ligne[position++];
                if (valeurGuillemet == 0 && (valeur == 32 || valeur == 9)) break;
                if (valeur == valeurGuillemet) { valeurGuillemet = 0; continue; }
                if (valeurGuillemet == 0 && (valeur == 39 || valeur == 34)) { valeurGuillemet = valeur; continue; }
                valeurJeton[terminaison++] = valeur;
            }
            if (valeurGuillemet != 0) { EntréeSortieTerminal.écrire("commande analyserValeur: 따옴표가 닫히지 않았습니다\n"); return false; }
            longueur[nombreÉlémentsJeton] = terminaison - pointInitial[nombreÉlémentsJeton]; nombreÉlémentsJeton++;
        }
        return true;
    }
    static boolean texteÉgal(int numéro, String texteMot) {
        if (numéro >= nombreÉlémentsJeton) return false;
        int indicePosition=0;
        for (int indiceOrdinal=0; indiceOrdinal<texteMot.length(); indiceOrdinal++) {
            int codeCaractère=texteMot.charAt(indiceOrdinal);
            if (codeCaractère>=0xd800 && codeCaractère<=0xdbff && indiceOrdinal+1<texteMot.length()) codeCaractère=0x10000+((codeCaractère-0xd800)<<10)+texteMot.charAt(++indiceOrdinal)-0xdc00;
            int nombreÉlémentsOctet=codeCaractère<128?1:codeCaractère<2048?2:codeCaractère<65536?3:4;
            for (int valeurSéquence=nombreÉlémentsOctet-1; valeurSéquence>=0; valeurSéquence--) {
                int valeur=nombreÉlémentsOctet==1?codeCaractère:valeurSéquence==nombreÉlémentsOctet-1?(nombreÉlémentsOctet==2?0xc0:nombreÉlémentsOctet==3?0xe0:0xf0)|(codeCaractère>>(6*valeurSéquence)):0x80|((codeCaractère>>(6*valeurSéquence))&63);
                if (indicePosition>=longueur[numéro] || valeurJeton[pointInitial[numéro]+indicePosition++]!=valeur) return false;
            }
        }
        return indicePosition==longueur[numéro];
    }
    static int chemin(int numéro) {
        if (numéro >= nombreÉlémentsJeton) return -22;
        int résultat = FichiersMémoire.démarrerChemin(longueur[numéro]); if (résultat < 0) return résultat;
        for (int indiceBoucle = 0; indiceBoucle < longueur[numéro]; indiceBoucle++) {
            résultat = FichiersMémoire.octetChemin(indiceBoucle, valeurJeton[pointInitial[numéro] + indiceBoucle]); if (résultat < 0) return résultat;
        }
        return 0;
    }
    static void erreur(int numéro) { résultat = 1; EntréeSortieTerminal.écrire("erreur "); EntréeSortieTerminal.nombre(numéro); EntréeSortieTerminal.Caractères(10); }
    static void valeurVue() {
        if (nombreÉlémentsJeton != 2) { EntréeSortieTerminal.écrire("사용법: cat Fichier\n"); return; }
        int résultat = chemin(1); if (résultat < 0) { erreur(résultat); return; }
        int Fichier = FichiersMémoire.ouvrir(0); if (Fichier < 0) { erreur(Fichier); return; }
        while (true) { int valeur = FichiersMémoire.lire(Fichier); if (valeur == 256) break; if (valeur < 0) { erreur(valeur); break; } octetOriginal(valeur); }
        FichiersMémoire.fermer(Fichier); EntréeSortieTerminal.Caractères(10);
    }
    static void valeurÉditer() {
        if (nombreÉlémentsJeton != 2) { EntréeSortieTerminal.écrire("사용법: edit Fichier\n"); return; }
        int résultat = chemin(1); if (résultat < 0) { erreur(résultat); return; }
        longueurNomÉditer = longueur[1];
        for (int indiceBoucle = 0; indiceBoucle < longueurNomÉditer; indiceBoucle++) nomÉditer[indiceBoucle] = valeurJeton[pointInitial[1] + indiceBoucle];
        EntréeSortieTerminal.écrire("EDIT: Fichier 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(valeurMaximal 16384바이트)\n");
        int taille = 0;
        while (true) {
            EntréeSortieTerminal.écrire("edit> "); int valeurEntrée = lireLigneEntrée();
            if (valeurEntrée < 0) { EntréeSortieTerminal.écrire("EDIT CANCELLED\n"); return; }
            if (valeurEntrée == 1 && ligne[0] == '.') break;
            if (valeurEntrée + 1 > contenuÉdité.length - taille) { EntréeSortieTerminal.écrire("EDIT CANCELLED: file too large\n"); return; }
            for (int indiceBoucle = 0; indiceBoucle < valeurEntrée; indiceBoucle++) contenuÉdité[taille++] = ligne[indiceBoucle];
            contenuÉdité[taille++] = 10;
        }
        FichiersMémoire.démarrerChemin(longueurNomÉditer);
        for (int indiceBoucle = 0; indiceBoucle < longueurNomÉditer; indiceBoucle++) FichiersMémoire.octetChemin(indiceBoucle, nomÉditer[indiceBoucle]);
        int Fichier = FichiersMémoire.ouvrir(577); if (Fichier < 0) { erreur(Fichier); return; }
        for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) FichiersMémoire.écrire(Fichier, contenuÉdité[indiceBoucle]);
        FichiersMémoire.fermer(Fichier); EntréeSortieTerminal.écrire("SAVED "); EntréeSortieTerminal.nombre(taille); EntréeSortieTerminal.écrire("valeurOctet(주기억 Fichier)\n");
    }
    static int valeurHexadécimal(int valeur) {
        if (valeur >= '0' && valeur <= '9') return valeur - '0';
        if (valeur >= 'a' && valeur <= 'f') return valeur - 'a' + 10;
        if (valeur >= 'A' && valeur <= 'F') return valeur - 'A' + 10;
        return -1;
    }
    static void entréeSortieBinaire(boolean placerValeur) {
        if (nombreÉlémentsJeton != 2) { EntréeSortieTerminal.écrire("사용법: load Fichier | hex Fichier\n"); return; }
        int résultat = chemin(1); if (résultat < 0) { erreur(résultat); return; }
        if (!placerValeur) {
            int Fichier = FichiersMémoire.ouvrir(0); if (Fichier < 0) { erreur(Fichier); return; }
            EntréeSortieTerminal.écrire("HEX BEGIN "); EntréeSortieTerminal.nombre(FichiersMémoire.taille(Fichier)); EntréeSortieTerminal.Caractères(10);
            int nombreÉlémentsEntréeÉlément = 0;
            while (true) {
                int valeur = FichiersMémoire.lire(Fichier); if (valeur < 0 || valeur == 256) break;
                EntréeSortieTerminal.Caractères("0123456789abcdef".charAt(valeur >> 4)); EntréeSortieTerminal.Caractères("0123456789abcdef".charAt(valeur & 15));
                if (++nombreÉlémentsEntréeÉlément % 32 == 0) EntréeSortieTerminal.Caractères(10);
            }
            if (nombreÉlémentsEntréeÉlément % 32 != 0) EntréeSortieTerminal.Caractères(10);
            FichiersMémoire.fermer(Fichier); EntréeSortieTerminal.écrire("HEX END\n"); return;
        }
        longueurNomÉditer = longueur[1];
        for (int indiceBoucle = 0; indiceBoucle < longueurNomÉditer; indiceBoucle++) nomÉditer[indiceBoucle] = valeurJeton[pointInitial[1] + indiceBoucle];
        EntréeSortieTerminal.écrire("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int taille = 0;
        while (true) {
            EntréeSortieTerminal.écrire("hex> "); int valeurEntrée = lireLigneEntrée();
            if (valeurEntrée < 0) { EntréeSortieTerminal.écrire("LOAD CANCELLED\n"); return; }
            if (valeurEntrée == 1 && ligne[0] == '.') break;
            int valeurAvantCôté = -1;
            for (int indiceBoucle = 0; indiceBoucle < valeurEntrée; indiceBoucle++) {
                if (ligne[indiceBoucle] == 32 || ligne[indiceBoucle] == 9) continue;
                int valeur = valeurHexadécimal(ligne[indiceBoucle]);
                if (valeur < 0 || taille >= contenuÉdité.length) { EntréeSortieTerminal.écrire("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (valeurAvantCôté < 0) valeurAvantCôté = valeur; else { contenuÉdité[taille++] = valeurAvantCôté * 16 + valeur; valeurAvantCôté = -1; }
            }
            if (valeurAvantCôté >= 0) { EntréeSortieTerminal.écrire("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        FichiersMémoire.démarrerChemin(longueurNomÉditer);
        for (int indiceBoucle = 0; indiceBoucle < longueurNomÉditer; indiceBoucle++) FichiersMémoire.octetChemin(indiceBoucle, nomÉditer[indiceBoucle]);
        int Fichier = FichiersMémoire.ouvrir(577); if (Fichier < 0) { erreur(Fichier); return; }
        for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) FichiersMémoire.écrire(Fichier, contenuÉdité[indiceBoucle]);
        FichiersMémoire.fermer(Fichier); EntréeSortieTerminal.écrire("LOADED "); EntréeSortieTerminal.nombre(taille); EntréeSortieTerminal.écrire("valeurOctet(주기억 Fichier)\n");
    }
    static int Outils(int numéro) {
        return EntréeÉlémentOutil(numéro, 1);
    }
    static int EntréeÉlémentOutil(int numéro, int lancer) {
        if (nombreÉlémentsJeton - lancer > 8) return -22;
        CarteMatérielle.préparerArguments(nombreÉlémentsJeton - lancer);
        for (int donnéesPremier = lancer; donnéesPremier < nombreÉlémentsJeton; donnéesPremier++) {
            if (longueur[donnéesPremier] > 255) return -36;
            for (int indiceBoucle = 0; indiceBoucle < longueur[donnéesPremier]; indiceBoucle++) CarteMatérielle.octetArgument(donnéesPremier - lancer, indiceBoucle, valeurJeton[pointInitial[donnéesPremier] + indiceBoucle]);
        }
        return numéro == -2 ? CarteMatérielle.exécuterFichierLinux() : numéro < 0 ? CarteMatérielle.exécuterFichierUtilisateur() : CarteMatérielle.lancerProgrammeUtilisateur(numéro);
    }
    static int LotPython() {
        if (nombreÉlémentsJeton > 8) return -22;
        CarteMatérielle.préparerArguments(nombreÉlémentsJeton);
        String chemin = "/lib/Paquet.py";
        // Écrire une chaîne Java dans le tampon d’arguments UTF-8 de l’interpréteur de commandes.
        int indicePosition = 0;
        for (int indiceOrdinal = 0; indiceOrdinal < chemin.length(); indiceOrdinal++) {
            int valeurCaractère = chemin.charAt(indiceOrdinal);
            if (valeurCaractère < 128) CarteMatérielle.octetArgument(0, indicePosition++, valeurCaractère);
            else { CarteMatérielle.octetArgument(0, indicePosition++, 0xe0 | (valeurCaractère >> 12)); CarteMatérielle.octetArgument(0, indicePosition++, 0x80 | ((valeurCaractère >> 6) & 63)); CarteMatérielle.octetArgument(0, indicePosition++, 0x80 | (valeurCaractère & 63)); }
        }
        for (int indiceOrdinal = 1; indiceOrdinal < nombreÉlémentsJeton; indiceOrdinal++) {
            if (longueur[indiceOrdinal] > 255) return -36;
            for (int valeurCaractère = 0; valeurCaractère < longueur[indiceOrdinal]; valeurCaractère++) CarteMatérielle.octetArgument(indiceOrdinal, valeurCaractère, valeurJeton[pointInitial[indiceOrdinal] + valeurCaractère]);
        }
        return CarteMatérielle.lancerProgrammeUtilisateur(12);
    }
    static int formatExécution() {
        int valeurTraité = chemin(0); if (valeurTraité < 0) return valeurTraité;
        int Fichier = FichiersMémoire.ouvrir(0); if (Fichier < 0) return Fichier;
        int donnéesPremier = FichiersMémoire.lire(Fichier), donnéesOctet = FichiersMémoire.lire(Fichier), codeCaractère = FichiersMémoire.lire(Fichier), valeurFinalPosition = FichiersMémoire.lire(Fichier);
        FichiersMémoire.fermer(Fichier);
        if (donnéesPremier == 127 && donnéesOctet == 'E' && codeCaractère == 'L' && valeurFinalPosition == 'F') return 1;
        if (donnéesPremier == 'P' && donnéesOctet == 'K' && codeCaractère == 3 && valeurFinalPosition == 4) return 2;
        return 0;
    }
    static int lancerExemple(int numéro, String arguments) {
        CarteMatérielle.préparerArguments(1);
        for (int indiceBoucle = 0; indiceBoucle < arguments.length(); indiceBoucle++) CarteMatérielle.octetArgument(0, indiceBoucle, arguments.charAt(indiceBoucle));
        return CarteMatérielle.lancerProgrammeUtilisateur(numéro);
    }
    static void octetTexte(int Fichier, int valeur) { FichiersMémoire.écrire(Fichier, valeur); }
    static void fichierStatique(String nom, String valeurContenuValeur) {
        // Les noms de fichiers du paquet sont en ASCII ; leur contenu est enregistré en UTF-8.
        FichiersMémoire.démarrerChemin(nom.length());
        for (int indiceBoucle = 0; indiceBoucle < nom.length(); indiceBoucle++) FichiersMémoire.octetChemin(indiceBoucle, nom.charAt(indiceBoucle));
        int Fichier = FichiersMémoire.ouvrir(193); if (Fichier < 0) return;
        for (int indiceBoucle = 0; indiceBoucle < valeurContenuValeur.length(); indiceBoucle++) {
            int codeCaractère = valeurContenuValeur.charAt(indiceBoucle);
            if (codeCaractère >= 0xd800 && codeCaractère <= 0xdbff && indiceBoucle + 1 < valeurContenuValeur.length()) codeCaractère = 0x10000 + ((codeCaractère - 0xd800) << 10) + valeurContenuValeur.charAt(++indiceBoucle) - 0xdc00;
            if (codeCaractère < 128) octetTexte(Fichier, codeCaractère);
            else {
                int nombre = codeCaractère < 2048 ? 2 : codeCaractère < 65536 ? 3 : 4;
                octetTexte(Fichier, (nombre == 2 ? 0xc0 : nombre == 3 ? 0xe0 : 0xf0) | (codeCaractère >> (6 * (nombre - 1))));
                for (int nombreÉlémentsEntréeÉlément = nombre - 1; nombreÉlémentsEntréeÉlément > 0; nombreÉlémentsEntréeÉlément--) octetTexte(Fichier, 0x80 | ((codeCaractère >> (6 * (nombreÉlémentsEntréeÉlément - 1))) & 63));
            }
        }
        FichiersMémoire.fermer(Fichier);
    }
    static void aideHangul() {
        EntréeSortieTerminal.écrire("F9 ou Shift+Space active la saisie en français.\n");
        EntréeSortieTerminal.écrire("  [FR] keyboard; [EN] ASCII\n");
        EntréeSortieTerminal.écrire("  _ → °\n");
        EntréeSortieTerminal.écrire("  F9: EN ↔ fr | Ctrl+Shift+V: UTF-8\n");
        EntréeSortieTerminal.écrire("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        EntréeSortieTerminal.écrire("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int cheminExemple(String nom) {
        int nombreÉlémentsOctet = 0;
        for (int indiceBoucle = 0; indiceBoucle < nom.length(); indiceBoucle++) { int codeCaractère = nom.charAt(indiceBoucle); if (codeCaractère >= 0xd800 && codeCaractère <= 0xdfff) return -22; nombreÉlémentsOctet += codeCaractère < 128 ? 1 : codeCaractère < 2048 ? 2 : 3; }
        int valeurTraité = FichiersMémoire.démarrerChemin(nombreÉlémentsOctet); if (valeurTraité < 0) return valeurTraité;
        int indicePosition = 0;
        for (int indiceBoucle = 0; indiceBoucle < nom.length(); indiceBoucle++) {
            int codeCaractère = nom.charAt(indiceBoucle);
            if (codeCaractère < 128) FichiersMémoire.octetChemin(indicePosition++, codeCaractère);
            else if (codeCaractère < 2048) { FichiersMémoire.octetChemin(indicePosition++, 0xc0 | (codeCaractère >> 6)); FichiersMémoire.octetChemin(indicePosition++, 0x80 | (codeCaractère & 63)); }
            else { FichiersMémoire.octetChemin(indicePosition++, 0xe0 | (codeCaractère >> 12)); FichiersMémoire.octetChemin(indicePosition++, 0x80 | ((codeCaractère >> 6) & 63)); FichiersMémoire.octetChemin(indicePosition++, 0x80 | (codeCaractère & 63)); }
        }
        return 0;
    }
    static int répertoireExemple(String nom) {
        int valeurTraité = cheminExemple(nom); if (valeurTraité < 0) return valeurTraité;
        valeurTraité = FichiersMémoire.créerRépertoire(); return valeurTraité == -17 ? 0 : valeurTraité;
    }
    static int fichierExemple(String nom, String Données) {
        int valeurTraité = cheminExemple(nom); if (valeurTraité < 0) return valeurTraité;
        int Fichier = FichiersMémoire.ouvrir(193); if (Fichier == -17) return 0; if (Fichier < 0) return Fichier;
        for (int indiceBoucle = 0; indiceBoucle < Données.length(); indiceBoucle += 2) {
            valeurTraité = FichiersMémoire.écrire(Fichier, valeurHexadécimal(Données.charAt(indiceBoucle)) * 16 + valeurHexadécimal(Données.charAt(indiceBoucle + 1)));
            if (valeurTraité < 0) { FichiersMémoire.fermer(Fichier); return valeurTraité; }
        }
        return FichiersMémoire.fermer(Fichier);
    }
    static void afficherAide() {
        outilSystème.afficherAide();
        EntréeSortieTerminal.écrire("sshd / interpréteurCommandesSécuriser start|stop|status: SSH :22 (user, 장치별 valeurMotPasse)\n");
        EntréeSortieTerminal.écrire("vncd / PrésenterDistant start|stop|status: VNC :5900 (장치별 valeurMotPasse)\n");
        EntréeSortieTerminal.écrire("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        EntréeSortieTerminal.écrire("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        EntréeSortieTerminal.écrire("wc grep head tail tee env export unset history sh source true false exit\n");
        EntréeSortieTerminal.écrire("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        EntréeSortieTerminal.écrire("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        EntréeSortieTerminal.écrire("valeurCoin + côtéGauche 버튼 valeurGlisser: terminal taille changerValeur; terminal size: valeurColonne/valeurRangée\n");
        EntréeSortieTerminal.écrire("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        EntréeSortieTerminal.écrire("vi FILE: i to insert; Esc then :wq to save and quit\n");
        EntréeSortieTerminal.écrire("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        EntréeSortieTerminal.écrire("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        EntréeSortieTerminal.écrire("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        EntréeSortieTerminal.écrire("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        EntréeSortieTerminal.écrire("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        EntréeSortieTerminal.écrire("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        EntréeSortieTerminal.écrire("python FILE.py | python -c 'CODE' (MicroPython)\n");
        EntréeSortieTerminal.écrire("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        EntréeSortieTerminal.écrire("pip: MicroPython arbreSource installerValeur; Hôte --network --pip valeurNécessaire; /lib는 RAM\n");
        EntréeSortieTerminal.écrire("gui | run cpp | net test | tasks | selftest | samples\n");
        EntréeSortieTerminal.écrire("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        EntréeSortieTerminal.écrire("/example/java /example/c /example/python: examples ready at boot\n");
        EntréeSortieTerminal.écrire("example java|c|python: restore missing examples (keeps existing files)\n");
        aideHangul();
    }
    static void terminal(boolean commutéÉtait) {
        if (commutéÉtait && CarteMatérielle.terminal(2) != 0) { CarteMatérielle.terminal(0); EntréeSortieTerminal.écrire("TERMINAL CLOSED\n"); }
        else if (CarteMatérielle.terminal(1) < 0) erreur(-19);
        else EntréeSortieTerminal.écrire("TERMINAL READY — fr terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void commande() {
        if (nombreÉlémentsJeton == 0) return;
        if (outilSystème.exécuterCommande()) return;
        if (texteÉgal(0,"sshd") || texteÉgal(0,"interpréteurCommandesSécuriser") || texteÉgal(0,"vncd") || texteÉgal(0,"PrésenterDistant")) {
            int valeurGenre=texteÉgal(0,"vncd")||texteÉgal(0,"PrésenterDistant")?1:0;
            int action=texteÉgal(1,"start")||texteÉgal(1,"lancer")?1:texteÉgal(1,"stop")||texteÉgal(1,"arrêter")?0:2;
            int valeurÉtatValeur=CarteMatérielle.contrôleDistant(valeurGenre,action);
            if(valeurÉtatValeur<0)erreur(valeurÉtatValeur);else EntréeSortieTerminal.écrire(CarteMatérielle.contrôleDistant(valeurGenre,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (texteÉgal(0, "help") || texteÉgal(0, "h")) { if (texteÉgal(1, "ko") || texteÉgal(1, "input")) aideHangul(); else afficherAide(); }
        else if (texteÉgal(0, "info") || texteÉgal(0, "i")) Noyau.informationSystème();
        else if (texteÉgal(0, "pwd")) { FichiersMémoire.écrireActuel(); EntréeSortieTerminal.Caractères(10); }
        else if (texteÉgal(0, "cd")) {
            int valeurTraité;
            if (nombreÉlémentsJeton == 1) { FichiersMémoire.démarrerChemin(1); valeurTraité = FichiersMémoire.octetChemin(0, '/'); } else valeurTraité = nombreÉlémentsJeton == 2 ? chemin(1) : -22;
            if (valeurTraité >= 0) valeurTraité = FichiersMémoire.changerRépertoire(); if (valeurTraité < 0) erreur(valeurTraité);
        }
        else if (texteÉgal(0, "ls") || texteÉgal(0, "f")) {
            int indiceArgument = texteÉgal(1, "-l") ? 2 : 1, valeurTraité;
            if (nombreÉlémentsJeton == indiceArgument) { FichiersMémoire.démarrerChemin(1); valeurTraité = FichiersMémoire.octetChemin(0, '.'); } else valeurTraité = nombreÉlémentsJeton == indiceArgument + 1 ? chemin(indiceArgument) : -22;
            if (valeurTraité >= 0) valeurTraité = FichiersMémoire.entréesListeChemin(); if (valeurTraité < 0) erreur(valeurTraité);
        }
        else if (texteÉgal(0, "mkdir") || texteÉgal(0, "rmdir") || texteÉgal(0, "touch")) OutilsInterpréteurCommandes.travailUnitéFichier(texteÉgal(0, "mkdir") ? "mkdir" : texteÉgal(0, "rmdir") ? "rmdir" : "touch");
        else if (texteÉgal(0, "cp") || texteÉgal(0, "mv")) OutilsInterpréteurCommandes.copierValeur(texteÉgal(0, "mv"));
        else if (texteÉgal(0, "cat")) OutilsInterpréteurCommandes.valeurVue();
        else if (texteÉgal(0, "wc")) OutilsInterpréteurCommandes.valeurComptageEnCours();
        else if (texteÉgal(0, "grep")) OutilsInterpréteurCommandes.trouverEntréeÉlément();
        else if (texteÉgal(0, "head") || texteÉgal(0, "tail")) OutilsInterpréteurCommandes.valeurTête(texteÉgal(0, "tail"));
        else if (texteÉgal(0, "tee")) OutilsInterpréteurCommandes.écrireEnsemble();
        else if (texteÉgal(0, "env")) SyntaxeInterpréteurCommandes.afficherEnvironnement();
        else if (texteÉgal(0, "export") || texteÉgal(0, "unset")) {
            if (nombreÉlémentsJeton == 1) SyntaxeInterpréteurCommandes.afficherEnvironnement();
            for (int indiceBoucle = 1; indiceBoucle < nombreÉlémentsJeton; indiceBoucle++) { int valeurTraité = SyntaxeInterpréteurCommandes.réglagesEnvironnement(indiceBoucle, texteÉgal(0, "unset")); if (valeurTraité != 0) { résultat = valeurTraité; EntréeSortieTerminal.écrire("commande analyserValeur: valeurVariable 이름이 잘못되었거나 예약된 이름이거나 environnement 공간이 가득 찼습니다\n"); } }
        }
        else if (texteÉgal(0, "sh") || texteÉgal(0, "source")) SyntaxeInterpréteurCommandes.exécuterFichier();
        else if (texteÉgal(0, "true")) résultat = 0;
        else if (texteÉgal(0, "false")) résultat = 1;
        else if (texteÉgal(0, "history")) ÉditeurLigne.afficherJournal();
        else if (texteÉgal(0, "exit")) {
            if (SyntaxeInterpréteurCommandes.valeurProfondeur > 0) { résultat = nombreÉlémentsJeton == 1 ? SyntaxeInterpréteurCommandes.valeurÉtatValeur : OutilsInterpréteurCommandes.valeurChiffre(1); if (résultat < 0 || résultat > 255) résultat = 2; SyntaxeInterpréteurCommandes.finScript = true; }
            else if (CarteMatérielle.terminal(2) != 0) terminal(true);
            else EntréeSortieTerminal.écrire("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (texteÉgal(0, "edit")) valeurÉditer();
        else if (texteÉgal(0, "load") || texteÉgal(0, "hex")) entréeSortieBinaire(texteÉgal(0, "load"));
        else if (texteÉgal(0, "rm")) {
            if (nombreÉlémentsJeton < 2) { résultat = 2; EntréeSortieTerminal.écrire("사용법: rm Fichier...\n"); }
            for (int indiceBoucle = 1; indiceBoucle < nombreÉlémentsJeton; indiceBoucle++) { int valeurTraité = chemin(indiceBoucle); if (valeurTraité == 0) valeurTraité = FichiersMémoire.effacerEntréeÉlément(); if (valeurTraité < 0) erreur(valeurTraité); }
        }
        else if (texteÉgal(0, "echo")) {
            int démarrerPosition = texteÉgal(1, "-n") ? 2 : 1;
            for (int donnéesPremier = démarrerPosition; donnéesPremier < nombreÉlémentsJeton; donnéesPremier++) { if (donnéesPremier > démarrerPosition) EntréeSortieTerminal.Caractères(32); for (int indiceBoucle = 0; indiceBoucle < longueur[donnéesPremier]; indiceBoucle++) CarteMatérielle.écrireSériel(valeurJeton[pointInitial[donnéesPremier] + indiceBoucle]); }
            if (démarrerPosition == 1) EntréeSortieTerminal.Caractères(10);
        }
        else if (texteÉgal(0, "clear")) EntréeSortieTerminal.écrire("\u001b[2J\u001b[H");
        else if (texteÉgal(0, "javac") || texteÉgal(0, "java") || texteÉgal(0, "python") || texteÉgal(0, "pip")) {
            int valeurTraité = texteÉgal(0, "pip") ? LotPython() : Outils(texteÉgal(0, "javac") ? 10 : texteÉgal(0, "java") ? 11 : 12); résultat = valeurTraité == -1005 ? -1005 : valeurTraité < 0 ? 126 : valeurTraité;
            if (valeurTraité != -1005 && !SyntaxeInterpréteurCommandes.estConnexionEnCours) { EntréeSortieTerminal.écrire("exit "); EntréeSortieTerminal.nombre(valeurTraité); EntréeSortieTerminal.Caractères(10); }
        }
        else if (texteÉgal(0, "vi")) { int valeurTraité = Outils(13); résultat = valeurTraité == -1005 ? -1005 : valeurTraité < 0 ? 126 : valeurTraité; }
        else if (texteÉgal(0, "cc") || texteÉgal(0, "tcc")) { int valeurTraité = Outils(15); résultat = valeurTraité < 0 ? 126 : valeurTraité; if (!SyntaxeInterpréteurCommandes.estConnexionEnCours) { EntréeSortieTerminal.écrire("exit "); EntréeSortieTerminal.nombre(valeurTraité); EntréeSortieTerminal.Caractères(10); } }
        else if (texteÉgal(0, "jaot")) { int valeurTraité = Outils(16); résultat = valeurTraité < 0 ? 126 : valeurTraité; if (!SyntaxeInterpréteurCommandes.estConnexionEnCours) { EntréeSortieTerminal.écrire("exit "); EntréeSortieTerminal.nombre(valeurTraité); EntréeSortieTerminal.Caractères(10); } }
        else if (texteÉgal(0, "terminal")) {
            if (texteÉgal(1, "size")) { int taille = CarteMatérielle.terminal(13); EntréeSortieTerminal.écrire("TERMINAL SIZE "); EntréeSortieTerminal.nombre(taille & 65535); EntréeSortieTerminal.Caractères('x'); EntréeSortieTerminal.nombre(taille >>> 16); EntréeSortieTerminal.Caractères(10); }
            else terminal(false);
        }
        else if (texteÉgal(0, "gui") || texteÉgal(0, "v")) { CarteMatérielle.terminal(9); Bureau.exécuterCommande(); }
        else if (texteÉgal(0, "c")) Noyau.testC();
        else if (texteÉgal(0, "tasks") || texteÉgal(0, "t")) Noyau.testTâches();
        else if (texteÉgal(0, "g")) Noyau.Écran();
        else if (texteÉgal(0, "selftest") || texteÉgal(0, "u")) Noyau.testProgrammesUtilisateur();
        else if (texteÉgal(0, "e") || (texteÉgal(0, "run") && texteÉgal(1, "cpp"))) {
            int valeurTraité = CarteMatérielle.lancerProgrammeUtilisateur(0); if (valeurTraité == 0) EntréeSortieTerminal.écrire("ELF DEMO PASS\n"); else erreur(valeurTraité);
        }
        else if (texteÉgal(0, "run")) { int valeurTraité = texteÉgal(1, "--linux") ? EntréeÉlémentOutil(-2, 2) : Outils(-1); résultat = valeurTraité == -1005 ? -1005 : valeurTraité < 0 ? 126 : valeurTraité; if (valeurTraité != -1005 && !SyntaxeInterpréteurCommandes.estConnexionEnCours) { EntréeSortieTerminal.écrire("exit "); EntréeSortieTerminal.nombre(valeurTraité); EntréeSortieTerminal.Caractères(10); } }
        else if (texteÉgal(0, "n") || (texteÉgal(0, "net") && texteÉgal(1, "test"))) Noyau.testMiseEnRéseau();
        else if (texteÉgal(0, "ftpd")) {
            if (texteÉgal(1, "start")) { int valeurTraité = CarteMatérielle.serviceTransfertFichier(1); if (valeurTraité < 0) erreur(valeurTraité); else { EntréeSortieTerminal.écrire("FTP listening "); outilSystème.écrireAdresse(CarteMatérielle.étatRéseau(0,0)); EntréeSortieTerminal.écrire(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (texteÉgal(1, "stop")) { CarteMatérielle.serviceTransfertFichier(0); EntréeSortieTerminal.écrire("FTP stopped\n"); }
            else EntréeSortieTerminal.écrire(CarteMatérielle.serviceTransfertFichier(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (texteÉgal(0, "samples")) { Paquet.préparer(); EntréeSortieTerminal.écrire("SAMPLES READY (existing files kept)\n"); }
        else if (texteÉgal(0, "example")) {
            int Langue = texteÉgal(1, "java") ? 0 : texteÉgal(1, "c") ? 1 : texteÉgal(1, "python") ? 2 : -1;
            if (nombreÉlémentsJeton != 2 || Langue < 0) EntréeSortieTerminal.écrire("example java|c|python: Sortie, Fichier, 네트워크, 그래픽, Java Swing fenêtre Exemples\n");
            else { int valeurTraité = LotExemple.installerValeur(Langue); if (valeurTraité < 0) { erreur(valeurTraité); if (valeurTraité == -28) EntréeSortieTerminal.écrire("RAM full: remove unused files, then retry example\n"); } else EntréeSortieTerminal.écrire("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int valeurFormat = formatExécution();
            if (valeurFormat == 1 || valeurFormat == 2) {
                int valeurTraité = EntréeÉlémentOutil(valeurFormat == 1 ? -1 : 14, 0); résultat = valeurTraité == -1005 ? -1005 : valeurTraité < 0 ? 126 : valeurTraité;
                if (valeurTraité != -1005 && !SyntaxeInterpréteurCommandes.estConnexionEnCours) { EntréeSortieTerminal.écrire("exit "); EntréeSortieTerminal.nombre(valeurTraité); EntréeSortieTerminal.Caractères(10); }
            } else if (valeurFormat == 0) { résultat = 126; EntréeSortieTerminal.écrire("실행할 nombre 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { résultat = 127; EntréeSortieTerminal.écrire("Unknown command. help: commands\n"); }
        }
    }
    public static void exécuterCommande() {
        Paquet.préparer();
        for (int Langue = 0; Langue < 3; Langue++) { int valeurTraité = LotExemple.installerValeur(Langue); if (valeurTraité < 0) erreur(valeurTraité); }
        afficherAide();
        while (true) {
            sessionFenêtre.entréeÉlémentValeurProcessus(); if (sessionFenêtre.exécutionReprendre()) continue;
            if (!sessionFenêtre.lireContinuation) EntréeSortieTerminal.écrire("jkoros-native> "); ÉditeurLigne.ligneCommande = true; CarteMatérielle.attendreDistant(1); int taille = lireLigneEntrée(); CarteMatérielle.attendreDistant(0); ÉditeurLigne.ligneCommande = false;
            if (taille == -3) continue;
            if (taille == -2) EntréeSortieTerminal.écrire("commande analyserValeur: 명령줄이 너무 깁니다\n");
            if (taille >= 0) { SyntaxeInterpréteurCommandes.finScript = false; SyntaxeInterpréteurCommandes.exécuterCommande(ligne, 0, taille, 0); } else SyntaxeInterpréteurCommandes.valeurÉtatValeur = 130;
            CarteMatérielle.commandeDistantFin(SyntaxeInterpréteurCommandes.valeurÉtatValeur);
            ÉditeurLigne.taille = ÉditeurLigne.valeurCurseur = ÉditeurLigne.démarrerFenêtre = 0;
        }
    }
}

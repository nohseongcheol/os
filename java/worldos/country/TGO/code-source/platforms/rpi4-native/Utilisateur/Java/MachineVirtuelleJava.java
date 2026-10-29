// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** JVM restreinte exécutée au niveau ARM64 EL0. Vérifie à l’exécution les limites des fichiers, de la pile, des références et des branchements. */
public final class MachineVirtuelleJava {
    static int[] Fichier = new int[16 * 16384], fichierTemporaire = new int[16384], texteNomFichier = new int[512];
    static int[] baliseConstante = new int[8192], valeurPremierConstante = new int[8192], valeurDeuxièmeConstante = new int[8192], référenceChaîne = new int[8192];
    static int[] texteNomMéthode = new int[512], typeMéthode = new int[512], accèsMéthode = new int[512], propriétaireMéthode = new int[512];
    static int[] démarrerMéthode = new int[512], finMéthode = new int[512], pileMéthode = new int[512], variablesLocalesMéthode = new int[512];
    static int[] nombreÉlémentsArgumentMéthode = new int[512], typeArgumentMéthode = new int[8192], retournerMéthode = new int[512];
    static int[] valeurFrontière = new int[16 * 16384];
    static int[] valeurLocal = new int[16384], typeLocal = new int[16384], valeurPileOpérande = new int[16384], typePileOpérande = new int[16384];
    static int[] méthodeCadre = new int[128], positionCadre = new int[128], pileCadre = new int[128], instructionMachineCadre = new int[128], initialiserCadre = new int[128];
    static int[] nomDéfinitionClasse = new int[16], tailleDéfinitionClasse = new int[16], parentDéfinitionClasse = new int[16], étatValeurDéfinitionClasse = new int[16], nombreÉlémentsEmplacementClasse = new int[16], initialiserDéfinitionClasse = new int[16];
    static int[] interfaceClasse = new int[16 * 16], nombreÉlémentsInterfaceClasse = new int[16];
    static int[] nomEmplacement = new int[512], typeEmplacement = new int[512], propriétaireEmplacement = new int[512], permissionsEmplacement = new int[512], positionEmplacement = new int[512], donnéesEmplacement = new int[512];
    static int[] intercepterDémarrer = new int[1024], intercepterFin = new int[1024], intercepterPosition = new int[1024], intercepterClasse = new int[1024], intercepterMéthode = new int[1024];
    static int[] valeurTas = new int[32768], largeurTas = new int[32768], marqueTas = new int[32768], référenceTas = new int[32768], attendrePrésenterPour = new int[32768];
    static int[] référenceTemporaire = new int[256], élémentTableau = new int[32768], entierStocker = new int[256];
    static int taille, lirePosition, nombreÉlémentsMéthode, nomClasse, indiceCadre = -1, positionFinTas = 1, typeRetourner;
    static int nombreÉlémentsDéfinitionClasse, nombreÉlémentsEmplacement, intercepterNombreÉléments, classeAnalyséActuel, objetLevé, nombreÉlémentsTemporaire, nombreÉlémentsPrésenter, nombreÉlémentsCollection;
    static int filExécutionActuel, nombreÉlémentsFilExécution = 1, définitionClasseEntréeÉlément;
    static int[] cadreFilExécution = new int[4], étatValeurFilExécution = new int[4], objetFilExécution = new int[4], cibleFilExécution = new int[4], attendreFilExécutionPour = new int[4];
    static boolean erreur, changerRequête;
    static int[] propriétaireVerrou = new int[32768], profondeurVerrou = new int[32768], verrouCadre = new int[128], verrouClasse = new int[16], filExécutionClasse = new int[16];

    static void valeurÉchec(String texteMot) {
        if (erreur) return;
        int codeCatégorie = 0;
        if (OutilJava.texteÉgal(texteMot, "ArithmeticException: / by zero")) codeCatégorie = 4;
        if (OutilJava.texteÉgal(texteMot, "NullPointerException") || OutilJava.texteÉgal(texteMot, "null or invalid array")) codeCatégorie = 5;
        if (OutilJava.texteÉgal(texteMot, "ArrayIndexOutOfBoundsException")) codeCatégorie = 7;
        if (OutilJava.texteÉgal(texteMot, "StringIndexOutOfBoundsException")) codeCatégorie = 8;
        if (OutilJava.texteÉgal(texteMot, "NumberFormatException")) codeCatégorie = 10;
        if (OutilJava.texteÉgal(texteMot, "FileNotFoundException: file open failed")) codeCatégorie = 12;
        if (OutilJava.texteÉgal(texteMot, "IOException: stream closed") || OutilJava.texteÉgal(texteMot, "IOException: read failed") || OutilJava.texteÉgal(texteMot, "IOException: write failed")) codeCatégorie = 11;
        if (OutilJava.texteÉgal(texteMot, "ClassCastException")) codeCatégorie = 14;
        if (OutilJava.texteÉgal(texteMot, "NegativeArraySizeException")) codeCatégorie = 15;
        if (codeCatégorie != 0 && indiceCadre >= 0) { leverException(codeCatégorie, texteMot); return; }
        Utilisateur.écrire("JVM error: "); Utilisateur.écrire(texteMot); Utilisateur.écrireValeurCaractère(10); erreur = true;
    }
    static boolean rogner(int lancer, int longueur) {
        if (lancer < 0 || lancer >= Fichier.length || longueur < 0) return false;
        int définitionClasse = lancer / 16384;
        return lancer % 16384 <= tailleDéfinitionClasse[définitionClasse] && longueur <= tailleDéfinitionClasse[définitionClasse] - lancer % 16384;
    }
    static int valeurOctet() {
        if (!rogner(lirePosition, 1)) { valeurÉchec("truncated class file"); return 0; }
        return Fichier[lirePosition++];
    }
    static int valeurCourt() { return valeurOctet() << 8 | valeurOctet(); }
    static int Entier() { return valeurCourt() << 16 | valeurCourt(); }
    static void sauterOctets(int longueur) { if (!rogner(lirePosition, longueur)) valeurÉchec("invalid attribute size"); else lirePosition += longueur; }
    static boolean contrôlerConstante(int nombre, int valeurGenre) {
        if (nombre <= 0 || nombre >= baliseConstante.length || baliseConstante[nombre] != valeurGenre) { valeurÉchec("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean plageTexte(int lancer, int longueur, String texteMot) {
        if (!rogner(lancer, longueur)) return false;
        int lireCurseur = lancer, terminaison = lancer + longueur;
        for (int indiceBoucle = 0; indiceBoucle < texteMot.length(); indiceBoucle++) {
            int codeCaractère = texteMot.charAt(indiceBoucle);
            if (codeCaractère > 0 && codeCaractère < 128) { if (lireCurseur >= terminaison || Fichier[lireCurseur++] != codeCaractère) return false; }
            else if (codeCaractère < 2048) {
                if (lireCurseur + 2 > terminaison || Fichier[lireCurseur++] != (192 | (codeCaractère >> 6)) || Fichier[lireCurseur++] != (128 | (codeCaractère & 63))) return false;
            } else if (lireCurseur + 3 > terminaison || Fichier[lireCurseur++] != (224 | (codeCaractère >> 12)) || Fichier[lireCurseur++] != (128 | ((codeCaractère >> 6) & 63)) || Fichier[lireCurseur++] != (128 | (codeCaractère & 63))) return false;
        }
        return lireCurseur == terminaison;
    }
    static boolean texteMot(int valeurConstante, String texteMot) { return contrôlerConstante(valeurConstante, 1) && plageTexte(valeurPremierConstante[valeurConstante], valeurDeuxièmeConstante[valeurConstante], texteMot); }
    static boolean motConcordant(int opérandePremier, int opérandeDeuxième) {
        if (!contrôlerConstante(opérandePremier, 1) || !contrôlerConstante(opérandeDeuxième, 1) || valeurDeuxièmeConstante[opérandePremier] != valeurDeuxièmeConstante[opérandeDeuxième]) return false;
        for (int nombre = 0; nombre < valeurDeuxièmeConstante[opérandePremier]; nombre++) if (Fichier[valeurPremierConstante[opérandePremier] + nombre] != Fichier[valeurPremierConstante[opérandeDeuxième] + nombre]) return false;
        return true;
    }
    static int texteNomClasse(int nombre) { return contrôlerConstante(nombre, 7) && contrôlerConstante(valeurPremierConstante[nombre], 1) ? valeurPremierConstante[nombre] : 0; }
    static int nomRéférence(int nombre) { return contrôlerConstante(nombre, 12) && contrôlerConstante(valeurPremierConstante[nombre], 1) ? valeurPremierConstante[nombre] : 0; }
    static int typeRéférence(int nombre) { return contrôlerConstante(nombre, 12) && contrôlerConstante(valeurDeuxièmeConstante[nombre], 1) ? valeurDeuxièmeConstante[nombre] : 0; }
    static int typeDescripteur(int terminaison, boolean typeVide) {
        if (lirePosition >= terminaison) { valeurÉchec("invalid descriptor"); return 0; }
        int valeur = valeurOctet();
        if (valeur == 'V' && typeVide) return 0;
        if (valeur == 'I' || valeur == 'B' || valeur == 'C' || valeur == 'S' || valeur == 'Z') return 1;
        if (valeur == '[') { typeDescripteur(terminaison, false); return 2; }
        if (valeur == 'L') {
            int lancer = lirePosition;
            while (lirePosition < terminaison && Fichier[lirePosition] != ';') lirePosition++;
            if (lirePosition == terminaison || lirePosition == lancer) valeurÉchec("invalid reference descriptor");
            else lirePosition++;
            return 2;
        }
        valeurÉchec("unsupported descriptor type"); return 0;
    }
    static void lireDescripteur(int Fonction) {
        int élémentListePrécédentÉlément = lirePosition, nombre = typeMéthode[Fonction];
        if (!contrôlerConstante(nombre, 1)) return;
        lirePosition = valeurPremierConstante[nombre]; int terminaison = lirePosition + valeurDeuxièmeConstante[nombre];
        if (valeurOctet() != '(') valeurÉchec("invalid method descriptor");
        int nombreÉlémentsÉlémentListe = 0;
        while (!erreur && lirePosition < terminaison && Fichier[lirePosition] != ')') {
            if (nombreÉlémentsÉlémentListe == 16) { valeurÉchec("too many method arguments"); break; }
            typeArgumentMéthode[Fonction * 16 + nombreÉlémentsÉlémentListe++] = typeDescripteur(terminaison, false);
        }
        if (lirePosition >= terminaison || valeurOctet() != ')') valeurÉchec("invalid method descriptor");
        retournerMéthode[Fonction] = typeDescripteur(terminaison, true); nombreÉlémentsArgumentMéthode[Fonction] = nombreÉlémentsÉlémentListe;
        if (lirePosition != terminaison) valeurÉchec("invalid method descriptor");
        lirePosition = élémentListePrécédentÉlément;
    }
    static int lireIndiceConstante() { int valeur = valeurCourt(); return valeur == 0 ? 0 : classeAnalyséActuel * 512 + valeur; }
    static int lireConstanteCodeOpération() { return propriétaireMéthode[méthodeCadre[indiceCadre]] * 512 + lireCourtCodeOpération(); }
    static void sauterAttribut() {
        int nombreÉlémentsÉlémentListe = valeurCourt();
        for (int nombre = 0; nombre < nombreÉlémentsÉlémentListe && !erreur; nombre++) { contrôlerConstante(lireIndiceConstante(), 1); sauterOctets(Entier()); }
    }
    static int longueurCommande(int valeur) {
        if (valeur == 16 || valeur == 18 || valeur == 21 || valeur == 25 || valeur == 54 || valeur == 58 || valeur == 188) return 2;
        if (valeur == 17 || valeur == 19 || valeur == 132 || valeur >= 153 && valeur <= 167
            || valeur >= 178 && valeur <= 184 || valeur == 187 || valeur == 189 || valeur == 192 || valeur == 193 || valeur == 198 || valeur == 199) return 3;
        if (valeur == 185 || valeur == 200) return 5;
        if (valeur >= 0 && valeur <= 8 || valeur >= 26 && valeur <= 29 || valeur >= 42 && valeur <= 46 || valeur >= 50 && valeur <= 53
            || valeur >= 59 && valeur <= 62 || valeur >= 75 && valeur <= 79 || valeur >= 83 && valeur <= 95
            || valeur == 96 || valeur == 100 || valeur == 104 || valeur == 108 || valeur == 112 || valeur == 116
            || valeur == 120 || valeur == 122 || valeur == 124 || valeur == 126 || valeur == 128 || valeur == 130
            || valeur >= 145 && valeur <= 147 || valeur == 172 || valeur == 176 || valeur == 177 || valeur == 190 || valeur == 191
            || valeur == 194 || valeur == 195) return 1;
        return 0;
    }
    static int entierPosition(int lireCurseur) {
        if (!rogner(lireCurseur, 4)) { valeurÉchec("truncated bytecode operand"); return 0; }
        return Fichier[lireCurseur] << 24 | Fichier[lireCurseur + 1] << 16 | Fichier[lireCurseur + 2] << 8 | Fichier[lireCurseur + 3];
    }
    static int lireLongueur(int lireCurseur, int lancer, int terminaison) {
        int valeur = Fichier[lireCurseur], longueur = longueurCommande(valeur);
        if (valeur == 170 || valeur == 171) {
            int positionBase = lireCurseur + 1;
            while ((positionBase - lancer) % 4 != 0) positionBase++;
            if (terminaison - positionBase < (valeur == 170 ? 12 : 8)) return 0;
            int nombreÉlémentsEntréeÉlément = valeur == 170 ? entierPosition(positionBase + 8) - entierPosition(positionBase + 4) + 1 : entierPosition(positionBase + 4);
            if (nombreÉlémentsEntréeÉlément < 0 || nombreÉlémentsEntréeÉlément > 2048) return 0;
            longueur = positionBase - lireCurseur + (valeur == 170 ? 12 + 4 * nombreÉlémentsEntréeÉlément : 8 + 8 * nombreÉlémentsEntréeÉlément);
        }
        if (valeur == 196 && lireCurseur + 1 < terminaison) {
            int donnéesMot = Fichier[lireCurseur + 1]; longueur = donnéesMot == 132 ? 6 : (donnéesMot == 21 || donnéesMot == 25 || donnéesMot == 54 || donnéesMot == 58) ? 4 : 0;
        }
        return longueur > 0 && longueur <= terminaison - lireCurseur ? longueur : 0;
    }
    static void contrôlerValeurDestination(int valeurDestination, int Fonction) {
        if (valeurDestination < démarrerMéthode[Fonction] || valeurDestination >= finMéthode[Fonction] || valeurFrontière[valeurDestination] != Fonction + 1) valeurÉchec("invalid branch target");
    }
    static void lireClasse(int définitionClasse) {
        classeAnalyséActuel = définitionClasse; lirePosition = définitionClasse * 16384; taille = lirePosition + tailleDéfinitionClasse[définitionClasse];
        if (Entier() != 0xcafebabe) { valeurÉchec("not a class file"); return; }
        int révisionMineur = valeurCourt(), valeurVersion = valeurCourt();
        if (valeurVersion < 45 || valeurVersion > 52 || révisionMineur != 0) { valeurÉchec("supported class versions: 45..52, minor 0"); return; }
        int nombreÉlémentsConstante = valeurCourt(), positionBase = définitionClasse * 512;
        if (nombreÉlémentsConstante < 1 || nombreÉlémentsConstante > 512) { valeurÉchec("constant pool limit (511)"); return; }
        for (int nombreÉlémentsEntréeÉlément = 1; nombreÉlémentsEntréeÉlément < nombreÉlémentsConstante && !erreur; nombreÉlémentsEntréeÉlément++) {
            int nombre = positionBase + nombreÉlémentsEntréeÉlément, valeurGenre = valeurOctet(); baliseConstante[nombre] = valeurGenre;
            if (valeurGenre == 1) { valeurDeuxièmeConstante[nombre] = valeurCourt(); valeurPremierConstante[nombre] = lirePosition; sauterOctets(valeurDeuxièmeConstante[nombre]); }
            else if (valeurGenre == 3) valeurPremierConstante[nombre] = Entier();
            else if (valeurGenre == 7 || valeurGenre == 8) valeurPremierConstante[nombre] = lireIndiceConstante();
            else if (valeurGenre == 9 || valeurGenre == 10 || valeurGenre == 11 || valeurGenre == 12) { valeurPremierConstante[nombre] = lireIndiceConstante(); valeurDeuxièmeConstante[nombre] = lireIndiceConstante(); }
            else valeurÉchec("unsupported constant type");
        }
        int valeurPermission = valeurCourt();
        if ((valeurPermission & (0x2000 | 0x4000)) != 0) valeurÉchec("annotation/enum class unsupported");
        nomDéfinitionClasse[définitionClasse] = texteNomClasse(lireIndiceConstante());
        parentDéfinitionClasse[définitionClasse] = texteNomClasse(lireIndiceConstante());
        int nombreÉlémentsInterface = valeurCourt(); if (nombreÉlémentsInterface > 16) { valeurÉchec("interface count limit"); return; }
        nombreÉlémentsInterfaceClasse[définitionClasse] = nombreÉlémentsInterface;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsInterface; indiceBoucle++) interfaceClasse[définitionClasse * 16 + indiceBoucle] = texteNomClasse(lireIndiceConstante());
        int nombreÉlémentsChamp = valeurCourt();
        if (nombreÉlémentsChamp > 512 - nombreÉlémentsEmplacement) { valeurÉchec("field count limit (512)"); return; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsChamp && !erreur; indiceBoucle++) {
            int indiceFichier = nombreÉlémentsEmplacement++; propriétaireEmplacement[indiceFichier] = définitionClasse; permissionsEmplacement[indiceFichier] = valeurCourt(); nomEmplacement[indiceFichier] = lireIndiceConstante(); typeEmplacement[indiceFichier] = lireIndiceConstante();
            contrôlerConstante(nomEmplacement[indiceFichier], 1); contrôlerConstante(typeEmplacement[indiceFichier], 1);
            int valeurPréservé = lirePosition; lirePosition = valeurPremierConstante[typeEmplacement[indiceFichier]]; int codeCatégorie = typeDescripteur(lirePosition + valeurDeuxièmeConstante[typeEmplacement[indiceFichier]], false); lirePosition = valeurPréservé;
            if ((permissionsEmplacement[indiceFichier] & 8) == 0) positionEmplacement[indiceFichier] = nombreÉlémentsEmplacementClasse[définitionClasse]++;
            int donnéesAttribut = valeurCourt();
            for (int positionInterne = 0; positionInterne < donnéesAttribut && !erreur; positionInterne++) {
                int constanteNom = lireIndiceConstante(), longueurValide = Entier();
                if (texteMot(constanteNom, "ConstantValue") && longueurValide == 2) {
                    int valeurDonnées = lireIndiceConstante();
                    if (codeCatégorie == 1 && contrôlerConstante(valeurDonnées, 3)) donnéesEmplacement[indiceFichier] = valeurPremierConstante[valeurDonnées];
                    else if (codeCatégorie == 2 && contrôlerConstante(valeurDonnées, 8)) donnéesEmplacement[indiceFichier] = texteConstante(valeurPremierConstante[valeurDonnées]);
                } else sauterOctets(longueurValide);
            }
        }
        int nombreÉlémentsÉlémentListe = valeurCourt();
        if (nombreÉlémentsÉlémentListe > 512 - nombreÉlémentsMéthode) { valeurÉchec("method count limit (512)"); return; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsÉlémentListe && !erreur; indiceBoucle++) {
            int nombre = nombreÉlémentsMéthode++; propriétaireMéthode[nombre] = définitionClasse;
            accèsMéthode[nombre] = valeurCourt(); texteNomMéthode[nombre] = lireIndiceConstante(); typeMéthode[nombre] = lireIndiceConstante();
            contrôlerConstante(texteNomMéthode[nombre], 1); lireDescripteur(nombre);
            if ((accèsMéthode[nombre] & 8) == 0) {
                if (nombreÉlémentsArgumentMéthode[nombre] == 16) { valeurÉchec("too many instance method arguments"); return; }
                for (int positionComparaison = nombreÉlémentsArgumentMéthode[nombre]; positionComparaison > 0; positionComparaison--) typeArgumentMéthode[nombre * 16 + positionComparaison] = typeArgumentMéthode[nombre * 16 + positionComparaison - 1];
                typeArgumentMéthode[nombre * 16] = 2; nombreÉlémentsArgumentMéthode[nombre]++;
            }
            if ((accèsMéthode[nombre] & 0x100) != 0) valeurÉchec("user native method unsupported");
            if (texteMot(texteNomMéthode[nombre], "<clinit>")) initialiserDéfinitionClasse[définitionClasse] = nombre + 1;
            for (int valeurAvantCôté = 0; valeurAvantCôté < nombre; valeurAvantCôté++) if (propriétaireMéthode[valeurAvantCôté] == définitionClasse && motConcordant(texteNomMéthode[valeurAvantCôté], texteNomMéthode[nombre]) && motConcordant(typeMéthode[valeurAvantCôté], typeMéthode[nombre])) valeurÉchec("duplicate method");
            int nombreÉlémentsAttribut = valeurCourt();
            for (int valeurAttribut = 0; valeurAttribut < nombreÉlémentsAttribut && !erreur; valeurAttribut++) {
                int nom = lireIndiceConstante(), longueur = Entier(), lancer = lirePosition;
                if (!rogner(lancer, longueur)) { valeurÉchec("truncated method attribute"); break; }
                if (texteMot(nom, "Code")) {
                    if (démarrerMéthode[nombre] != 0) valeurÉchec("duplicate Code attribute");
                    pileMéthode[nombre] = valeurCourt(); variablesLocalesMéthode[nombre] = valeurCourt(); int longueurCode = Entier();
                    if (pileMéthode[nombre] > 128 || variablesLocalesMéthode[nombre] > 128 || variablesLocalesMéthode[nombre] < nombreÉlémentsArgumentMéthode[nombre]
                        || longueurCode < 1 || longueurCode > 8192) valeurÉchec("method memory limits exceeded");
                    démarrerMéthode[nombre] = lirePosition; sauterOctets(longueurCode); finMéthode[nombre] = lirePosition;
                    int nombreÉlémentsInterceptionEnCours = valeurCourt();
                    if (nombreÉlémentsInterceptionEnCours > 1024 - intercepterNombreÉléments) { valeurÉchec("exception table limit"); return; }
                    for (int positionInterne = 0; positionInterne < nombreÉlémentsInterceptionEnCours; positionInterne++) {
                        int référenceErreur = intercepterNombreÉléments++; intercepterMéthode[référenceErreur] = nombre;
                        intercepterDémarrer[référenceErreur] = démarrerMéthode[nombre] + valeurCourt(); intercepterFin[référenceErreur] = démarrerMéthode[nombre] + valeurCourt();
                        intercepterPosition[référenceErreur] = démarrerMéthode[nombre] + valeurCourt(); int valeurEncodé = lireIndiceConstante(); intercepterClasse[référenceErreur] = valeurEncodé == 0 ? 0 : texteNomClasse(valeurEncodé);
                    }
                    sauterAttribut();
                    if (lirePosition != lancer + longueur) valeurÉchec("Code attribute size mismatch");
                } else sauterOctets(longueur);
            }
            if ((accèsMéthode[nombre] & 0x400) != 0) continue;
            if (démarrerMéthode[nombre] == 0) valeurÉchec("missing Code attribute");
            int entréeÉlémentEmplacement = démarrerMéthode[nombre];
            while (entréeÉlémentEmplacement < finMéthode[nombre] && !erreur) {
                int longueur = lireLongueur(entréeÉlémentEmplacement, démarrerMéthode[nombre], finMéthode[nombre]);
                if (longueur == 0) { valeurÉchec("unsupported or truncated bytecode"); break; }
                valeurFrontière[entréeÉlémentEmplacement] = nombre + 1; entréeÉlémentEmplacement += longueur;
            }
            entréeÉlémentEmplacement = démarrerMéthode[nombre];
            while (entréeÉlémentEmplacement < finMéthode[nombre] && !erreur) {
                int valeur = Fichier[entréeÉlémentEmplacement];
                if (valeur >= 153 && valeur <= 167 || valeur == 198 || valeur == 199) contrôlerValeurDestination(entréeÉlémentEmplacement + (short)(Fichier[entréeÉlémentEmplacement + 1] << 8 | Fichier[entréeÉlémentEmplacement + 2]), nombre);
                if (valeur == 200) contrôlerValeurDestination(entréeÉlémentEmplacement + entierPosition(entréeÉlémentEmplacement + 1), nombre);
                if (valeur == 170 || valeur == 171) {
                    int lireCurseur = entréeÉlémentEmplacement + 1; while ((lireCurseur - démarrerMéthode[nombre]) % 4 != 0) lireCurseur++;
                    contrôlerValeurDestination(entréeÉlémentEmplacement + entierPosition(lireCurseur), nombre);
                    int nombreÉlémentsEntréeÉlément = valeur == 170 ? entierPosition(lireCurseur + 8) - entierPosition(lireCurseur + 4) + 1 : entierPosition(lireCurseur + 4);
                    lireCurseur += valeur == 170 ? 12 : 8;
                    for (int positionInterne = 0; positionInterne < nombreÉlémentsEntréeÉlément; positionInterne++) contrôlerValeurDestination(entréeÉlémentEmplacement + entierPosition(lireCurseur + positionInterne * (valeur == 170 ? 4 : 8) + (valeur == 170 ? 0 : 4)), nombre);
                }
                entréeÉlémentEmplacement += lireLongueur(entréeÉlémentEmplacement, démarrerMéthode[nombre], finMéthode[nombre]);
            }
            for (int positionInterne = 0; positionInterne < intercepterNombreÉléments; positionInterne++) if (intercepterMéthode[positionInterne] == nombre) {
                contrôlerValeurDestination(intercepterDémarrer[positionInterne], nombre); contrôlerValeurDestination(intercepterPosition[positionInterne], nombre);
                if (intercepterFin[positionInterne] != finMéthode[nombre]) contrôlerValeurDestination(intercepterFin[positionInterne], nombre);
                if (intercepterDémarrer[positionInterne] >= intercepterFin[positionInterne]) valeurÉchec("invalid exception range");
            }
        }
        if (!erreur) sauterAttribut();
        if (lirePosition != taille) valeurÉchec("extra class file data");
    }
    static int allouerStockage(int valeurGenre, int longueur) { return mémoireNouveau(valeurGenre, longueur); }
    static boolean valeurObjet(int référence, int valeurGenre) {
        if (!estObjetValide(référence)) return false;
        if (valeurTas[référence] != valeurGenre) { valeurÉchec("object type mismatch"); return false; }
        return true;
    }
    static int texteConstante(int numéro) {
        if (!contrôlerConstante(numéro, 1)) return 0;
        if (référenceChaîne[numéro] != 0) return référenceChaîne[numéro];
        int référence = allouerStockage(1, valeurDeuxièmeConstante[numéro]); if (erreur) return 0;
        int terminaison = valeurPremierConstante[numéro] + valeurDeuxièmeConstante[numéro], nombre = valeurPremierConstante[numéro], longueur = 0;
        while (nombre < terminaison && !erreur) {
            int valeur = Fichier[nombre++];
            if (valeur == 0) valeurÉchec("invalid modified UTF-8");
            else if (valeur >= 192 && valeur <= 223 && nombre < terminaison) {
                int élémentListeSuivant = Fichier[nombre++];
                if ((élémentListeSuivant & 192) != 128) valeurÉchec("invalid modified UTF-8");
                valeur = (valeur & 31) << 6 | élémentListeSuivant & 63;
                if (valeur != 0 && valeur < 128) valeurÉchec("overlong modified UTF-8");
            } else if (valeur >= 224 && valeur <= 239 && nombre + 1 < terminaison) {
                int opérandePremier = Fichier[nombre++], opérandeDeuxième = Fichier[nombre++];
                if ((opérandePremier & 192) != 128 || (opérandeDeuxième & 192) != 128) valeurÉchec("invalid modified UTF-8");
                valeur = (valeur & 15) << 12 | (opérandePremier & 63) << 6 | opérandeDeuxième & 63;
                if (valeur < 2048) valeurÉchec("overlong modified UTF-8");
            } else if (valeur >= 128) valeurÉchec("invalid modified UTF-8");
            valeurTas[référence + 2 + longueur++] = valeur;
        }
        valeurTas[référence + 1] = longueur; référenceChaîne[numéro] = référence; return référence;
    }
    static int caractèreHôte(String valeur) {
        int référence = allouerStockage(1, valeur.length()); if (erreur) return 0;
        for (int nombre = 0; nombre < valeur.length(); nombre++) valeurTas[référence + 2 + nombre] = valeur.charAt(nombre);
        return référence;
    }
    static void écrireTexte(int référence) {
        if (référence == 0) { Utilisateur.écrire("null"); return; }
        if (!valeurObjet(référence, 1)) return;
        for (int nombre = 0; nombre < valeurTas[référence + 1]; nombre++) Utilisateur.écrireValeurCaractère(valeurTas[référence + 2 + nombre]);
    }
    static int caractèreChiffre(int valeur) {
        int référence = allouerStockage(1, 11); if (erreur) return 0;
        int longueur = 0;
        if (valeur < 0) valeurTas[référence + 2 + longueur++] = '-'; else valeur = -valeur;
        int indicePosition = 1000000000; boolean lancer = false;
        while (indicePosition != 0) {
            int nombre = -(valeur / indicePosition);
            if (nombre != 0 || lancer || indicePosition == 1) { valeurTas[référence + 2 + longueur++] = '0' + nombre; lancer = true; }
            valeur %= indicePosition; indicePosition /= 10;
        }
        valeurTas[référence + 1] = longueur; return référence;
    }
    static int décoderEntier(int référence) {
        if (!valeurObjet(référence, 1)) return 0;
        int longueur = valeurTas[référence + 1], nombre = 0, valeur = 0; boolean valeurNégatif = false;
        if (longueur > 0 && (valeurTas[référence + 2] == '-' || valeurTas[référence + 2] == '+')) { valeurNégatif = valeurTas[référence + 2] == '-'; nombre++; }
        if (nombre == longueur) valeurÉchec("NumberFormatException");
        for (; nombre < longueur && !erreur; nombre++) {
            int valeurChiffre = valeurTas[référence + 2 + nombre] - '0';
            if (valeurChiffre < 0 || valeurChiffre > 9 || valeur < -214748364 || valeur == -214748364 && valeurChiffre > (valeurNégatif ? 8 : 7)) valeurÉchec("NumberFormatException");
            valeur = valeur * 10 - valeurChiffre;
        }
        return valeurNégatif ? valeur : -valeur;
    }
    static void placerValeur(int valeur, int valeurType) {
        if (erreur) return;
        if (indiceCadre < 0 || pileCadre[indiceCadre] >= pileMéthode[méthodeCadre[indiceCadre]]) { valeurÉchec("operand stack overflow"); return; }
        int entréeÉlémentEmplacement = indiceCadre * 128 + pileCadre[indiceCadre]++; valeurPileOpérande[entréeÉlémentEmplacement] = valeur; typePileOpérande[entréeÉlémentEmplacement] = valeurType;
    }
    static int soustraireValeurs(int valeurType) {
        if (erreur) return 0;
        if (indiceCadre < 0 || pileCadre[indiceCadre] < 1) { valeurÉchec("operand stack underflow"); return 0; }
        int entréeÉlémentEmplacement = indiceCadre * 128 + --pileCadre[indiceCadre]; typeRetourner = typePileOpérande[entréeÉlémentEmplacement];
        if (valeurType != 0 && typeRetourner != valeurType) valeurÉchec("operand type mismatch");
        if (typeRetourner == 2) protégerValeur(valeurPileOpérande[entréeÉlémentEmplacement]);
        return valeurPileOpérande[entréeÉlémentEmplacement];
    }
    static void lireLocal(int numéro, int valeurType) {
        if (numéro >= variablesLocalesMéthode[méthodeCadre[indiceCadre]] || numéro < 0 || typeLocal[indiceCadre * 128 + numéro] != valeurType) { valeurÉchec("invalid or uninitialized local"); return; }
        placerValeur(valeurLocal[indiceCadre * 128 + numéro], valeurType);
    }
    static void écrireLocal(int numéro, int valeurType) {
        if (numéro >= variablesLocalesMéthode[méthodeCadre[indiceCadre]] || numéro < 0) { valeurÉchec("local index out of range"); return; }
        int valeur = soustraireValeurs(valeurType); valeurLocal[indiceCadre * 128 + numéro] = valeur; typeLocal[indiceCadre * 128 + numéro] = valeurType;
    }
    static int lireOctetCodeOpération() {
        int position = positionCadre[indiceCadre];
        if (position < démarrerMéthode[méthodeCadre[indiceCadre]] || position >= finMéthode[méthodeCadre[indiceCadre]]) { valeurÉchec("instruction pointer out of range"); return 0; }
        positionCadre[indiceCadre]++; return Fichier[position];
    }
    static int lireCourtCodeOpération() { return lireOctetCodeOpération() << 8 | lireOctetCodeOpération(); }
    static void valeurDéplacer(int position) {
        int Fonction = méthodeCadre[indiceCadre];
        if (position < démarrerMéthode[Fonction] || position >= finMéthode[Fonction] || valeurFrontière[position] != Fonction + 1) valeurÉchec("invalid branch target");
        else positionCadre[indiceCadre] = position;
    }
    static void invoquer(int Fonction) {
        if (indiceCadre % 32 == 31) { valeurÉchec("call stack limit (32)"); return; }
        int élémentListeSuivant = indiceCadre + 1;
        for (int nombre = 0; nombre < 128; nombre++) typeLocal[élémentListeSuivant * 128 + nombre] = 0;
        for (int nombre = nombreÉlémentsArgumentMéthode[Fonction] - 1; nombre >= 0; nombre--) {
            valeurLocal[élémentListeSuivant * 128 + nombre] = soustraireValeurs(typeArgumentMéthode[Fonction * 16 + nombre]); typeLocal[élémentListeSuivant * 128 + nombre] = typeArgumentMéthode[Fonction * 16 + nombre];
        }
        if (erreur) return;
        indiceCadre = élémentListeSuivant; initialiserCadre[indiceCadre] = 0; méthodeCadre[indiceCadre] = Fonction; positionCadre[indiceCadre] = démarrerMéthode[Fonction]; pileCadre[indiceCadre] = 0;
    }
    static void résultatRetourner(int valeurType) {
        if (valeurType != retournerMéthode[méthodeCadre[indiceCadre]]) { valeurÉchec("return type mismatch"); return; }
        int valeur = valeurType == 0 ? 0 : soustraireValeurs(valeurType);
        if (initialiserCadre[indiceCadre] != 0) étatValeurDéfinitionClasse[initialiserCadre[indiceCadre] - 1] = 2;
        if (verrouCadre[indiceCadre] != 0) { libérerVerrou(verrouCadre[indiceCadre]); verrouCadre[indiceCadre] = 0; }
        indiceCadre--; if (indiceCadre >= filExécutionActuel * 32 && valeurType != 0) placerValeur(valeur, valeurType);
    }
    static int[] nomFichierFlux = new int[64];
    static void appelFluxFichier(int valeurPropriétaire, int nom, int valeurFormat, int commande) {
        boolean Sortie = texteMot(valeurPropriétaire, "java/io/FileOutputStream");
        int valeurGenre = Sortie ? 6 : 5;
        if (commande == 183 && texteMot(nom, "<init>")) {
            boolean valeurContinuation = false;
            if (Sortie && texteMot(valeurFormat, "(Ljava/lang/String;Z)V")) valeurContinuation = soustraireValeurs(1) != 0;
            else if (!texteMot(valeurFormat, "(Ljava/lang/String;)V")) { valeurÉchec("unsupported file stream constructor"); return; }
            int nomEntréeÉlémentFichier = soustraireValeurs(2), valeurFlux = soustraireValeurs(2);
            if (!valeurObjet(nomEntréeÉlémentFichier, 1) || !valeurObjet(valeurFlux, valeurGenre) || erreur) return;
            if (valeurTas[valeurFlux + 3] != 0) { valeurÉchec("file stream already initialized"); return; }
            int longueur = valeurTas[nomEntréeÉlémentFichier + 1];
            if (longueur < 1 || longueur > 63) { valeurÉchec("invalid file name length"); return; }
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueur; entréeÉlémentEmplacement++) {
                int valeur = valeurTas[nomEntréeÉlémentFichier + 2 + entréeÉlémentEmplacement];
                if (valeur < 1) { valeurÉchec("invalid file stream path"); return; }
                nomFichierFlux[entréeÉlémentEmplacement] = valeur;
            }
            nomFichierFlux[longueur] = 0;
            int entréeÉlémentDescripteur = Utilisateur.ouvrirDescripteurFichier(nomFichierFlux, Sortie ? (valeurContinuation ? 1089 : 577) : 0);
            if (entréeÉlémentDescripteur < 0) { valeurÉchec("FileNotFoundException: file open failed"); return; }
            valeurTas[valeurFlux + 2] = entréeÉlémentDescripteur; valeurTas[valeurFlux + 3] = 1;
            return;
        }
        if (commande != 182) { valeurÉchec("invalid file stream invocation"); return; }
        if ((Sortie && texteMot(nom, "write") || !Sortie && texteMot(nom, "read"))
            && (texteMot(valeurFormat, Sortie ? "([B)V" : "([B)I") || texteMot(valeurFormat, Sortie ? "([BII)V" : "([BII)I"))) {
            boolean valeurRogner = texteMot(valeurFormat, Sortie ? "([BII)V" : "([BII)I");
            int nombreÉlémentsEntréeÉlément = valeurRogner ? soustraireValeurs(1) : 0, pointInitial = valeurRogner ? soustraireValeurs(1) : 0, tableauDonnées = soustraireValeurs(2), référenceObjet = soustraireValeurs(2);
            if (!valeurObjet(tableauDonnées, 20) || !valeurObjet(référenceObjet, valeurGenre)) return;
            if (!valeurRogner) nombreÉlémentsEntréeÉlément = valeurTas[tableauDonnées + 1];
            if (pointInitial < 0 || nombreÉlémentsEntréeÉlément < 0 || pointInitial > valeurTas[tableauDonnées + 1] - nombreÉlémentsEntréeÉlément) { leverException(6, "file buffer bounds"); return; }
            if (valeurTas[référenceObjet + 3] == 0 || valeurTas[référenceObjet + 2] < 0) { valeurÉchec("IOException: stream closed"); return; }
            int nombreÉlémentsAchevé = 0;
            while (nombreÉlémentsAchevé < nombreÉlémentsEntréeÉlément && !erreur) {
                int valeurRetourné = Sortie ? Utilisateur.écrireOctetFichierUn(valeurTas[référenceObjet + 2], valeurTas[tableauDonnées + 2 + pointInitial + nombreÉlémentsAchevé]) : Utilisateur.lireOctetFichierUn(valeurTas[référenceObjet + 2]);
                if (valeurRetourné < 0) { valeurÉchec(Sortie ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!Sortie && valeurRetourné == 256) break;
                if (!Sortie) valeurTas[tableauDonnées + 2 + pointInitial + nombreÉlémentsAchevé] = (byte)valeurRetourné;
                nombreÉlémentsAchevé++;
            }
            if (!Sortie) placerValeur(nombreÉlémentsEntréeÉlément != 0 && nombreÉlémentsAchevé == 0 ? -1 : nombreÉlémentsAchevé, 1);
            return;
        }
        if (Sortie && texteMot(nom, "flush") && texteMot(valeurFormat, "()V")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, valeurGenre) && valeurTas[référenceObjet + 2] < 0) valeurÉchec("IOException: stream closed"); return; }
        int action = -1, valeur = 0;
        if (texteMot(nom, "close") && texteMot(valeurFormat, "()V")) action = 0;
        if (!Sortie && texteMot(nom, "read") && texteMot(valeurFormat, "()I")) action = 1;
        if (Sortie && texteMot(nom, "write") && texteMot(valeurFormat, "(I)V")) { action = 2; valeur = soustraireValeurs(1); }
        if (action < 0) { valeurÉchec("unsupported file stream method"); return; }
        int valeurFlux = soustraireValeurs(2);
        if (!valeurObjet(valeurFlux, valeurGenre) || erreur) return;
        if (valeurTas[valeurFlux + 3] == 0) { valeurÉchec("uninitialized file stream"); return; }
        int entréeÉlémentDescripteur = valeurTas[valeurFlux + 2];
        if (action == 0) {
            if (entréeÉlémentDescripteur >= 0 && Utilisateur.fermerDescripteurFichier(entréeÉlémentDescripteur) < 0) valeurÉchec("IOException: close failed");
            valeurTas[valeurFlux + 2] = -1; return;
        }
        if (entréeÉlémentDescripteur < 0) { valeurÉchec("IOException: stream closed"); return; }
        if (action == 1) {
            int résultat = Utilisateur.lireOctetFichierUn(entréeÉlémentDescripteur);
            if (résultat < -1) valeurÉchec("IOException: read failed"); else placerValeur(résultat == 256 ? -1 : résultat, 1);
        } else if (Utilisateur.écrireOctetFichierUn(entréeÉlémentDescripteur, valeur) != 1) valeurÉchec("IOException: write failed");
    }
    static void appelMéthode(int numéro, int commande) {
        if (numéro <= 0 || numéro >= baliseConstante.length || (baliseConstante[numéro] != 10 && baliseConstante[numéro] != 11)) { valeurÉchec("invalid method reference"); return; }
        int valeurPropriétaire = texteNomClasse(valeurPremierConstante[numéro]), nom = nomRéférence(valeurDeuxièmeConstante[numéro]), valeurFormat = typeRéférence(valeurDeuxièmeConstante[numéro]);
        if (erreur) return;
        if (invoquerDéfaut(valeurPropriétaire, nom, valeurFormat, commande)) return;
        if (texteMot(valeurPropriétaire, "java/io/FileInputStream") || texteMot(valeurPropriétaire, "java/io/FileOutputStream")) {
            appelFluxFichier(valeurPropriétaire, nom, valeurFormat, commande); return;
        }
        if (commande == 184 && texteMot(valeurPropriétaire, "java/lang/Integer") && texteMot(nom, "parseInt") && texteMot(valeurFormat, "(Ljava/lang/String;)I")) {
            placerValeur(décoderEntier(soustraireValeurs(2)), 1); return;
        }
        if (commande == 182 && texteMot(valeurPropriétaire, "java/io/PrintStream") && (texteMot(nom, "println") || texteMot(nom, "print"))) {
            int valeurType = 0, valeur = 0;
            if (texteMot(valeurFormat, "(I)V")) { valeurType = 1; valeur = soustraireValeurs(1); }
            else if (texteMot(valeurFormat, "(Z)V")) { valeurType = 2; valeur = soustraireValeurs(1); }
            else if (texteMot(valeurFormat, "(C)V")) { valeurType = 3; valeur = soustraireValeurs(1); }
            else if (texteMot(valeurFormat, "(Ljava/lang/String;)V")) { valeurType = 4; valeur = soustraireValeurs(2); }
            else if (!texteMot(valeurFormat, "()V") || !texteMot(nom, "println")) valeurÉchec("unsupported print descriptor");
            if (soustraireValeurs(2) != -1) valeurÉchec("invalid PrintStream receiver");
            if (erreur) return;
            if (valeurType == 1) OutilJava.écrireNuméro(valeur);
            if (valeurType == 2) Utilisateur.écrire(valeur == 0 ? "false" : "true");
            if (valeurType == 3) Utilisateur.écrireValeurCaractère(valeur & 65535);
            if (valeurType == 4) écrireTexte(valeur);
            if (texteMot(nom, "println")) Utilisateur.écrireValeurCaractère(10);
            return;
        }
        if (commande == 182 && texteMot(valeurPropriétaire, "java/lang/String")) {
            if (texteMot(nom, "length") && texteMot(valeurFormat, "()I")) {
                int référence = soustraireValeurs(2); if (valeurObjet(référence, 1)) placerValeur(valeurTas[référence + 1], 1); return;
            }
            if (texteMot(nom, "charAt") && texteMot(valeurFormat, "(I)C")) {
                int valeurIndiceTableau = soustraireValeurs(1), référence = soustraireValeurs(2);
                if (valeurObjet(référence, 1)) {
                    if (valeurIndiceTableau < 0 || valeurIndiceTableau >= valeurTas[référence + 1]) valeurÉchec("StringIndexOutOfBoundsException"); else placerValeur(valeurTas[référence + 2 + valeurIndiceTableau], 1);
                }
                return;
            }
        }
        if (texteMot(valeurPropriétaire, "java/lang/StringBuilder")) {
            if (commande == 183 && texteMot(nom, "<init>") && texteMot(valeurFormat, "()V")) { valeurObjet(soustraireValeurs(2), 4); return; }
            if (commande == 182 && texteMot(nom, "toString") && texteMot(valeurFormat, "()Ljava/lang/String;")) {
                int référence = soustraireValeurs(2); if (valeurObjet(référence, 4)) placerValeur(valeurTas[référence + 2] == 0 ? caractèreHôte("") : valeurTas[référence + 2], 2); return;
            }
            if (commande == 182 && texteMot(nom, "append")) {
                int texte = 0;
                if (texteMot(valeurFormat, "(I)Ljava/lang/StringBuilder;")) texte = caractèreChiffre(soustraireValeurs(1));
                else if (texteMot(valeurFormat, "(Z)Ljava/lang/StringBuilder;")) texte = caractèreHôte(soustraireValeurs(1) == 0 ? "false" : "true");
                else if (texteMot(valeurFormat, "(C)Ljava/lang/StringBuilder;")) {
                    int valeur = soustraireValeurs(1); texte = allouerStockage(1, 1); if (!erreur) valeurTas[texte + 2] = valeur & 65535;
                }
                else if (texteMot(valeurFormat, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { texte = soustraireValeurs(2); if (texte == 0) texte = caractèreHôte("null"); }
                else { valeurÉchec("unsupported StringBuilder append"); return; }
                int référence = soustraireValeurs(2); if (!valeurObjet(référence, 4) || !valeurObjet(texte, 1)) return;
                int valeurAvantCôté = valeurTas[référence + 2], longueurValeurAvantCôté = valeurAvantCôté == 0 ? 0 : valeurTas[valeurAvantCôté + 1], longueurValeurRetourArrièreCôté = valeurTas[texte + 1];
                int texteNouveau = allouerStockage(1, longueurValeurAvantCôté + longueurValeurRetourArrièreCôté); if (erreur) return;
                for (int nombre = 0; nombre < longueurValeurAvantCôté; nombre++) valeurTas[texteNouveau + 2 + nombre] = valeurTas[valeurAvantCôté + 2 + nombre];
                for (int nombre = 0; nombre < longueurValeurRetourArrièreCôté; nombre++) valeurTas[texteNouveau + 2 + longueurValeurAvantCôté + nombre] = valeurTas[texte + 2 + nombre];
                valeurTas[référence + 2] = texteNouveau; placerValeur(référence, 2); return;
            }
        }
        int définitionClasse = trouverDéfinitionClasse(valeurPropriétaire); if (définitionClasse < 0 || erreur) return;
        int indiceFichier = trouverMéthode(définitionClasse, nom, valeurFormat);
        if (indiceFichier < 0) {
            for (int codeCaractère = définitionClasse, nombreÉlémentsEntréeÉlément = 0; codeCaractère >= 0 && nombreÉlémentsEntréeÉlément < 16; nombreÉlémentsEntréeÉlément++, codeCaractère = classeParent(codeCaractère))
                if (texteMot(parentDéfinitionClasse[codeCaractère], "java/lang/Thread")) { invoquerFilExécution(nom, valeurFormat, commande); return; }
            valeurÉchec("NoSuchMethodError"); return;
        }
        if (((accèsMéthode[indiceFichier] & 8) != 0) != (commande == 184)) { valeurÉchec("method static/instance mismatch"); return; }
        if (commande == 184) { if (!initialiser(propriétaireMéthode[indiceFichier], instructionMachineCadre[indiceCadre])) return; }
        else {
            int lireCurseur = pileCadre[indiceCadre] - nombreÉlémentsArgumentMéthode[indiceFichier];
            if (lireCurseur < 0 || typePileOpérande[indiceCadre * 128 + lireCurseur] != 2) { valeurÉchec("invalid method receiver"); return; }
            int référenceObjet = valeurPileOpérande[indiceCadre * 128 + lireCurseur];
            if (!estObjetValide(référenceObjet)) return;
            if (valeurTas[référenceObjet] < 32 || !classeContient(valeurTas[référenceObjet] - 32, valeurPropriétaire)) { valeurÉchec("method receiver type mismatch"); return; }
            if (commande != 183) indiceFichier = trouverMéthode(valeurTas[référenceObjet] - 32, nom, valeurFormat);
        }
        if (indiceFichier < 0 || (accèsMéthode[indiceFichier] & 0x400) != 0) { valeurÉchec("AbstractMethodError"); return; }
        int référenceVerrou = 0;
        if ((accèsMéthode[indiceFichier] & 32) != 0) {
            if (commande == 184) { int codeCaractère = propriétaireMéthode[indiceFichier]; if (verrouClasse[codeCaractère] == 0) verrouClasse[codeCaractère] = allouerStockage(8, 0); référenceVerrou = verrouClasse[codeCaractère]; }
            else référenceVerrou = valeurPileOpérande[indiceCadre * 128 + pileCadre[indiceCadre] - nombreÉlémentsArgumentMéthode[indiceFichier]];
            if (!acquérirVerrou(référenceVerrou)) { if (!erreur) positionCadre[indiceCadre] = instructionMachineCadre[indiceCadre]; return; }
        }
        invoquer(indiceFichier); if (!erreur) verrouCadre[indiceCadre] = référenceVerrou;
    }
    static boolean peutTableauStocker(int référenceTableau, int valeurDonnées) {
        if (valeurDonnées == 0 || élémentTableau[référenceTableau] == 0) return true;
        boolean estRéussi = élémentTableau[référenceTableau] == -1 ? (valeurDonnées > 0 && valeurDonnées < positionFinTas && valeurTas[valeurDonnées] == 1) : objetConcordant(valeurDonnées, élémentTableau[référenceTableau]);
        if (!estRéussi && !erreur) leverException(17, "array element type mismatch");
        return estRéussi;
    }
    static int emplacementTableau(int référence, int valeurIndiceTableau, int valeurType) {
        if (!valeurObjet(référence, valeurType)) return 0;
        if (valeurIndiceTableau < 0 || valeurIndiceTableau >= valeurTas[référence + 1]) { valeurÉchec("ArrayIndexOutOfBoundsException"); return 0; }
        return référence + 2 + valeurIndiceTableau;
    }
    static void exécuterCommande() {
        int donnéesResteDivision = 500000, valeurFragment = 100;
        while (true) {
            if (erreur) { if (objetLevé != 0) exceptionPoignée(); if (erreur || indiceCadre < filExécutionActuel * 32) break; }
            if (indiceCadre < filExécutionActuel * 32 || changerRequête || --valeurFragment == 0) { if (!filExécutionCommuter()) break; valeurFragment = 100; }
            if (indiceCadre == 0 && étatValeurDéfinitionClasse[définitionClasseEntréeÉlément] != 2 && !initialiser(définitionClasseEntréeÉlément, positionCadre[indiceCadre])) continue;
            if (indiceCadre == filExécutionActuel * 32 && filExécutionActuel != 0 && (accèsMéthode[méthodeCadre[indiceCadre]] & 32) != 0 && verrouCadre[indiceCadre] == 0) {
                int référenceObjet = cibleFilExécution[filExécutionActuel]; if (!acquérirVerrou(référenceObjet)) { if (erreur) break; continue; } verrouCadre[indiceCadre] = référenceObjet;
            }
            nombreÉlémentsTemporaire = 0;
            if (--donnéesResteDivision == 0) { valeurÉchec("instruction limit (500000)"); break; }
            int lancer = positionCadre[indiceCadre]; instructionMachineCadre[indiceCadre] = lancer; int valeur = lireOctetCodeOpération();
            if (erreur) break;
            if (valeur == 0) continue;
            if (valeur == 1) { placerValeur(0, 2); continue; }
            if (valeur >= 2 && valeur <= 8) { placerValeur(valeur - 3, 1); continue; }
            if (valeur == 16) { placerValeur((byte)lireOctetCodeOpération(), 1); continue; }
            if (valeur == 17) { placerValeur((short)lireCourtCodeOpération(), 1); continue; }
            if (valeur == 18 || valeur == 19) {
                int nombre = propriétaireMéthode[méthodeCadre[indiceCadre]] * 512 + (valeur == 18 ? lireOctetCodeOpération() : lireCourtCodeOpération());
                if (nombre <= 0 || nombre >= baliseConstante.length) valeurÉchec("invalid ldc constant");
                else if (baliseConstante[nombre] == 3) placerValeur(valeurPremierConstante[nombre], 1);
                else if (baliseConstante[nombre] == 8) placerValeur(texteConstante(valeurPremierConstante[nombre]), 2);
                else valeurÉchec("unsupported ldc constant");
                continue;
            }
            if (valeur == 21 || valeur == 25) { lireLocal(lireOctetCodeOpération(), valeur == 21 ? 1 : 2); continue; }
            if (valeur >= 26 && valeur <= 29) { lireLocal(valeur - 26, 1); continue; }
            if (valeur >= 42 && valeur <= 45) { lireLocal(valeur - 42, 2); continue; }
            if (valeur == 54 || valeur == 58) { écrireLocal(lireOctetCodeOpération(), valeur == 54 ? 1 : 2); continue; }
            if (valeur >= 59 && valeur <= 62) { écrireLocal(valeur - 59, 1); continue; }
            if (valeur >= 75 && valeur <= 78) { écrireLocal(valeur - 75, 2); continue; }
            if (valeur == 46 || valeur >= 50 && valeur <= 53) {
                int positionEntréeÉlément = soustraireValeurs(1), référenceObjet = soustraireValeurs(2), codeCatégorie = valeur == 46 ? 2 : valeur == 50 ? 3 : valeur == 51 ? 20 : valeur == 52 ? 22 : 23;
                if (valeur == 51 && référenceObjet > 0 && référenceObjet < positionFinTas && valeurTas[référenceObjet] == 21) codeCatégorie = 21;
                int lireCurseur = emplacementTableau(référenceObjet, positionEntréeÉlément, codeCatégorie); if (!erreur) placerValeur(valeurTas[lireCurseur], valeur == 50 ? 2 : 1); continue;
            }
            if (valeur == 79 || valeur >= 83 && valeur <= 86) {
                int référenceEntréeÉlément = soustraireValeurs(valeur == 83 ? 2 : 1), positionEntréeÉlément = soustraireValeurs(1), référenceObjet = soustraireValeurs(2), codeCatégorie = valeur == 79 ? 2 : valeur == 83 ? 3 : valeur == 84 ? 20 : valeur == 85 ? 22 : 23;
                if (valeur == 84 && référenceObjet > 0 && référenceObjet < positionFinTas && valeurTas[référenceObjet] == 21) codeCatégorie = 21;
                int lireCurseur = emplacementTableau(référenceObjet, positionEntréeÉlément, codeCatégorie);
                if (!erreur && codeCatégorie == 3 && !peutTableauStocker(référenceObjet, référenceEntréeÉlément)) continue;
                if (!erreur) valeurTas[lireCurseur] = codeCatégorie == 20 ? (byte)référenceEntréeÉlément : codeCatégorie == 21 ? référenceEntréeÉlément & 1 : codeCatégorie == 22 ? (char)référenceEntréeÉlément : codeCatégorie == 23 ? (short)référenceEntréeÉlément : référenceEntréeÉlément;
                continue;
            }
            if (valeur >= 87 && valeur <= 95) { instructionMachinePile(valeur); continue; }
            if (valeur == 96 || valeur == 100 || valeur == 104 || valeur == 108 || valeur == 112 || valeur == 120
                || valeur == 122 || valeur == 124 || valeur == 126 || valeur == 128 || valeur == 130) {
                int opérandeDeuxième = soustraireValeurs(1), opérandePremier = soustraireValeurs(1), résultat = 0;
                if ((valeur == 108 || valeur == 112) && opérandeDeuxième == 0) { valeurÉchec("ArithmeticException: / by zero"); continue; }
                if (valeur == 96) résultat = opérandePremier + opérandeDeuxième;
                if (valeur == 100) résultat = opérandePremier - opérandeDeuxième;
                if (valeur == 104) résultat = opérandePremier * opérandeDeuxième;
                if (valeur == 108) résultat = opérandePremier / opérandeDeuxième;
                if (valeur == 112) résultat = opérandePremier % opérandeDeuxième;
                if (valeur == 120) résultat = opérandePremier << opérandeDeuxième;
                if (valeur == 122) résultat = opérandePremier >> opérandeDeuxième;
                if (valeur == 124) résultat = opérandePremier >>> opérandeDeuxième;
                if (valeur == 126) résultat = opérandePremier & opérandeDeuxième;
                if (valeur == 128) résultat = opérandePremier | opérandeDeuxième;
                if (valeur == 130) résultat = opérandePremier ^ opérandeDeuxième;
                placerValeur(résultat, 1); continue;
            }
            if (valeur == 116) { placerValeur(-soustraireValeurs(1), 1); continue; }
            if (valeur == 132) {
                int portéeLocal = lireOctetCodeOpération(), étapeIncrément = (byte)lireOctetCodeOpération(); lireLocal(portéeLocal, 1); placerValeur(soustraireValeurs(1) + étapeIncrément, 1); écrireLocal(portéeLocal, 1); continue;
            }
            if (valeur >= 145 && valeur <= 147) {
                int nombre = soustraireValeurs(1); placerValeur(valeur == 145 ? (byte)nombre : valeur == 146 ? (char)nombre : (short)nombre, 1); continue;
            }
            if (valeur >= 153 && valeur <= 167 || valeur == 198 || valeur == 199) {
                int valeurDestination = lancer + (short)lireCourtCodeOpération(); boolean devraitPoursuivre = valeur == 167;
                if (valeur >= 153 && valeur <= 158) {
                    int nombre = soustraireValeurs(1); devraitPoursuivre = valeur == 153 ? nombre == 0 : valeur == 154 ? nombre != 0 : valeur == 155 ? nombre < 0 : valeur == 156 ? nombre >= 0 : valeur == 157 ? nombre > 0 : nombre <= 0;
                } else if (valeur >= 159 && valeur <= 166) {
                    int opérandeDeuxième = soustraireValeurs(valeur >= 165 ? 2 : 1), opérandePremier = soustraireValeurs(valeur >= 165 ? 2 : 1);
                    devraitPoursuivre = valeur == 159 || valeur == 165 ? opérandePremier == opérandeDeuxième : valeur == 160 || valeur == 166 ? opérandePremier != opérandeDeuxième : valeur == 161 ? opérandePremier < opérandeDeuxième : valeur == 162 ? opérandePremier >= opérandeDeuxième : valeur == 163 ? opérandePremier > opérandeDeuxième : opérandePremier <= opérandeDeuxième;
                } else if (valeur == 198 || valeur == 199) { int nombre = soustraireValeurs(2); devraitPoursuivre = valeur == 198 ? nombre == 0 : nombre != 0; }
                if (devraitPoursuivre) valeurDéplacer(valeurDestination); continue;
            }
            if (valeur == 172 || valeur == 176 || valeur == 177) { résultatRetourner(valeur == 172 ? 1 : valeur == 176 ? 2 : 0); continue; }
            if (valeur >= 178 && valeur <= 181) { invoquerChamp(lireConstanteCodeOpération(), valeur, lancer); continue; }
            if (valeur >= 182 && valeur <= 185) {
                int valeurEncodé = lireConstanteCodeOpération();
                if (valeur == 185) { int nombreÉlémentsTotal = lireOctetCodeOpération(); if (nombreÉlémentsTotal == 0 || lireOctetCodeOpération() != 0) { valeurÉchec("invalid invokeinterface operands"); continue; } }
                appelMéthode(valeurEncodé, valeur); continue;
            }
            if (valeur == 187) { objetNouveau(texteNomClasse(lireConstanteCodeOpération()), lancer); continue; }
            if (valeur == 188 || valeur == 189) {
                int codeCatégorie = 3, composant = 0;
                if (valeur == 188) { int donnéesTemporaire = lireOctetCodeOpération(); codeCatégorie = donnéesTemporaire == 10 ? 2 : donnéesTemporaire == 8 ? 20 : donnéesTemporaire == 4 ? 21 : donnéesTemporaire == 5 ? 22 : donnéesTemporaire == 9 ? 23 : 0; }
                else composant = texteNomClasse(lireConstanteCodeOpération());
                if (codeCatégorie == 0) { valeurÉchec("unsupported primitive array type"); continue; }
                int longueurValide = soustraireValeurs(1), référenceObjet = allouerStockage(codeCatégorie, longueurValide); if (!erreur) élémentTableau[référenceObjet] = composant; placerValeur(référenceObjet, 2); continue;
            }
            if (valeur == 190) {
                int référenceObjet = soustraireValeurs(2);
                if (estObjetValide(référenceObjet)) { int positionComparaison = valeurTas[référenceObjet]; if (positionComparaison != 2 && positionComparaison != 3 && (positionComparaison < 20 || positionComparaison > 23)) valeurÉchec("not an array"); else placerValeur(valeurTas[référenceObjet + 1], 1); }
                continue;
            }
            if (valeur == 191) {
                int référenceObjet = soustraireValeurs(2); if (estObjetValide(référenceObjet)) { if (valeurTas[référenceObjet] != 9) valeurÉchec("athrow requires supported Throwable"); else { objetLevé = référenceObjet; erreur = true; } }
                continue;
            }
            if (valeur == 192 || valeur == 193) {
                int constanteNom = texteNomClasse(lireConstanteCodeOpération()), référenceObjet = soustraireValeurs(2); boolean correspond = objetConcordant(référenceObjet, constanteNom);
                if (valeur == 193) placerValeur(référenceObjet != 0 && correspond ? 1 : 0, 1);
                else { if (!correspond && !erreur) valeurÉchec("ClassCastException"); placerValeur(référenceObjet, 2); }
                continue;
            }
            if (valeur == 170 || valeur == 171) {
                int lireCurseur = lancer + 1, indiceFichier = méthodeCadre[indiceCadre], référenceTouche = soustraireValeurs(1);
                while ((lireCurseur - démarrerMéthode[indiceFichier]) % 4 != 0) lireCurseur++;
                int adresseCible = entierPosition(lireCurseur);
                if (valeur == 170) { int valeurBas = entierPosition(lireCurseur + 4), valeurHaut = entierPosition(lireCurseur + 8); if (référenceTouche >= valeurBas && référenceTouche <= valeurHaut) adresseCible = entierPosition(lireCurseur + 12 + (référenceTouche - valeurBas) * 4); }
                else { int nombreÉlémentsTotal = entierPosition(lireCurseur + 4); for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsTotal; indiceBoucle++) if (entierPosition(lireCurseur + 8 + indiceBoucle * 8) == référenceTouche) adresseCible = entierPosition(lireCurseur + 12 + indiceBoucle * 8); }
                valeurDéplacer(lancer + adresseCible); continue;
            }
            if (valeur == 200) { valeurDéplacer(lancer + entierPosition(lancer + 1)); continue; }
            if (valeur == 194 || valeur == 195) {
                int référenceObjet = soustraireValeurs(2);
                if (valeur == 195) libérerVerrou(référenceObjet);
                else if (!acquérirVerrou(référenceObjet) && !erreur) { placerValeur(référenceObjet, 2); positionCadre[indiceCadre] = lancer; }
                continue;
            }
            if (valeur == 196) {
                int codeCommande = lireOctetCodeOpération(), positionEntréeÉlément = lireCourtCodeOpération();
                if (codeCommande == 21 || codeCommande == 25) lireLocal(positionEntréeÉlément, codeCommande == 21 ? 1 : 2);
                else if (codeCommande == 54 || codeCommande == 58) écrireLocal(positionEntréeÉlément, codeCommande == 54 ? 1 : 2);
                else if (codeCommande == 132) { int valeurVariation = (short)lireCourtCodeOpération(); lireLocal(positionEntréeÉlément, 1); placerValeur(soustraireValeurs(1) + valeurVariation, 1); écrireLocal(positionEntréeÉlément, 1); }
                else valeurÉchec("unsupported wide opcode");
                continue;
            }
            valeurÉchec("unsupported bytecode");
        }
    }
    static int trouverDéfinitionClasse(int nom) {
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsDéfinitionClasse; indiceBoucle++) if (nomDéfinitionClasse[indiceBoucle] != 0 && motConcordant(nomDéfinitionClasse[indiceBoucle], nom)) return indiceBoucle;
        return chargerDéfinitionClasse(texteConstante(nom));
    }
    static int chargerDéfinitionClasse(int chaîneNom) {
        if (!valeurObjet(chaîneNom, 1)) return -1;
        int longueur = valeurTas[chaîneNom + 1];
        if (longueur < 1 || longueur > 505 || nombreÉlémentsDéfinitionClasse == 16) { valeurÉchec("class name/count limit"); return -1; }
        for (int indiceBoucle = 0; indiceBoucle < longueur; indiceBoucle++) { int codeCaractère = valeurTas[chaîneNom + 2 + indiceBoucle]; texteNomFichier[indiceBoucle] = codeCaractère == '/' ? '.' : codeCaractère; }
        texteNomFichier[longueur] = '.'; texteNomFichier[longueur + 1] = 'c'; texteNomFichier[longueur + 2] = 'l'; texteNomFichier[longueur + 3] = 'a'; texteNomFichier[longueur + 4] = 's'; texteNomFichier[longueur + 5] = 's'; texteNomFichier[longueur + 6] = 0;
        int taille = Utilisateur.lireFichier(texteNomFichier, fichierTemporaire);
        if (taille < 0) { valeurÉchec("ClassNotFoundException"); return -1; }
        int définitionClasse = nombreÉlémentsDéfinitionClasse++; tailleDéfinitionClasse[définitionClasse] = taille;
        for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) Fichier[définitionClasse * 16384 + indiceBoucle] = fichierTemporaire[indiceBoucle];
        lireClasse(définitionClasse); if (erreur) return -1;
        int donnéesEffectif = texteConstante(nomDéfinitionClasse[définitionClasse]);
        if (!égalTextes(donnéesEffectif, chaîneNom, true)) { valeurÉchec("class name does not match file"); return -1; }
        int valeurParent = parentDéfinitionClasse[définitionClasse];
        if (valeurParent != 0 && !texteMot(valeurParent, "java/lang/Object") && !texteMot(valeurParent, "java/lang/Thread")) {
            // Une classe déjà enregistrée n’est pas rechargée ; les cycles d’héritage sont toutefois explicitement refusés.
            int valeurSommet = trouverDéfinitionClasse(valeurParent);
            if (erreur || valeurSommet < 0) return -1;
            int lireCurseur = valeurSommet, nombreÉlémentsÉtapePhase = 0;
            while (lireCurseur >= 0 && nombreÉlémentsÉtapePhase++ < 16) {
                if (lireCurseur == définitionClasse) { valeurÉchec("cyclic inheritance"); return -1; }
                lireCurseur = classeParent(lireCurseur);
            }
            int démarrerDéplacement = nombreÉlémentsEmplacementClasse[valeurSommet];
            for (int indiceFichier = 0; indiceFichier < nombreÉlémentsEmplacement; indiceFichier++) if (propriétaireEmplacement[indiceFichier] == définitionClasse && (permissionsEmplacement[indiceFichier] & 8) == 0) positionEmplacement[indiceFichier] += démarrerDéplacement;
            nombreÉlémentsEmplacementClasse[définitionClasse] += démarrerDéplacement;
        }
        return définitionClasse;
    }
    static int classeParent(int définitionClasse) {
        int nom = parentDéfinitionClasse[définitionClasse];
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsDéfinitionClasse; indiceBoucle++) if (nom != 0 && nomDéfinitionClasse[indiceBoucle] != 0 && motConcordant(nomDéfinitionClasse[indiceBoucle], nom)) return indiceBoucle;
        return -1;
    }
    static int trouverMéthode(int définitionClasse, int nom, int valeurFormat) {
        for (int valeurProfondeur = 0; définitionClasse >= 0 && valeurProfondeur < 16; valeurProfondeur++, définitionClasse = classeParent(définitionClasse)) {
            for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsMéthode; indiceBoucle++) if (propriétaireMéthode[indiceBoucle] == définitionClasse && motConcordant(texteNomMéthode[indiceBoucle], nom) && motConcordant(typeMéthode[indiceBoucle], valeurFormat)) return indiceBoucle;
        }
        return -1;
    }
    static int méthodeNom(int définitionClasse, String nom, String valeurFormat) {
        for (int valeurProfondeur = 0; définitionClasse >= 0 && valeurProfondeur < 16; valeurProfondeur++, définitionClasse = classeParent(définitionClasse))
            for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsMéthode; indiceBoucle++) if (propriétaireMéthode[indiceBoucle] == définitionClasse && texteMot(texteNomMéthode[indiceBoucle], nom) && texteMot(typeMéthode[indiceBoucle], valeurFormat)) return indiceBoucle;
        return -1;
    }
    static int genreType(int nom) { return Fichier[valeurPremierConstante[nom]] == 'L' || Fichier[valeurPremierConstante[nom]] == '[' ? 2 : 1; }
    static boolean initialiser(int définitionClasse, int démarrerCommande) {
        if (définitionClasse < 0 || erreur) return false;
        if (étatValeurDéfinitionClasse[définitionClasse] == 3) { valeurÉchec("NoClassDefFoundError: initialization failed"); return false; }
        if (étatValeurDéfinitionClasse[définitionClasse] == 1 && filExécutionClasse[définitionClasse] != filExécutionActuel) { positionCadre[indiceCadre] = démarrerCommande; changerRequête = true; return false; }
        if (étatValeurDéfinitionClasse[définitionClasse] != 0) return true;
        int valeurSommet = classeParent(définitionClasse);
        if (valeurSommet >= 0 && !initialiser(valeurSommet, démarrerCommande)) return false;
        étatValeurDéfinitionClasse[définitionClasse] = 1; filExécutionClasse[définitionClasse] = filExécutionActuel;
        if (initialiserDéfinitionClasse[définitionClasse] != 0) {
            positionCadre[indiceCadre] = démarrerCommande;
            invoquer(initialiserDéfinitionClasse[définitionClasse] - 1); if (!erreur) initialiserCadre[indiceCadre] = définitionClasse + 1;
            return false;
        }
        étatValeurDéfinitionClasse[définitionClasse] = 2; return true;
    }
    static void invoquerChamp(int numéro, int commande, int lancer) {
        if (!contrôlerConstante(numéro, 9)) return;
        int valeurPropriétaire = texteNomClasse(valeurPremierConstante[numéro]), nom = nomRéférence(valeurDeuxièmeConstante[numéro]), valeurFormat = typeRéférence(valeurDeuxièmeConstante[numéro]);
        if (texteMot(valeurPropriétaire, "java/lang/System") && (texteMot(nom, "out") || texteMot(nom, "err")) && texteMot(valeurFormat, "Ljava/io/PrintStream;") && commande == 178) { placerValeur(-1, 2); return; }
        int définitionClasse = trouverDéfinitionClasse(valeurPropriétaire); if (définitionClasse < 0 || erreur) return;
        int valeurTrouvé = -1;
        for (int lireCurseur = définitionClasse, valeurProfondeur = 0; lireCurseur >= 0 && valeurProfondeur < 16 && valeurTrouvé < 0; valeurProfondeur++, lireCurseur = classeParent(lireCurseur))
            for (int indiceFichier = 0; indiceFichier < nombreÉlémentsEmplacement; indiceFichier++) if (propriétaireEmplacement[indiceFichier] == lireCurseur && motConcordant(nomEmplacement[indiceFichier], nom) && motConcordant(typeEmplacement[indiceFichier], valeurFormat)) valeurTrouvé = indiceFichier;
        if (valeurTrouvé < 0) { valeurÉchec("NoSuchFieldError"); return; }
        boolean valeurStatique = commande == 178 || commande == 179;
        if (valeurStatique != ((permissionsEmplacement[valeurTrouvé] & 8) != 0)) { valeurÉchec("field static/instance mismatch"); return; }
        if (valeurStatique && !initialiser(propriétaireEmplacement[valeurTrouvé], lancer)) return;
        int valeurType = genreType(valeurFormat), valeur = 0;
        if (commande == 179 || commande == 181) valeur = soustraireValeurs(valeurType);
        if (valeurStatique) { if (commande == 178) placerValeur(donnéesEmplacement[valeurTrouvé], valeurType); else if (!erreur) donnéesEmplacement[valeurTrouvé] = valeur; return; }
        int référenceObjet = soustraireValeurs(2);
        if (!estObjetValide(référenceObjet)) return;
        if (valeurTas[référenceObjet] < 32 || !classeContient(valeurTas[référenceObjet] - 32, valeurPropriétaire)) { valeurÉchec("field receiver type mismatch"); return; }
        int emplacementPréservé = référenceObjet + 2 + positionEmplacement[valeurTrouvé];
        if (commande == 180) placerValeur(valeurTas[emplacementPréservé], valeurType);
        else if (!erreur) { valeurTas[emplacementPréservé] = valeur; référenceTas[emplacementPréservé] = valeurType == 2 ? 1 : 0; }
    }
    static boolean classeContient(int définitionClasse, int nom) {
        for (int profondeur = 0; définitionClasse >= 0 && profondeur < 16; profondeur++, définitionClasse = classeParent(définitionClasse)) {
            if (motConcordant(nomDéfinitionClasse[définitionClasse], nom) || (parentDéfinitionClasse[définitionClasse] != 0 && motConcordant(parentDéfinitionClasse[définitionClasse], nom))) return true;
            for (int positionInterne = 0; positionInterne < nombreÉlémentsInterfaceClasse[définitionClasse]; positionInterne++) if (motConcordant(interfaceClasse[définitionClasse * 16 + positionInterne], nom)) return true;
        }
        return false;
    }
    static boolean égalTextes(int donnéesPremier, int donnéesOctet, boolean chemin) {
        if (donnéesPremier == donnéesOctet) return true;
        if (donnéesPremier <= 0 || donnéesOctet <= 0 || valeurTas[donnéesPremier] != 1 || valeurTas[donnéesOctet] != 1 || valeurTas[donnéesPremier + 1] != valeurTas[donnéesOctet + 1]) return false;
        for (int indiceBoucle = 0; indiceBoucle < valeurTas[donnéesPremier + 1]; indiceBoucle++) {
            int coordonnéeCoordonnéeHorizontale = valeurTas[donnéesPremier + 2 + indiceBoucle], coordonnéeCoordonnéeVerticale = valeurTas[donnéesOctet + 2 + indiceBoucle];
            if (chemin) { if (coordonnéeCoordonnéeHorizontale == '.') coordonnéeCoordonnéeHorizontale = '/'; if (coordonnéeCoordonnéeVerticale == '.') coordonnéeCoordonnéeVerticale = '/'; }
            if (coordonnéeCoordonnéeHorizontale != coordonnéeCoordonnéeVerticale) return false;
        }
        return true;
    }
    static boolean estObjetValide(int référenceObjet) {
        if (référenceObjet == 0) { valeurÉchec("NullPointerException"); return false; }
        if (référenceObjet < 1 || référenceObjet >= positionFinTas || largeurTas[référenceObjet] < 2 || valeurTas[référenceObjet] == 0) { valeurÉchec("invalid object reference"); return false; }
        return true;
    }
    static void protégerValeur(int référenceObjet) {
        if (référenceObjet > 0 && référenceObjet < positionFinTas && largeurTas[référenceObjet] >= 2 && nombreÉlémentsTemporaire < référenceTemporaire.length) référenceTemporaire[nombreÉlémentsTemporaire++] = référenceObjet;
    }
    static void afficherValeur(int référenceObjet) {
        if (référenceObjet > 0 && référenceObjet < positionFinTas && largeurTas[référenceObjet] >= 2 && valeurTas[référenceObjet] != 0 && marqueTas[référenceObjet] == 0) {
            marqueTas[référenceObjet] = 1; attendrePrésenterPour[nombreÉlémentsPrésenter++] = référenceObjet;
        }
    }
    static void collecterDéchets() {
        nombreÉlémentsPrésenter = 0; nombreÉlémentsCollection++;
        for (int contrôlerPosition = 1; contrôlerPosition < positionFinTas; contrôlerPosition += largeurTas[contrôlerPosition]) marqueTas[contrôlerPosition] = 0;
        for (int indiceBoucle = 0; indiceBoucle < référenceChaîne.length; indiceBoucle++) afficherValeur(référenceChaîne[indiceBoucle]);
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEmplacement; indiceBoucle++) if ((permissionsEmplacement[indiceBoucle] & 8) != 0 && genreType(typeEmplacement[indiceBoucle]) == 2) afficherValeur(donnéesEmplacement[indiceBoucle]);
        for (int donnéesTemporaire = 0; donnéesTemporaire < nombreÉlémentsFilExécution; donnéesTemporaire++) {
            afficherValeur(objetFilExécution[donnéesTemporaire]); afficherValeur(cibleFilExécution[donnéesTemporaire]);
            int positionSommet = donnéesTemporaire == filExécutionActuel ? indiceCadre : cadreFilExécution[donnéesTemporaire];
            for (int indiceFichier = donnéesTemporaire * 32; indiceFichier <= positionSommet; indiceFichier++) {
                for (int positionInterne = 0; positionInterne < variablesLocalesMéthode[méthodeCadre[indiceFichier]]; positionInterne++) if (typeLocal[indiceFichier * 128 + positionInterne] == 2) afficherValeur(valeurLocal[indiceFichier * 128 + positionInterne]);
                for (int positionInterne = 0; positionInterne < pileCadre[indiceFichier]; positionInterne++) if (typePileOpérande[indiceFichier * 128 + positionInterne] == 2) afficherValeur(valeurPileOpérande[indiceFichier * 128 + positionInterne]);
            }
        }
        for (int indiceBoucle = 0; indiceBoucle < référenceÉcran.length; indiceBoucle++) afficherValeur(référenceÉcran[indiceBoucle]);
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsUltérieur; indiceBoucle++) afficherValeur(ultérieurPlanification[indiceBoucle]);
        for (int indiceBoucle = 0; indiceBoucle < entierStocker.length; indiceBoucle++) afficherValeur(entierStocker[indiceBoucle]);
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsDéfinitionClasse; indiceBoucle++) afficherValeur(verrouClasse[indiceBoucle]);
        for (int contrôlerPosition = 1; contrôlerPosition < positionFinTas; contrôlerPosition += largeurTas[contrôlerPosition]) if (profondeurVerrou[contrôlerPosition] > 0) afficherValeur(contrôlerPosition);
        afficherValeur(objetLevé);
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsTemporaire; indiceBoucle++) afficherValeur(référenceTemporaire[indiceBoucle]);
        while (nombreÉlémentsPrésenter > 0) {
            int référenceObjet = attendrePrésenterPour[--nombreÉlémentsPrésenter], codeCatégorie = valeurTas[référenceObjet];
            for (int indiceBoucle = référenceObjet + 2; indiceBoucle < référenceObjet + largeurTas[référenceObjet]; indiceBoucle++) if (codeCatégorie == 3 || codeCatégorie == 4 || référenceTas[indiceBoucle] != 0) afficherValeur(valeurTas[indiceBoucle]);
        }
        for (int contrôlerPosition = 1; contrôlerPosition < positionFinTas; contrôlerPosition += largeurTas[contrôlerPosition]) if (marqueTas[contrôlerPosition] == 0) valeurTas[contrôlerPosition] = 0;
        for (int contrôlerPosition = 1; contrôlerPosition < positionFinTas; contrôlerPosition += largeurTas[contrôlerPosition]) if (valeurTas[contrôlerPosition] == 0) {
            while (contrôlerPosition + largeurTas[contrôlerPosition] < positionFinTas && valeurTas[contrôlerPosition + largeurTas[contrôlerPosition]] == 0) { int positionSuivant = contrôlerPosition + largeurTas[contrôlerPosition]; largeurTas[contrôlerPosition] += largeurTas[positionSuivant]; largeurTas[positionSuivant] = 0; }
            if (contrôlerPosition + largeurTas[contrôlerPosition] == positionFinTas) { positionFinTas = contrôlerPosition; break; }
        }
    }
    static int mémoireNouveau(int valeurGenre, int longueur) {
        if (longueur < 0) { valeurÉchec("NegativeArraySizeException"); return 0; }
        if (longueur > valeurTas.length - 3) { valeurÉchec("object heap exhausted"); return 0; }
        int nombreÉlémentsRequis = longueur + 2, référenceObjet = 0;
        if (nombreÉlémentsRequis <= valeurTas.length - positionFinTas) { référenceObjet = positionFinTas; positionFinTas += nombreÉlémentsRequis; }
        else {
            collecterDéchets();
            for (int lireCurseur = 1; lireCurseur < positionFinTas; lireCurseur += largeurTas[lireCurseur]) if (valeurTas[lireCurseur] == 0 && largeurTas[lireCurseur] >= nombreÉlémentsRequis) { référenceObjet = lireCurseur; break; }
            if (référenceObjet != 0) {
                int longueurRestant = largeurTas[référenceObjet] - nombreÉlémentsRequis;
                if (longueurRestant >= 2) { largeurTas[référenceObjet + nombreÉlémentsRequis] = longueurRestant; valeurTas[référenceObjet + nombreÉlémentsRequis] = 0; }
                else nombreÉlémentsRequis += longueurRestant;
            } else if (nombreÉlémentsRequis <= valeurTas.length - positionFinTas) { référenceObjet = positionFinTas; positionFinTas += nombreÉlémentsRequis; }
        }
        if (référenceObjet == 0) { valeurÉchec("object heap exhausted"); return 0; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsRequis; indiceBoucle++) { valeurTas[référenceObjet + indiceBoucle] = 0; référenceTas[référenceObjet + indiceBoucle] = 0; largeurTas[référenceObjet + indiceBoucle] = 0; }
        élémentTableau[référenceObjet] = 0;
        largeurTas[référenceObjet] = nombreÉlémentsRequis; valeurTas[référenceObjet] = valeurGenre; valeurTas[référenceObjet + 1] = longueur; protégerValeur(référenceObjet); return référenceObjet;
    }
    static int classeException(String constanteNom) {
        if (OutilJava.texteÉgal(constanteNom, "java/lang/Throwable")) return 1;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/Exception")) return 2;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/RuntimeException")) return 3;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/ArithmeticException")) return 4;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/NullPointerException")) return 5;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/IndexOutOfBoundsException")) return 6;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/IllegalArgumentException")) return 9;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/NumberFormatException")) return 10;
        if (OutilJava.texteÉgal(constanteNom, "java/io/IOException")) return 11;
        if (OutilJava.texteÉgal(constanteNom, "java/io/FileNotFoundException")) return 12;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/IllegalStateException")) return 13;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/ClassCastException")) return 14;
        if (OutilJava.texteÉgal(constanteNom, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int constanteException(int nom) {
        for (int indiceBoucle = 1; indiceBoucle <= 41; indiceBoucle++) if (texteMot(nom, nomException(indiceBoucle))) return indiceBoucle;
        return 0;
    }
    static String nomException(int valeurIdentité) {
        if (valeurIdentité == 40) return "java/lang/InterruptedException";
        if (valeurIdentité == 41) return "français/interne/ExceptionInterrompuAttendre";
        if (valeurIdentité == 39) return "java/net/SocketException";
        if (valeurIdentité == 20) return "français/interne/exception";
        if (valeurIdentité == 21) return "français/interne/ExceptionExécution";
        if (valeurIdentité == 22) return "français/interne/ExceptionSortieEntrée";
        if (valeurIdentité == 23) return "français/interne/ExceptionDélaiExpirationAttendre";
        if (valeurIdentité == 24) return "français/interne/ExceptionRechercherAdresse";
        if (valeurIdentité == 25) return "français/interne/ExceptionFichierManquant";
        if (valeurIdentité == 26) return "français/interne/ExceptionCommunication";
        if (valeurIdentité == 27) return "français/interne/ExceptionArgumentInvalide";
        if (valeurIdentité == 28) return "français/interne/ÉchecFormatNuméro";
        if (valeurIdentité == 29) return "français/interne/ExceptionBornes";
        if (valeurIdentité == 30) return "français/interne/ExceptionBornesTableau";
        if (valeurIdentité == 31) return "français/interne/ExceptionBornesChaîne";
        if (valeurIdentité == 32) return "français/interne/ExceptionRéférenceRéférenceNulle";
        if (valeurIdentité == 33) return "français/interne/ÉchecArithmétique";
        if (valeurIdentité == 34) return "français/interne/ExceptionÉtatValeur";
        if (valeurIdentité == 35) return "français/interne/ExceptionConversionTypeType";
        if (valeurIdentité == 36) return "français/interne/ÉchecTailleTableauNégatif";
        if (valeurIdentité == 37) return "français/interne/ÉchecStockerTableau";
        if (valeurIdentité == 38) return "français/interne/ExceptionÉtatValeurFilExécution";
        if (valeurIdentité == 1) return "java/lang/Throwable"; if (valeurIdentité == 2) return "java/lang/Exception";
        if (valeurIdentité == 3) return "java/lang/RuntimeException"; if (valeurIdentité == 4) return "java/lang/ArithmeticException";
        if (valeurIdentité == 5) return "java/lang/NullPointerException"; if (valeurIdentité == 6) return "java/lang/IndexOutOfBoundsException";
        if (valeurIdentité == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (valeurIdentité == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (valeurIdentité == 9) return "java/lang/IllegalArgumentException"; if (valeurIdentité == 10) return "java/lang/NumberFormatException";
        if (valeurIdentité == 11) return "java/io/IOException"; if (valeurIdentité == 12) return "java/io/FileNotFoundException";
        if (valeurIdentité == 17) return "java/lang/ArrayStoreException";
        if (valeurIdentité == 18) return "java/net/UnknownHostException";
        if (valeurIdentité == 19) return "java/net/SocketTimeoutException";
        if (valeurIdentité == 16) return "java/lang/IllegalThreadStateException";
        if (valeurIdentité == 13) return "java/lang/IllegalStateException"; if (valeurIdentité == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int parentException(int valeurIdentité) {
        if (valeurIdentité == 40) return 2;
        if (valeurIdentité == 41) return 40;
        if (valeurIdentité == 39) return 11;
        if (valeurIdentité == 1) return 0;
        if (valeurIdentité == 2) return 1;
        if (valeurIdentité == 3) return 2;
        if (valeurIdentité == 4) return 3;
        if (valeurIdentité == 5) return 3;
        if (valeurIdentité == 6) return 3;
        if (valeurIdentité == 7) return 6;
        if (valeurIdentité == 8) return 6;
        if (valeurIdentité == 9) return 3;
        if (valeurIdentité == 10) return 9;
        if (valeurIdentité == 11) return 2;
        if (valeurIdentité == 12) return 11;
        if (valeurIdentité == 13) return 3;
        if (valeurIdentité == 14) return 3;
        if (valeurIdentité == 15) return 3;
        if (valeurIdentité == 16) return 9;
        if (valeurIdentité == 17) return 3;
        if (valeurIdentité == 18) return 11;
        if (valeurIdentité == 19) return 11;
        if (valeurIdentité == 20) return 2;
        if (valeurIdentité == 21) return 3;
        if (valeurIdentité == 22) return 11;
        if (valeurIdentité == 23) return 22;
        if (valeurIdentité == 24) return 22;
        if (valeurIdentité == 25) return 22;
        if (valeurIdentité == 26) return 22;
        if (valeurIdentité == 27) return 9;
        if (valeurIdentité == 28) return 27;
        if (valeurIdentité == 29) return 6;
        if (valeurIdentité == 30) return 29;
        if (valeurIdentité == 31) return 29;
        if (valeurIdentité == 32) return 5;
        if (valeurIdentité == 33) return 4;
        if (valeurIdentité == 34) return 13;
        if (valeurIdentité == 35) return 14;
        if (valeurIdentité == 36) return 15;
        if (valeurIdentité == 37) return 17;
        if (valeurIdentité == 38) return 16;
        return 0;
    }
    static boolean exceptionContient(int valeurEffectif, int souhaité) {
        for (int valeurProfondeur = 0; valeurEffectif != 0 && valeurProfondeur < 16; valeurProfondeur++, valeurEffectif = parentException(valeurEffectif))
            if (valeurEffectif == souhaité) return true;
        return false;
    }
    static void leverException(int valeurIdentité, String référenceLisezMoi) {
        int référenceObjet = mémoireNouveau(9, 2); if (erreur) return;
        valeurTas[référenceObjet + 2] = valeurIdentité; valeurTas[référenceObjet + 3] = caractèreHôte(référenceLisezMoi); référenceTas[référenceObjet + 3] = 1;
        objetLevé = référenceObjet; erreur = true;
    }
    static boolean objetConcordant(int référenceObjet, int nom) {
        if (référenceObjet == 0) return true;
        if (!estObjetValide(référenceObjet)) return false;
        int codeCatégorie = valeurTas[référenceObjet];
        if (texteMot(nom, "java/lang/Object")) return true;
        if (codeCatégorie >= 32) return classeContient(codeCatégorie - 32, nom);
        if (codeCatégorie == 9) { int adresseCible = constanteException(nom); return adresseCible != 0 && exceptionContient(valeurTas[référenceObjet + 2], adresseCible); }
        if (codeCatégorie == 1) return texteMot(nom, "java/lang/String") || texteMot(nom, "java/lang/CharSequence");
        if (codeCatégorie == 4) return texteMot(nom, "java/lang/StringBuilder") || texteMot(nom, "java/lang/CharSequence");
        if (codeCatégorie == 10) return texteMot(nom, "java/util/ArrayList") || texteMot(nom, "java/util/List");
        if (codeCatégorie == 11) return texteMot(nom, "java/util/HashMap") || texteMot(nom, "java/util/Map");
        if (codeCatégorie == 12) return texteMot(nom, "java/lang/Integer") || texteMot(nom, "java/lang/Number");
        if (codeCatégorie >= 24 && codeCatégorie <= 28 && valeurTas[référenceObjet + 13] != 0) return classeÉcranCoréen(nom) == codeCatégorie || texteMot(nom, "français/interne/ÉlémentÉcran");
        if (codeCatégorie >= 24 && codeCatégorie <= 28) return (classeÉcranCoréen(nom) == 0 && classeÉcran(nom) == codeCatégorie) || texteMot(nom, "java/awt/Component") || texteMot(nom, "java/awt/Container") || texteMot(nom, "javax/swing/JComponent");
        if (codeCatégorie == 29) return texteMot(nom, valeurTas[référenceObjet + 3] != 0 ? "français/interne/NotificationAction" : "java/awt/event/ActionEvent");
        if (codeCatégorie == 30) return texteMot(nom, "java/awt/FlowLayout") || texteMot(nom, "java/awt/LayoutManager");
        if (codeCatégorie == 17) return texteMot(nom, "java/net/Socket");
        if (codeCatégorie == 18) return texteMot(nom, "java/net/ServerSocket");
        if (codeCatégorie == 19) return texteMot(nom, valeurTas[référenceObjet + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (codeCatégorie == 14) return texteMot(nom, "java/net/InetAddress");
        if (codeCatégorie == 15) return texteMot(nom, "java/net/DatagramSocket");
        if (codeCatégorie == 16) return texteMot(nom, "java/net/DatagramPacket");
        if (codeCatégorie == 13) return texteMot(nom, valeurTas[référenceObjet + 3] != 0 ? "français/interne/tâcheFond" : "java/lang/Thread");
        if (codeCatégorie == 2) return texteMot(nom, "[I"); if (codeCatégorie == 20) return texteMot(nom, "[B"); if (codeCatégorie == 21) return texteMot(nom, "[Z");
        if (codeCatégorie == 22) return texteMot(nom, "[C"); if (codeCatégorie == 23) return texteMot(nom, "[S");
        if (codeCatégorie != 3) return false;
        if (texteMot(nom, "[Ljava/lang/Object;")) return true;
        int composant = élémentTableau[référenceObjet];
        if (composant == -1) return texteMot(nom, "[Ljava/lang/String;") || texteMot(nom, "[Ljava/lang/CharSequence;");
        if (composant == 0) return false;
        if (comparerClassesTableau(composant, nom)) return true;
        if ((texteMot(composant, "java/lang/String") || texteMot(composant, "java/lang/StringBuilder")) && texteMot(nom, "[Ljava/lang/CharSequence;")) return true;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsDéfinitionClasse; indiceBoucle++) if (motConcordant(nomDéfinitionClasse[indiceBoucle], composant)) {
            for (int codeCaractère = indiceBoucle, profondeur = 0; codeCaractère >= 0 && profondeur < 16; profondeur++, codeCaractère = classeParent(codeCaractère)) {
                if (comparerClassesTableau(parentDéfinitionClasse[codeCaractère], nom)) return true;
                for (int positionInterne = 0; positionInterne < nombreÉlémentsInterfaceClasse[codeCaractère]; positionInterne++) if (comparerClassesTableau(interfaceClasse[codeCaractère * 16 + positionInterne], nom)) return true;
            }
        }
        return false;
    }
    static boolean comparerClassesTableau(int constanteNom, int descripteur) {
        int contrôlerPosition = valeurPremierConstante[descripteur], nombreÉlémentsEntréeÉlément = valeurDeuxièmeConstante[descripteur];
        if (constanteNom == 0 || nombreÉlémentsEntréeÉlément < 4 || Fichier[contrôlerPosition] != '[' || Fichier[contrôlerPosition + 1] != 'L' || Fichier[contrôlerPosition + nombreÉlémentsEntréeÉlément - 1] != ';' || valeurDeuxièmeConstante[constanteNom] != nombreÉlémentsEntréeÉlément - 3) return false;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément - 3; indiceBoucle++) if (Fichier[valeurPremierConstante[constanteNom] + indiceBoucle] != Fichier[contrôlerPosition + 2 + indiceBoucle]) return false;
        return true;
    }
    static void exceptionPoignée() {
        if (objetLevé == 0) return;
        erreur = false;
        while (indiceCadre >= filExécutionActuel * 32) {
            int indiceFichier = méthodeCadre[indiceCadre], lireCurseur = instructionMachineCadre[indiceCadre];
            for (int indiceBoucle = 0; indiceBoucle < intercepterNombreÉléments; indiceBoucle++) if (intercepterMéthode[indiceBoucle] == indiceFichier && lireCurseur >= intercepterDémarrer[indiceBoucle] && lireCurseur < intercepterFin[indiceBoucle]
                && (intercepterClasse[indiceBoucle] == 0 || objetConcordant(objetLevé, intercepterClasse[indiceBoucle]))) {
                positionCadre[indiceCadre] = intercepterPosition[indiceBoucle]; pileCadre[indiceCadre] = 0; placerValeur(objetLevé, 2); objetLevé = 0; return;
            }
            if (initialiserCadre[indiceCadre] != 0) étatValeurDéfinitionClasse[initialiserCadre[indiceCadre] - 1] = 3;
            if (verrouCadre[indiceCadre] != 0) { libérerVerrou(verrouCadre[indiceCadre]); verrouCadre[indiceCadre] = 0; }
            indiceCadre--;
        }
        Utilisateur.écrire("Uncaught ");
        if (valeurTas[objetLevé] == 9) { Utilisateur.écrire(nomException(valeurTas[objetLevé + 2])); Utilisateur.écrire(": "); écrireTexte(valeurTas[objetLevé + 3]); }
        else Utilisateur.écrire("user exception");
        Utilisateur.écrireValeurCaractère(10); objetLevé = 0; erreur = true;
    }
    // Cette JVM n’accepte actuellement que les éléments de pile category-1 (int/reference).
    static void instructionMachinePile(int codeCommande) {
        int donnéesPremier = soustraireValeurs(0), formatPremier = typeRetourner;
        if (codeCommande == 87) return;
        if (codeCommande == 89) { placerValeur(donnéesPremier, formatPremier); placerValeur(donnéesPremier, formatPremier); return; }
        int donnéesOctet = soustraireValeurs(0), formatDeuxième = typeRetourner;
        if (codeCommande == 88) return;
        if (codeCommande == 90) { placerValeur(donnéesPremier, formatPremier); placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); return; }
        if (codeCommande == 92) { placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); return; }
        if (codeCommande == 95) { placerValeur(donnéesPremier, formatPremier); placerValeur(donnéesOctet, formatDeuxième); return; }
        int codeCaractère = soustraireValeurs(0), formatTroisième = typeRetourner;
        if (codeCommande == 91) { placerValeur(donnéesPremier, formatPremier); placerValeur(codeCaractère, formatTroisième); placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); return; }
        if (codeCommande == 93) { placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); placerValeur(codeCaractère, formatTroisième); placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); return; }
        int valeurFinalPosition = soustraireValeurs(0), formatQuatrième = typeRetourner;
        placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier); placerValeur(valeurFinalPosition, formatQuatrième); placerValeur(codeCaractère, formatTroisième); placerValeur(donnéesOctet, formatDeuxième); placerValeur(donnéesPremier, formatPremier);
    }
    static void objetNouveau(int constanteNom, int pointInitial) {
        int codeCatégorie = 0, longueurValide = 0, référenceException = constanteException(constanteNom);
        if (texteMot(constanteNom, "java/lang/StringBuilder")) { codeCatégorie = 4; longueurValide = 1; }
        if (texteMot(constanteNom, "java/io/FileInputStream")) { codeCatégorie = 5; longueurValide = 2; }
        if (texteMot(constanteNom, "java/io/FileOutputStream")) { codeCatégorie = 6; longueurValide = 2; }
        if (référenceException != 0) { codeCatégorie = 9; longueurValide = 2; }
        if (texteMot(constanteNom, "java/util/ArrayList")) { codeCatégorie = 10; longueurValide = 2; }
        if (texteMot(constanteNom, "java/util/HashMap")) { codeCatégorie = 11; longueurValide = 2; }
        if (texteMot(constanteNom, "java/lang/Integer")) { codeCatégorie = 12; longueurValide = 1; }
        if (texteMot(constanteNom, "java/net/Socket")) { codeCatégorie = 17; longueurValide = 5; }
        if (texteMot(constanteNom, "java/net/ServerSocket")) { codeCatégorie = 18; longueurValide = 5; }
        if (texteMot(constanteNom, "java/net/DatagramSocket")) { codeCatégorie = 15; longueurValide = 3; }
        if (texteMot(constanteNom, "java/net/DatagramPacket")) { codeCatégorie = 16; longueurValide = 4; }
        if (texteMot(constanteNom, "java/lang/Thread") || texteMot(constanteNom, "français/interne/tâcheFond")) { codeCatégorie = 13; longueurValide = 2; }
        if (texteMot(constanteNom, "java/lang/Object")) { codeCatégorie = 8; }
        if (codeCatégorie == 0 && classeÉcran(constanteNom) != 0) { codeCatégorie = classeÉcran(constanteNom); longueurValide = 12; }
        if (codeCatégorie == 0) {
            int codeCaractère = trouverDéfinitionClasse(constanteNom); if (codeCaractère < 0 || erreur || !initialiser(codeCaractère, pointInitial)) return;
            codeCatégorie = 32 + codeCaractère; longueurValide = nombreÉlémentsEmplacementClasse[codeCaractère];
        }
        int référenceObjet = allouerStockage(codeCatégorie, longueurValide); if (erreur) return;
        if (codeCatégorie == 13 && texteMot(constanteNom, "français/interne/tâcheFond")) valeurTas[référenceObjet + 3] = 1;
        if (codeCatégorie >= 24 && codeCatégorie <= 28 && classeÉcranCoréen(constanteNom) != 0) valeurTas[référenceObjet + 13] = 1;
        if (codeCatégorie == 5 || codeCatégorie == 6 || codeCatégorie == 15 || codeCatégorie == 17 || codeCatégorie == 18) valeurTas[référenceObjet + 2] = -1;
        if (codeCatégorie == 9) valeurTas[référenceObjet + 2] = référenceException;
        placerValeur(référenceObjet, 2);
    }
    static boolean égalValeurs(int donnéesPremier, int donnéesOctet) {
        if (donnéesPremier == donnéesOctet) return true;
        if (donnéesPremier == 0 || donnéesOctet == 0 || donnéesPremier < 0 || donnéesOctet < 0 || donnéesPremier >= positionFinTas || donnéesOctet >= positionFinTas) return false;
        if (valeurTas[donnéesPremier] == 1 && valeurTas[donnéesOctet] == 1) return égalTextes(donnéesPremier, donnéesOctet, false);
        return valeurTas[donnéesPremier] == 12 && valeurTas[donnéesOctet] == 12 && valeurTas[donnéesPremier + 2] == valeurTas[donnéesOctet + 2];
    }
    static int fragmentTexte(int référenceObjet, int démarrerPosition, int positionFin) {
        if (!valeurObjet(référenceObjet, 1)) return 0;
        if (démarrerPosition < 0 || positionFin < démarrerPosition || positionFin > valeurTas[référenceObjet + 1]) { valeurÉchec("StringIndexOutOfBoundsException"); return 0; }
        int valeurRetourné = allouerStockage(1, positionFin - démarrerPosition); if (erreur) return 0;
        for (int indiceBoucle = démarrerPosition; indiceBoucle < positionFin; indiceBoucle++) valeurTas[valeurRetourné + 2 + indiceBoucle - démarrerPosition] = valeurTas[référenceObjet + 2 + indiceBoucle];
        return valeurRetourné;
    }
    static int joindreTexte(int donnéesPremier, int donnéesOctet) {
        if (!valeurObjet(donnéesPremier, 1) || !valeurObjet(donnéesOctet, 1)) return 0;
        int nombreÉlémentsEntréeÉlément = valeurTas[donnéesPremier + 1], indiceMéthode = valeurTas[donnéesOctet + 1], valeurRetourné = allouerStockage(1, nombreÉlémentsEntréeÉlément + indiceMéthode); if (erreur) return 0;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) valeurTas[valeurRetourné + 2 + indiceBoucle] = valeurTas[donnéesPremier + 2 + indiceBoucle];
        for (int indiceBoucle = 0; indiceBoucle < indiceMéthode; indiceBoucle++) valeurTas[valeurRetourné + 2 + nombreÉlémentsEntréeÉlément + indiceBoucle] = valeurTas[donnéesOctet + 2 + indiceBoucle];
        return valeurRetourné;
    }
    static boolean invoquerDéfaut(int propriétaire, int constanteNom, int constanteDescripteur, int codeCommande) {
        if (texteMot(propriétaire, "français/interne/Arguments") && codeCommande == 184) {
            if (texteMot(constanteNom, "nombreÉlémentsÉlémentListe") && texteMot(constanteDescripteur, "()I")) { placerValeur(Utilisateur.nombreÉlémentsArguments() - 1, 1); return true; }
            if (texteMot(constanteNom, "texte") && texteMot(constanteDescripteur, "(I)Ljava/lang/String;")) {
                int indiceOrdinal = soustraireValeurs(1);
                if (indiceOrdinal < 0 || indiceOrdinal >= Utilisateur.nombreÉlémentsArguments() - 1) leverException(29, "exécuterCommande arguments 범위를 벗어났습니다");
                else placerValeur(caractèreHôte(Utilisateur.arguments(indiceOrdinal + 1)), 2);
                return true;
            }
            valeurÉchec("지원하지 않는 français exécuterCommande arguments invoquer"); return true;
        }
        if (texteMot(propriétaire, "français/interne/tâcheFond")) { filExécutionProcessus(constanteNom, constanteDescripteur, codeCommande, true); return true; }
        if (propriétaireÉcranCoréen(propriétaire)) { invoquerÉcranCoréen(propriétaire, constanteNom, constanteDescripteur, codeCommande); return true; }
        if (propriétaireÉcran(propriétaire)) { invoquerÉcran(propriétaire, constanteNom, constanteDescripteur, codeCommande); return true; }
        if (texteMot(propriétaire, "java/net/Socket") || texteMot(propriétaire, "java/net/ServerSocket") || texteMot(propriétaire, "java/io/InputStream") || texteMot(propriétaire, "java/io/OutputStream")) { invoquerFlux(propriétaire, constanteNom, constanteDescripteur, codeCommande); return true; }
        if (texteMot(propriétaire, "français/interne/valeurNoyau") && codeCommande == 184) {
            if (texteMot(constanteNom, "largeurÉcran") && texteMot(constanteDescripteur, "()I")) { placerValeur(Utilisateur.largeurÉcran(), 1); return true; }
            if (texteMot(constanteNom, "hauteurÉcran") && texteMot(constanteDescripteur, "()I")) { placerValeur(Utilisateur.hauteurÉcran(), 1); return true; }
            if (texteMot(constanteNom, "millisecondes") && texteMot(constanteDescripteur, "()I")) { placerValeur(Utilisateur.millisecondes(), 1); return true; }
            if (texteMot(constanteNom, "attendreImagePour") && texteMot(constanteDescripteur, "()I")) { placerValeur(Utilisateur.attendreImagePour(), 1); return true; }
            if (texteMot(constanteNom, "rectangle") && texteMot(constanteDescripteur, "(IIIII)I")) { int couleurPixel = soustraireValeurs(1), valeurHauteur = soustraireValeurs(1), valeurLargeur = soustraireValeurs(1), coordonnéeCoordonnéeVerticale = soustraireValeurs(1), coordonnéeCoordonnéeHorizontale = soustraireValeurs(1); placerValeur(Utilisateur.rectangle(coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale, valeurLargeur, valeurHauteur, couleurPixel), 1); return true; }
        }
        if (texteMot(propriétaire, "java/net/InetAddress") || texteMot(propriétaire, "java/net/DatagramPacket") || texteMot(propriétaire, "java/net/DatagramSocket")) { invoquerRéseau(propriétaire, constanteNom, constanteDescripteur, codeCommande); return true; }
        if (texteMot(propriétaire, "java/lang/Thread")) { invoquerFilExécution(constanteNom, constanteDescripteur, codeCommande); return true; }
        if (texteMot(propriétaire, "java/lang/Object")) {
            if (texteMot(constanteNom, "<init>") && texteMot(constanteDescripteur, "()V") && codeCommande == 183) { estObjetValide(soustraireValeurs(2)); return true; }
            if (texteMot(constanteNom, "equals") && texteMot(constanteDescripteur, "(Ljava/lang/Object;)Z")) { int donnéesOctet = soustraireValeurs(2), donnéesPremier = soustraireValeurs(2); if (estObjetValide(donnéesPremier)) placerValeur(donnéesPremier == donnéesOctet ? 1 : 0, 1); return true; }
        }
        if (constanteException(propriétaire) != 0) {
            if (texteMot(constanteNom, "<init>") && codeCommande == 183 && (texteMot(constanteDescripteur, "()V") || texteMot(constanteDescripteur, "(Ljava/lang/String;)V"))) {
                int invite = texteMot(constanteDescripteur, "()V") ? 0 : soustraireValeurs(2), référenceObjet = soustraireValeurs(2);
                if (valeurObjet(référenceObjet, 9)) { valeurTas[référenceObjet + 3] = invite; référenceTas[référenceObjet + 3] = 1; } return true;
            }
            if ((texteMot(constanteNom, "getMessage") || texteMot(constanteNom, "description")) && texteMot(constanteDescripteur, "()Ljava/lang/String;")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 9)) placerValeur(valeurTas[référenceObjet + 3], 2); return true; }
        }
        if (texteMot(propriétaire, "java/lang/String")) {
            if (codeCommande == 182 && texteMot(constanteNom, "getBytes") && (texteMot(constanteDescripteur, "()[B") || texteMot(constanteDescripteur, "(Ljava/lang/String;)[B"))) {
                int nomEncodage = texteMot(constanteDescripteur, "()[B") ? 0 : soustraireValeurs(2), référenceObjet = soustraireValeurs(2);
                if (!valeurObjet(référenceObjet, 1)) return true;
                if (nomEncodage != 0 && !égalTextes(nomEncodage, caractèreHôte("UTF-8"), false) && !égalTextes(nomEncodage, caractèreHôte("UTF8"), false) && !égalTextes(nomEncodage, caractèreHôte("utf-8"), false)) { leverException(11, "only UTF-8 encoding is supported"); return true; }
                int nombreÉlémentsEntréeÉlément = valeurTas[référenceObjet + 1], valeurRetourné = allouerStockage(20, nombreÉlémentsEntréeÉlément * 3), nombreÉlémentsUtilisé = 0; if (erreur) return true;
                for (int positionInterne = 0; positionInterne < nombreÉlémentsEntréeÉlément; positionInterne++) {
                    int codeCaractère = valeurTas[référenceObjet + 2 + positionInterne];
                    if (codeCaractère >= 0xd800 && codeCaractère <= 0xdbff && positionInterne + 1 < nombreÉlémentsEntréeÉlément && valeurTas[référenceObjet + 3 + positionInterne] >= 0xdc00 && valeurTas[référenceObjet + 3 + positionInterne] <= 0xdfff) codeCaractère = 0x10000 + ((codeCaractère - 0xd800) << 10) + valeurTas[référenceObjet + 2 + ++positionInterne] - 0xdc00;
                    else if (codeCaractère >= 0xd800 && codeCaractère <= 0xdfff) codeCaractère = '?';
                    if (codeCaractère < 128) valeurTas[valeurRetourné + 2 + nombreÉlémentsUtilisé++] = codeCaractère;
                    else { int nombreÉlémentsOctet = codeCaractère < 2048 ? 2 : codeCaractère < 65536 ? 3 : 4; valeurTas[valeurRetourné + 2 + nombreÉlémentsUtilisé++] = (byte)((nombreÉlémentsOctet == 2 ? 192 : nombreÉlémentsOctet == 3 ? 224 : 240) | codeCaractère >> (6 * (nombreÉlémentsOctet - 1))); for (int positionComparaison = nombreÉlémentsOctet - 1; positionComparaison > 0; positionComparaison--) valeurTas[valeurRetourné + 2 + nombreÉlémentsUtilisé++] = (byte)(128 | codeCaractère >> (6 * (positionComparaison - 1)) & 63); }
                }
                valeurTas[valeurRetourné + 1] = nombreÉlémentsUtilisé; placerValeur(valeurRetourné, 2); return true;
            }
            if (codeCommande == 184 && texteMot(constanteNom, "valueOf") && texteMot(constanteDescripteur, "(I)Ljava/lang/String;")) { placerValeur(caractèreChiffre(soustraireValeurs(1)), 2); return true; }
            if (codeCommande != 182) return false;
            if (texteMot(constanteNom, "equals") && texteMot(constanteDescripteur, "(Ljava/lang/Object;)Z")) { int donnéesOctet = soustraireValeurs(2), donnéesPremier = soustraireValeurs(2); if (valeurObjet(donnéesPremier, 1)) placerValeur(égalTextes(donnéesPremier, donnéesOctet, false) ? 1 : 0, 1); return true; }
            if (texteMot(constanteNom, "isEmpty") && texteMot(constanteDescripteur, "()Z")) { int donnéesPremier = soustraireValeurs(2); if (valeurObjet(donnéesPremier, 1)) placerValeur(valeurTas[donnéesPremier + 1] == 0 ? 1 : 0, 1); return true; }
            if (texteMot(constanteNom, "substring") && (texteMot(constanteDescripteur, "(I)Ljava/lang/String;") || texteMot(constanteDescripteur, "(II)Ljava/lang/String;"))) {
                boolean valeurDeuxième = texteMot(constanteDescripteur, "(II)Ljava/lang/String;"); int positionFin = valeurDeuxième ? soustraireValeurs(1) : 0, pointInitial = soustraireValeurs(1), donnéesPremier = soustraireValeurs(2);
                if (valeurObjet(donnéesPremier, 1)) placerValeur(fragmentTexte(donnéesPremier, pointInitial, valeurDeuxième ? positionFin : valeurTas[donnéesPremier + 1]), 2); return true;
            }
            if (texteMot(constanteNom, "concat") && texteMot(constanteDescripteur, "(Ljava/lang/String;)Ljava/lang/String;")) { int donnéesOctet = soustraireValeurs(2), donnéesPremier = soustraireValeurs(2); placerValeur(joindreTexte(donnéesPremier, donnéesOctet), 2); return true; }
            if (texteMot(constanteNom, "hashCode") && texteMot(constanteDescripteur, "()I")) { int donnéesPremier = soustraireValeurs(2), valeurHachage = 0; if (valeurObjet(donnéesPremier, 1)) { for (int indiceBoucle = 0; indiceBoucle < valeurTas[donnéesPremier + 1]; indiceBoucle++) valeurHachage = valeurHachage * 31 + valeurTas[donnéesPremier + 2 + indiceBoucle]; placerValeur(valeurHachage, 1); } return true; }
            if (texteMot(constanteNom, "toString") && texteMot(constanteDescripteur, "()Ljava/lang/String;")) { int donnéesPremier = soustraireValeurs(2); if (valeurObjet(donnéesPremier, 1)) placerValeur(donnéesPremier, 2); return true; }
        }
        if (texteMot(propriétaire, "java/lang/Integer")) {
            if (codeCommande == 184 && texteMot(constanteNom, "valueOf") && texteMot(constanteDescripteur, "(I)Ljava/lang/Integer;")) { int valeurDonnées = soustraireValeurs(1), référenceObjet = valeurDonnées >= -128 && valeurDonnées <= 127 ? entierStocker[valeurDonnées + 128] : 0; if (référenceObjet == 0) { référenceObjet = allouerStockage(12, 1); if (!erreur) { valeurTas[référenceObjet + 2] = valeurDonnées; if (valeurDonnées >= -128 && valeurDonnées <= 127) entierStocker[valeurDonnées + 128] = référenceObjet; } } placerValeur(référenceObjet, 2); return true; }
            if (codeCommande == 183 && texteMot(constanteNom, "<init>") && texteMot(constanteDescripteur, "(I)V")) { int valeurDonnées = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 12)) valeurTas[référenceObjet + 2] = valeurDonnées; return true; }
            if (codeCommande == 182 && texteMot(constanteNom, "intValue") && texteMot(constanteDescripteur, "()I")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 12)) placerValeur(valeurTas[référenceObjet + 2], 1); return true; }
            if (codeCommande == 184 && texteMot(constanteNom, "toString") && texteMot(constanteDescripteur, "(I)Ljava/lang/String;")) { placerValeur(caractèreChiffre(soustraireValeurs(1)), 2); return true; }
        }
        if (texteMot(propriétaire, "java/lang/Math") && codeCommande == 184) {
            if (texteMot(constanteNom, "abs") && texteMot(constanteDescripteur, "(I)I")) { int lireValeur = soustraireValeurs(1); placerValeur(lireValeur < 0 ? -lireValeur : lireValeur, 1); return true; }
            if ((texteMot(constanteNom, "min") || texteMot(constanteNom, "max")) && texteMot(constanteDescripteur, "(II)I")) { int donnéesOctet = soustraireValeurs(1), donnéesPremier = soustraireValeurs(1); placerValeur(texteMot(constanteNom, "min") ? (donnéesPremier < donnéesOctet ? donnéesPremier : donnéesOctet) : (donnéesPremier > donnéesOctet ? donnéesPremier : donnéesOctet), 1); return true; }
        }
        if (texteMot(propriétaire, "java/lang/System") && codeCommande == 184) {
            if (texteMot(constanteNom, "gc") && texteMot(constanteDescripteur, "()V")) { collecterDéchets(); return true; }
            if (texteMot(constanteNom, "arraycopy") && texteMot(constanteDescripteur, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int nombreÉlémentsEntréeÉlément = soustraireValeurs(1), indiceValeurDestination = soustraireValeurs(1), donnéesOctet = soustraireValeurs(2), démarrerPosition = soustraireValeurs(1), donnéesPremier = soustraireValeurs(2);
                if (estObjetValide(donnéesPremier) && estObjetValide(donnéesOctet)) {
                    int codeCatégorie = valeurTas[donnéesPremier];
                    if (valeurTas[donnéesOctet] != codeCatégorie || (codeCatégorie != 2 && codeCatégorie != 3 && (codeCatégorie < 20 || codeCatégorie > 23))) valeurÉchec("arraycopy type mismatch");
                    else if (nombreÉlémentsEntréeÉlément < 0 || démarrerPosition < 0 || indiceValeurDestination < 0 || démarrerPosition > valeurTas[donnéesPremier + 1] - nombreÉlémentsEntréeÉlément || indiceValeurDestination > valeurTas[donnéesOctet + 1] - nombreÉlémentsEntréeÉlément) valeurÉchec("ArrayIndexOutOfBoundsException");
                    else if (donnéesPremier == donnéesOctet && indiceValeurDestination > démarrerPosition) { for (int indiceBoucle = nombreÉlémentsEntréeÉlément - 1; indiceBoucle >= 0; indiceBoucle--) valeurTas[donnéesOctet + 2 + indiceValeurDestination + indiceBoucle] = valeurTas[donnéesPremier + 2 + démarrerPosition + indiceBoucle]; }
                    else { for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément && !erreur; indiceBoucle++) { int valeurDonnées = valeurTas[donnéesPremier + 2 + démarrerPosition + indiceBoucle]; if (codeCatégorie != 3 || peutTableauStocker(donnéesOctet, valeurDonnées)) valeurTas[donnéesOctet + 2 + indiceValeurDestination + indiceBoucle] = valeurDonnées; } }
                }
                return true;
            }
        }
        if (texteMot(propriétaire, "java/util/ArrayList") || texteMot(propriétaire, "java/util/List") || texteMot(propriétaire, "java/util/HashMap") || texteMot(propriétaire, "java/util/Map")) {
            invoquerCollection(propriétaire, constanteNom, constanteDescripteur, codeCommande); return true;
        }
        return false;
    }
    static void étendreCollection(int référenceObjet, int nombreÉlémentsRequis) {
        int valeurPrécédentÉlément = valeurTas[référenceObjet + 2], donnéesCapacité = valeurPrécédentÉlément == 0 ? 0 : valeurTas[valeurPrécédentÉlément + 1];
        if (donnéesCapacité >= nombreÉlémentsRequis) return;
        int positionSuivant = donnéesCapacité < 8 ? 8 : donnéesCapacité * 2; if (positionSuivant < nombreÉlémentsRequis) positionSuivant = nombreÉlémentsRequis;
        int tableauDonnées = allouerStockage(3, positionSuivant); if (erreur) return;
        for (int indiceBoucle = 0; indiceBoucle < donnéesCapacité; indiceBoucle++) valeurTas[tableauDonnées + 2 + indiceBoucle] = valeurTas[valeurPrécédentÉlément + 2 + indiceBoucle];
        valeurTas[référenceObjet + 2] = tableauDonnées; référenceTas[référenceObjet + 2] = 1;
    }
    static void invoquerCollection(int propriétaire, int constanteNom, int constanteDescripteur, int codeCommande) {
        boolean référenceAssocié = texteMot(propriétaire, "java/util/HashMap") || texteMot(propriétaire, "java/util/Map"); int codeCatégorie = référenceAssocié ? 11 : 10;
        if (texteMot(constanteNom, "<init>") && codeCommande == 183 && texteMot(constanteDescripteur, "()V")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, codeCatégorie)) étendreCollection(référenceObjet, 8); return; }
        if (codeCommande != 182 && codeCommande != 185) { valeurÉchec("invalid collection invocation"); return; }
        if (texteMot(constanteNom, "size") && texteMot(constanteDescripteur, "()I") || texteMot(constanteNom, "isEmpty") && texteMot(constanteDescripteur, "()Z")) {
            int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, codeCatégorie)) placerValeur(texteMot(constanteNom, "size") ? valeurTas[référenceObjet + 3] : valeurTas[référenceObjet + 3] == 0 ? 1 : 0, 1); return;
        }
        if (texteMot(constanteNom, "clear") && texteMot(constanteDescripteur, "()V")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, codeCatégorie)) { int tableauDonnées = valeurTas[référenceObjet + 2]; for (int indiceBoucle = 0; indiceBoucle < valeurTas[tableauDonnées + 1]; indiceBoucle++) valeurTas[tableauDonnées + 2 + indiceBoucle] = 0; valeurTas[référenceObjet + 3] = 0; } return; }
        if (!référenceAssocié && texteMot(constanteNom, "add") && texteMot(constanteDescripteur, "(Ljava/lang/Object;)Z")) {
            int valeurDonnées = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 10)) return;
            int nombreÉlémentsEntréeÉlément = valeurTas[référenceObjet + 3]; étendreCollection(référenceObjet, nombreÉlémentsEntréeÉlément + 1); if (!erreur) { valeurTas[valeurTas[référenceObjet + 2] + 2 + nombreÉlémentsEntréeÉlément] = valeurDonnées; valeurTas[référenceObjet + 3] = nombreÉlémentsEntréeÉlément + 1; placerValeur(1, 1); } return;
        }
        if (!référenceAssocié && (texteMot(constanteNom, "get") || texteMot(constanteNom, "remove")) && texteMot(constanteDescripteur, "(I)Ljava/lang/Object;") || !référenceAssocié && texteMot(constanteNom, "set") && texteMot(constanteDescripteur, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean estAffecté = texteMot(constanteNom, "set"); int valeurDonnées = estAffecté ? soustraireValeurs(2) : 0, positionEntréeÉlément = soustraireValeurs(1), référenceObjet = soustraireValeurs(2);
            if (!valeurObjet(référenceObjet, 10)) return;
            int nombreÉlémentsEntréeÉlément = valeurTas[référenceObjet + 3], tableauDonnées = valeurTas[référenceObjet + 2];
            if (positionEntréeÉlément < 0 || positionEntréeÉlément >= nombreÉlémentsEntréeÉlément) { leverException(6, "list index"); return; }
            int valeurPrécédentÉlément = valeurTas[tableauDonnées + 2 + positionEntréeÉlément];
            if (estAffecté) valeurTas[tableauDonnées + 2 + positionEntréeÉlément] = valeurDonnées;
            if (texteMot(constanteNom, "remove")) { for (int indiceBoucle = positionEntréeÉlément + 1; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) valeurTas[tableauDonnées + 1 + indiceBoucle] = valeurTas[tableauDonnées + 2 + indiceBoucle]; valeurTas[tableauDonnées + 1 + nombreÉlémentsEntréeÉlément] = 0; valeurTas[référenceObjet + 3] = nombreÉlémentsEntréeÉlément - 1; }
            placerValeur(valeurPrécédentÉlément, 2); return;
        }
        if (référenceAssocié && (texteMot(constanteNom, "get") || texteMot(constanteNom, "remove")) && texteMot(constanteDescripteur, "(Ljava/lang/Object;)Ljava/lang/Object;") || référenceAssocié && texteMot(constanteNom, "put") && texteMot(constanteDescripteur, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || référenceAssocié && texteMot(constanteNom, "containsKey") && texteMot(constanteDescripteur, "(Ljava/lang/Object;)Z")) {
            boolean estInsertion = texteMot(constanteNom, "put"), supprimer = texteMot(constanteNom, "remove");
            int valeurDonnées = estInsertion ? soustraireValeurs(2) : 0, référenceTouche = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 11)) return;
            int nombreÉlémentsEntréeÉlément = valeurTas[référenceObjet + 3], tableauDonnées = valeurTas[référenceObjet + 2], trouvéÉtait = -1;
            for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) if (égalValeurs(référenceTouche, valeurTas[tableauDonnées + 2 + 2 * indiceBoucle])) { trouvéÉtait = indiceBoucle; break; }
            int valeurPrécédentÉlément = trouvéÉtait < 0 ? 0 : valeurTas[tableauDonnées + 3 + 2 * trouvéÉtait];
            if (estInsertion) {
                if (trouvéÉtait < 0) { étendreCollection(référenceObjet, (nombreÉlémentsEntréeÉlément + 1) * 2); tableauDonnées = valeurTas[référenceObjet + 2]; trouvéÉtait = nombreÉlémentsEntréeÉlément; if (!erreur) valeurTas[référenceObjet + 3] = nombreÉlémentsEntréeÉlément + 1; }
                if (!erreur) { valeurTas[tableauDonnées + 2 + 2 * trouvéÉtait] = référenceTouche; valeurTas[tableauDonnées + 3 + 2 * trouvéÉtait] = valeurDonnées; }
            }
            if (supprimer && trouvéÉtait >= 0) { for (int indiceBoucle = trouvéÉtait + 1; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) { valeurTas[tableauDonnées + 2 * indiceBoucle] = valeurTas[tableauDonnées + 2 + 2 * indiceBoucle]; valeurTas[tableauDonnées + 1 + 2 * indiceBoucle] = valeurTas[tableauDonnées + 3 + 2 * indiceBoucle]; } valeurTas[tableauDonnées + 2 * nombreÉlémentsEntréeÉlément] = 0; valeurTas[tableauDonnées + 1 + 2 * nombreÉlémentsEntréeÉlément] = 0; valeurTas[référenceObjet + 3] = nombreÉlémentsEntréeÉlément - 1; }
            if (texteMot(constanteNom, "containsKey")) placerValeur(trouvéÉtait >= 0 ? 1 : 0, 1); else placerValeur(valeurPrécédentÉlément, 2);
            return;
        }
        valeurÉchec("unsupported collection method");
    }
    static boolean acquérirVerrou(int référenceObjet) {
        if (!estObjetValide(référenceObjet)) return false;
        if (profondeurVerrou[référenceObjet] != 0 && propriétaireVerrou[référenceObjet] != filExécutionActuel + 1) { changerRequête = true; return false; }
        propriétaireVerrou[référenceObjet] = filExécutionActuel + 1; profondeurVerrou[référenceObjet]++; return true;
    }
    static void libérerVerrou(int référenceObjet) {
        if (!estObjetValide(référenceObjet)) return;
        if (profondeurVerrou[référenceObjet] == 0 || propriétaireVerrou[référenceObjet] != filExécutionActuel + 1) { leverException(13, "monitor not owned"); return; }
        if (--profondeurVerrou[référenceObjet] == 0) propriétaireVerrou[référenceObjet] = 0;
    }
    static boolean filExécutionCommuter() {
        cadreFilExécution[filExécutionActuel] = indiceCadre;
        if (indiceCadre < filExécutionActuel * 32) étatValeurFilExécution[filExécutionActuel] = 3;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsFilExécution; indiceBoucle++) if (étatValeurFilExécution[indiceBoucle] == 2 && étatValeurFilExécution[attendreFilExécutionPour[indiceBoucle]] == 3) étatValeurFilExécution[indiceBoucle] = 1;
        for (int indiceBoucle = 1; indiceBoucle <= nombreÉlémentsFilExécution; indiceBoucle++) {
            int positionSuivant = (filExécutionActuel + indiceBoucle) % nombreÉlémentsFilExécution;
            if (étatValeurFilExécution[positionSuivant] == 1) { filExécutionActuel = positionSuivant; indiceCadre = cadreFilExécution[positionSuivant]; changerRequête = false; return true; }
        }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsFilExécution; indiceBoucle++) if (étatValeurFilExécution[indiceBoucle] != 3) { valeurÉchec("thread deadlock"); return false; }
        return false;
    }
    static void invoquerFilExécution(int constanteNom, int constanteDescripteur, int codeCommande) { filExécutionProcessus(constanteNom, constanteDescripteur, codeCommande, false); }
    static void filExécutionProcessus(int constanteNom, int constanteDescripteur, int codeCommande, boolean français) {
        if (codeCommande == 184 && texteMot(constanteNom, français ? "céderTâche" : "yield") && texteMot(constanteDescripteur, "()V")) { changerRequête = true; return; }
        if (codeCommande == 184 && texteMot(constanteNom, "currentThread") && texteMot(constanteDescripteur, "()Ljava/lang/Thread;")) { placerValeur(objetFilExécution[filExécutionActuel], 2); return; }
        if (codeCommande == 183 && texteMot(constanteNom, "<init>") && (texteMot(constanteDescripteur, "()V") || texteMot(constanteDescripteur, français ? "(Lfrançais/interne/TâcheTâcheExécutable;)V" : "(Ljava/lang/Runnable;)V"))) {
            int adresseCible = texteMot(constanteDescripteur, "()V") ? 0 : soustraireValeurs(2), référenceObjet = soustraireValeurs(2);
            if (!estObjetValide(référenceObjet)) return;
            if (valeurTas[référenceObjet] == 13) { valeurTas[référenceObjet + 2] = adresseCible; référenceTas[référenceObjet + 2] = 1; }
            else if (adresseCible != 0) valeurÉchec("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (codeCommande == 182 && (texteMot(constanteNom, français ? "démarrerTâche" : "start") || texteMot(constanteNom, français ? "attendreFin" : "join")) && texteMot(constanteDescripteur, "()V") || codeCommande == 182 && texteMot(constanteNom, français ? "estVivant" : "isAlive") && texteMot(constanteDescripteur, "()Z")) {
            int référenceObjet = soustraireValeurs(2); if (!estObjetValide(référenceObjet)) return;
            int valeurIdentité = -1; for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsFilExécution; indiceBoucle++) if (objetFilExécution[indiceBoucle] == référenceObjet) valeurIdentité = indiceBoucle;
            if (texteMot(constanteNom, français ? "estVivant" : "isAlive")) { placerValeur(valeurIdentité >= 0 && étatValeurFilExécution[valeurIdentité] != 3 ? 1 : 0, 1); return; }
            if (texteMot(constanteNom, français ? "attendreFin" : "join")) { if (valeurIdentité >= 0 && étatValeurFilExécution[valeurIdentité] != 3) { attendreFilExécutionPour[filExécutionActuel] = valeurIdentité; étatValeurFilExécution[filExécutionActuel] = 2; changerRequête = true; } return; }
            if (valeurIdentité >= 0) { leverException(français ? 38 : 16, "thread already started"); return; }
            if (nombreÉlémentsFilExécution == 4) { valeurÉchec("thread limit (4 including main)"); return; }
            int adresseCible = valeurTas[référenceObjet] == 13 ? valeurTas[référenceObjet + 2] : référenceObjet;
            int indiceFichier = adresseCible > 0 && valeurTas[adresseCible] >= 32 ? méthodeNom(valeurTas[adresseCible] - 32, français ? "exécuterTâche" : "run", "()V") : -1;
            if (adresseCible != 0 && indiceFichier < 0) { valeurÉchec("Runnable.run required"); return; }
            valeurIdentité = nombreÉlémentsFilExécution++; objetFilExécution[valeurIdentité] = référenceObjet; cibleFilExécution[valeurIdentité] = adresseCible;
            int cadre = valeurIdentité * 32; cadreFilExécution[valeurIdentité] = indiceFichier < 0 ? cadre - 1 : cadre; étatValeurFilExécution[valeurIdentité] = indiceFichier < 0 ? 3 : 1;
            if (indiceFichier >= 0) { méthodeCadre[cadre] = indiceFichier; positionCadre[cadre] = démarrerMéthode[indiceFichier]; valeurLocal[cadre * 128] = adresseCible; typeLocal[cadre * 128] = 2; }
            return;
        }
        valeurÉchec("unsupported Thread method");
    }
    static int[] valeurTemporaireRéseau = new int[514], texteAdresse = new int[16];
    static int adresseLocal() { return objetAdresse(0x7f000001); }
    static int objetAdresse(int valeur) { int référenceObjet = allouerStockage(14, 1); if (!erreur) valeurTas[référenceObjet + 2] = valeur; return référenceObjet; }
    static int décoderAdresse(int référenceObjet) {
        if (référenceObjet == 0 || égalTextes(référenceObjet, caractèreHôte("localhost"), false)) return 0x7f000001;
        if (!valeurObjet(référenceObjet, 1)) return 0;
        int valeurDonnées = 0, nombreÉlémentsTotal = 0, octetAdresse = 0, chiffres = 0, nombreÉlémentsEntréeÉlément = valeurTas[référenceObjet + 1];
        for (int indiceBoucle = 0; indiceBoucle <= nombreÉlémentsEntréeÉlément; indiceBoucle++) {
            int codeCaractère = indiceBoucle == nombreÉlémentsEntréeÉlément ? '.' : valeurTas[référenceObjet + 2 + indiceBoucle];
            if (codeCaractère == '.') { if (chiffres == 0 || nombreÉlémentsTotal == 4) { leverException(18, "numeric IPv4 address required; DNS unavailable"); return 0; } valeurDonnées = valeurDonnées << 8 | octetAdresse; nombreÉlémentsTotal++; octetAdresse = chiffres = 0; }
            else { if (codeCaractère < '0' || codeCaractère > '9' || ++chiffres > 3 || (octetAdresse = octetAdresse * 10 + codeCaractère - '0') > 255) { leverException(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (nombreÉlémentsTotal != 4) { leverException(18, "invalid IPv4 address"); return 0; } return valeurDonnées;
    }
    static int caractèreAdresse(int valeurDonnées) {
        int nombreÉlémentsEntréeÉlément = 0;
        for (int décaler = 24; décaler >= 0; décaler -= 8) {
            int octetAdresse = valeurDonnées >>> décaler & 255;
            if (octetAdresse >= 100) texteAdresse[nombreÉlémentsEntréeÉlément++] = '0' + octetAdresse / 100;
            if (octetAdresse >= 10) texteAdresse[nombreÉlémentsEntréeÉlément++] = '0' + octetAdresse / 10 % 10;
            texteAdresse[nombreÉlémentsEntréeÉlément++] = '0' + octetAdresse % 10; if (décaler != 0) texteAdresse[nombreÉlémentsEntréeÉlément++] = '.';
        }
        int référenceObjet = allouerStockage(1, nombreÉlémentsEntréeÉlément); if (!erreur) for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) valeurTas[référenceObjet + 2 + indiceBoucle] = texteAdresse[indiceBoucle]; return référenceObjet;
    }
    static void invoquerRéseau(int propriétaire, int constanteNom, int constanteDescripteur, int codeCommande) {
        if (texteMot(propriétaire, "java/net/InetAddress")) {
            if (codeCommande == 184 && texteMot(constanteNom, "getLoopbackAddress") && texteMot(constanteDescripteur, "()Ljava/net/InetAddress;")) { placerValeur(adresseLocal(), 2); return; }
            if (codeCommande == 184 && texteMot(constanteNom, "getByName") && texteMot(constanteDescripteur, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int valeurDonnées = décoderAdresse(soustraireValeurs(2)); if (objetLevé == 0 && !erreur) placerValeur(objetAdresse(valeurDonnées), 2); return;
            }
            if (codeCommande == 182 && texteMot(constanteNom, "getHostAddress") && texteMot(constanteDescripteur, "()Ljava/lang/String;")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 14)) placerValeur(caractèreAdresse(valeurTas[référenceObjet + 2]), 2); return; }
        }
        if (texteMot(propriétaire, "java/net/DatagramPacket")) {
            if (codeCommande == 183 && texteMot(constanteNom, "<init>") && (texteMot(constanteDescripteur, "([BI)V") || texteMot(constanteDescripteur, "([BILjava/net/InetAddress;I)V"))) {
                boolean référenceValeurDestination = texteMot(constanteDescripteur, "([BILjava/net/InetAddress;I)V"); int numéroPort = référenceValeurDestination ? soustraireValeurs(1) : 0, référenceAdresse = référenceValeurDestination ? soustraireValeurs(2) : 0;
                int nombreÉlémentsEntréeÉlément = soustraireValeurs(1), tableauDonnées = soustraireValeurs(2), référenceObjet = soustraireValeurs(2);
                if (!valeurObjet(référenceObjet, 16) || !valeurObjet(tableauDonnées, 20)) return;
                if (nombreÉlémentsEntréeÉlément < 0 || nombreÉlémentsEntréeÉlément > valeurTas[tableauDonnées + 1] || numéroPort < 0 || numéroPort > 65535) { leverException(9, "invalid datagram length/port"); return; }
                if (référenceAdresse != 0 && !valeurObjet(référenceAdresse, 14)) return;
                valeurTas[référenceObjet + 2] = tableauDonnées; référenceTas[référenceObjet + 2] = 1; valeurTas[référenceObjet + 3] = nombreÉlémentsEntréeÉlément;
                valeurTas[référenceObjet + 4] = référenceAdresse; référenceTas[référenceObjet + 4] = 1; valeurTas[référenceObjet + 5] = numéroPort; return;
            }
            if (codeCommande == 182 && texteMot(constanteNom, "setLength") && texteMot(constanteDescripteur, "(I)V")) {
                int nombreÉlémentsEntréeÉlément = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 16)) return;
                if (nombreÉlémentsEntréeÉlément < 0 || nombreÉlémentsEntréeÉlément > valeurTas[valeurTas[référenceObjet + 2] + 1]) leverException(9, "invalid datagram length"); else valeurTas[référenceObjet + 3] = nombreÉlémentsEntréeÉlément; return;
            }
            if (codeCommande == 182 && (texteMot(constanteNom, "getData") && texteMot(constanteDescripteur, "()[B") || texteMot(constanteNom, "getLength") && texteMot(constanteDescripteur, "()I") || texteMot(constanteNom, "getAddress") && texteMot(constanteDescripteur, "()Ljava/net/InetAddress;") || texteMot(constanteNom, "getPort") && texteMot(constanteDescripteur, "()I"))) {
                int référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 16)) return;
                int positionEntréeÉlément = texteMot(constanteNom, "getData") ? 2 : texteMot(constanteNom, "getLength") ? 3 : texteMot(constanteNom, "getAddress") ? 4 : 5;
                placerValeur(valeurTas[référenceObjet + positionEntréeÉlément], positionEntréeÉlément == 2 || positionEntréeÉlément == 4 ? 2 : 1); return;
            }
        }
        if (texteMot(propriétaire, "java/net/DatagramSocket")) {
            if (codeCommande == 183 && texteMot(constanteNom, "<init>") && (texteMot(constanteDescripteur, "()V") || texteMot(constanteDescripteur, "(I)V"))) {
                int numéroPort = texteMot(constanteDescripteur, "()V") ? 0 : soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 15)) return;
                if (numéroPort < 0 || numéroPort > 65535) { leverException(9, "invalid port"); return; }
                int numéroFichierOuvert = Utilisateur.ouvrirRéseau(numéroPort); if (numéroFichierOuvert < 0) leverException(39, "UDP socket/bind failed"); else valeurTas[référenceObjet + 2] = numéroFichierOuvert; return;
            }
            if (codeCommande == 182 && texteMot(constanteNom, "setSoTimeout") && texteMot(constanteDescripteur, "(I)V")) {
                int valeurMillisecondes = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 15)) return;
                if (valeurMillisecondes < 0) leverException(9, "negative timeout"); else valeurTas[référenceObjet + 3] = valeurMillisecondes; return;
            }
            if (codeCommande == 182 && texteMot(constanteNom, "getLocalPort") && texteMot(constanteDescripteur, "()I")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 15)) placerValeur(valeurTas[référenceObjet + 2] < 0 ? -1 : Utilisateur.portRéseau(valeurTas[référenceObjet + 2]), 1); return; }
            if (codeCommande == 182 && texteMot(constanteNom, "isClosed") && texteMot(constanteDescripteur, "()Z")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 15)) placerValeur(valeurTas[référenceObjet + 2] < 0 ? 1 : 0, 1); return; }
            if (codeCommande == 182 && texteMot(constanteNom, "close") && texteMot(constanteDescripteur, "()V")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, 15) && valeurTas[référenceObjet + 2] >= 0) { Utilisateur.fermerDescripteurFichier(valeurTas[référenceObjet + 2]); valeurTas[référenceObjet + 2] = -1; } return; }
            if (codeCommande == 182 && (texteMot(constanteNom, "send") || texteMot(constanteNom, "receive")) && texteMot(constanteDescripteur, "(Ljava/net/DatagramPacket;)V")) {
                int paquet = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (!valeurObjet(paquet, 16) || !valeurObjet(référenceObjet, 15)) return;
                int tableauDonnées = valeurTas[paquet + 2], longueurValide = valeurTas[paquet + 3], numéroFichierOuvert = valeurTas[référenceObjet + 2];
                if (numéroFichierOuvert < 0) { leverException(39, "socket closed"); return; }
                if (texteMot(constanteNom, "send")) {
                    if (!valeurObjet(valeurTas[paquet + 4], 14)) return;
                    if (longueurValide > 512) { leverException(11, "datagram limit (512 bytes)"); return; }
                    for (int indiceBoucle = 0; indiceBoucle < longueurValide; indiceBoucle++) valeurTemporaireRéseau[indiceBoucle] = valeurTas[tableauDonnées + 2 + indiceBoucle];
                    if (Utilisateur.envoyerRéseau(numéroFichierOuvert, valeurTas[valeurTas[paquet + 4] + 2], valeurTas[paquet + 5], valeurTemporaireRéseau, longueurValide) < 0) leverException(11, "UDP send failed");
                } else {
                    int nombreÉlémentsEntréeÉlément = Utilisateur.recevoirRéseau(numéroFichierOuvert, valeurTemporaireRéseau, longueurValide > 512 ? 512 : longueurValide);
                    if (nombreÉlémentsEntréeÉlément == -11) {
                        int tempsActuel = Utilisateur.millisecondes();
                        if (valeurTas[référenceObjet + 4] == 0) valeurTas[référenceObjet + 4] = tempsActuel + 1;
                        if (valeurTas[référenceObjet + 3] > 0 && tempsActuel - (valeurTas[référenceObjet + 4] - 1) >= valeurTas[référenceObjet + 3]) { valeurTas[référenceObjet + 4] = 0; leverException(19, "receive timed out"); return; }
                        placerValeur(référenceObjet, 2); placerValeur(paquet, 2); positionCadre[indiceCadre] = instructionMachineCadre[indiceCadre]; changerRequête = true; return;
                    }
                    valeurTas[référenceObjet + 4] = 0;
                    if (nombreÉlémentsEntréeÉlément < 0) { leverException(11, "UDP receive failed"); return; }
                    for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) valeurTas[tableauDonnées + 2 + indiceBoucle] = (byte)valeurTemporaireRéseau[indiceBoucle];
                    valeurTas[paquet + 3] = nombreÉlémentsEntréeÉlément; valeurTas[paquet + 4] = objetAdresse(valeurTemporaireRéseau[513]); référenceTas[paquet + 4] = 1; valeurTas[paquet + 5] = valeurTemporaireRéseau[512];
                }
                return;
            }
        }
        valeurÉchec("unsupported java.net method");
    }
    static boolean attendreFluxPour(int référenceObjet) {
        int tempsActuel = Utilisateur.millisecondes();
        if (valeurTas[référenceObjet + 5] == 0) valeurTas[référenceObjet + 5] = tempsActuel + 1;
        if (valeurTas[référenceObjet + 3] > 0 && tempsActuel - (valeurTas[référenceObjet + 5] - 1) >= valeurTas[référenceObjet + 3]) { valeurTas[référenceObjet + 5] = 0; leverException(19, "stream wait timed out"); return false; }
        positionCadre[indiceCadre] = instructionMachineCadre[indiceCadre]; changerRequête = true; return true;
    }
    static void invoquerFlux(int propriétaire, int constanteNom, int constanteDescripteur, int codeCommande) {
        boolean recevoirPage = texteMot(propriétaire, "java/net/ServerSocket"), flux = texteMot(propriétaire, "java/io/InputStream") || texteMot(propriétaire, "java/io/OutputStream");
        if (!flux && codeCommande == 183 && texteMot(constanteNom, "<init>")) {
            boolean estÉtatValeurVide = texteMot(constanteDescripteur, "()V"), nommé = texteMot(constanteDescripteur, "(Ljava/lang/String;I)V"), adressé = texteMot(constanteDescripteur, "(Ljava/net/InetAddress;I)V");
            if (!(estÉtatValeurVide || recevoirPage && texteMot(constanteDescripteur, "(I)V") || !recevoirPage && (nommé || adressé))) { valeurÉchec("unsupported socket constructor"); return; }
            int numéroPort = estÉtatValeurVide ? 0 : soustraireValeurs(1), référenceAdresse = nommé || adressé ? soustraireValeurs(2) : 0, référenceObjet = soustraireValeurs(2);
            if (!valeurObjet(référenceObjet, recevoirPage ? 18 : 17)) return;
            if (numéroPort < 0 || numéroPort > 65535) { leverException(9, "invalid port"); return; }
            if (adressé && !valeurObjet(référenceAdresse, 14)) return;
            int adresseRéseau = nommé ? décoderAdresse(référenceAdresse) : adressé ? valeurTas[référenceAdresse + 2] : 0x7f000001;
            if (erreur || objetLevé != 0) return;
            int numéroFichierOuvert = Utilisateur.contrôleFlux(0, 0, 0); if (numéroFichierOuvert < 0) { leverException(39, "socket slots exhausted"); return; }
            int valeurTraité = estÉtatValeurVide ? 0 : recevoirPage ? Utilisateur.contrôleFlux(1, numéroFichierOuvert, numéroPort) : Utilisateur.connecterFlux(numéroFichierOuvert, adresseRéseau, numéroPort);
            if (valeurTraité < 0) { Utilisateur.fermerDescripteurFichier(numéroFichierOuvert); leverException(39, "socket bind/connect failed"); return; }
            valeurTas[référenceObjet + 2] = numéroFichierOuvert; valeurTas[référenceObjet + 4] = numéroPort; valeurTas[référenceObjet + 6] = estÉtatValeurVide ? 0 : 1; return;
        }
        if (!flux && texteMot(constanteNom, "setSoTimeout") && texteMot(constanteDescripteur, "(I)V")) { int valeurMillisecondes = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, recevoirPage ? 18 : 17)) return; if (valeurMillisecondes < 0) leverException(9, "negative timeout"); else valeurTas[référenceObjet + 3] = valeurMillisecondes; return; }
        if (!flux && texteMot(constanteNom, "close") && texteMot(constanteDescripteur, "()V")) { int référenceObjet = soustraireValeurs(2); if (valeurObjet(référenceObjet, recevoirPage ? 18 : 17) && valeurTas[référenceObjet + 2] >= 0) { Utilisateur.fermerDescripteurFichier(valeurTas[référenceObjet + 2]); valeurTas[référenceObjet + 2] = -1; } return; }
        if (!flux && (texteMot(constanteNom, "getLocalPort") || texteMot(constanteNom, "getPort") || texteMot(constanteNom, "isClosed") || texteMot(constanteNom, "isConnected"))) {
            int référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, recevoirPage ? 18 : 17)) return;
            placerValeur(texteMot(constanteNom, "isClosed") ? valeurTas[référenceObjet + 2] < 0 ? 1 : 0 : texteMot(constanteNom, "isConnected") ? valeurTas[référenceObjet + 6] : texteMot(constanteNom, "getPort") ? valeurTas[référenceObjet + 4] : valeurTas[référenceObjet + 2] < 0 ? -1 : Utilisateur.contrôleFlux(4, valeurTas[référenceObjet + 2], 0), 1); return;
        }
        if (recevoirPage && texteMot(constanteNom, "accept") && texteMot(constanteDescripteur, "()Ljava/net/Socket;")) {
            int référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 18)) return; int numéroFichierOuvert = Utilisateur.contrôleFlux(3, valeurTas[référenceObjet + 2], 0);
            if (numéroFichierOuvert == -11) { if (attendreFluxPour(référenceObjet)) placerValeur(référenceObjet, 2); return; }
            valeurTas[référenceObjet + 5] = 0; if (numéroFichierOuvert < 0) { leverException(11, "accept failed"); return; }
            int valeurRetourné = allouerStockage(17, 5); if (erreur) { Utilisateur.fermerDescripteurFichier(numéroFichierOuvert); return; } valeurTas[valeurRetourné + 2] = numéroFichierOuvert; valeurTas[valeurRetourné + 4] = Utilisateur.contrôleFlux(5, numéroFichierOuvert, 0); valeurTas[valeurRetourné + 6] = 1; placerValeur(valeurRetourné, 2); return;
        }
        if (!recevoirPage && !flux && ((texteMot(constanteNom, "getInputStream") && texteMot(constanteDescripteur, "()Ljava/io/InputStream;")) || (texteMot(constanteNom, "getOutputStream") && texteMot(constanteDescripteur, "()Ljava/io/OutputStream;")))) {
            int référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 17)) return; if (valeurTas[référenceObjet + 2] < 0 || valeurTas[référenceObjet + 6] == 0) { leverException(39, "socket is not connected"); return; }
            int valeurRetourné = allouerStockage(19, 4); if (erreur) return; valeurTas[valeurRetourné + 2] = référenceObjet; référenceTas[valeurRetourné + 2] = 1; valeurTas[valeurRetourné + 3] = texteMot(constanteNom, "getInputStream") ? 0 : 1; placerValeur(valeurRetourné, 2); return;
        }
        if (flux) {
            boolean possèdeLire = texteMot(constanteNom, "read"), estOpérationÉcrire = texteMot(constanteNom, "write"), bloc = texteMot(constanteDescripteur, "([B)I") || texteMot(constanteDescripteur, "([B)V"), estSousTableau = texteMot(constanteDescripteur, "([BII)I") || texteMot(constanteDescripteur, "([BII)V");
            int nombreÉlémentsEntréeÉlément = estSousTableau ? soustraireValeurs(1) : 0, démarrerDéplacement = estSousTableau ? soustraireValeurs(1) : 0, tableauDonnées = bloc || estSousTableau ? soustraireValeurs(2) : 0;
            int valeurDonnées = estOpérationÉcrire && texteMot(constanteDescripteur, "(I)V") ? soustraireValeurs(1) : 0, référenceObjet = soustraireValeurs(2);
            if (!valeurObjet(référenceObjet, 19)) return; int référenceParent = valeurTas[référenceObjet + 2], numéroFichierOuvert = valeurTas[référenceParent + 2];
            if (numéroFichierOuvert < 0) { leverException(11, "stream closed"); return; }
            if (texteMot(constanteNom, "close") && texteMot(constanteDescripteur, "()V")) { Utilisateur.fermerDescripteurFichier(numéroFichierOuvert); valeurTas[référenceParent + 2] = -1; return; }
            if (texteMot(constanteNom, "flush") && texteMot(constanteDescripteur, "()V")) return;
            if ((!possèdeLire && !estOpérationÉcrire) || possèdeLire != (valeurTas[référenceObjet + 3] == 0)) { valeurÉchec("unsupported stream operation"); return; }
            if (bloc || estSousTableau) { if (!valeurObjet(tableauDonnées, 20)) return; if (bloc) nombreÉlémentsEntréeÉlément = valeurTas[tableauDonnées + 1]; if (démarrerDéplacement < 0 || nombreÉlémentsEntréeÉlément < 0 || démarrerDéplacement > valeurTas[tableauDonnées + 1] - nombreÉlémentsEntréeÉlément) { leverException(6, "stream array bounds"); return; } }
            else nombreÉlémentsEntréeÉlément = 1;
            if (nombreÉlémentsEntréeÉlément == 0) { if (possèdeLire) placerValeur(0, 1); return; }
            int nombreÉlémentsAchevé = estOpérationÉcrire ? valeurTas[référenceObjet + 4] : 0, valeurTraité = 0;
            while (nombreÉlémentsAchevé < nombreÉlémentsEntréeÉlément) {
                valeurTraité = possèdeLire ? Utilisateur.lireOctetFichierUn(numéroFichierOuvert) : Utilisateur.écrireOctetFichierUn(numéroFichierOuvert, bloc || estSousTableau ? valeurTas[tableauDonnées + 2 + démarrerDéplacement + nombreÉlémentsAchevé] : valeurDonnées);
                if (valeurTraité < 0 || possèdeLire && valeurTraité == 256) break;
                if (possèdeLire && (bloc || estSousTableau)) valeurTas[tableauDonnées + 2 + démarrerDéplacement + nombreÉlémentsAchevé] = (byte)valeurTraité;
                nombreÉlémentsAchevé++; if (possèdeLire && !(bloc || estSousTableau)) break;
            }
            if (valeurTraité == -11 && (estOpérationÉcrire || nombreÉlémentsAchevé == 0)) {
                valeurTas[référenceObjet + 4] = nombreÉlémentsAchevé;
                if (attendreFluxPour(référenceParent)) { placerValeur(référenceObjet, 2); if (bloc || estSousTableau) placerValeur(tableauDonnées, 2); if (estSousTableau) { placerValeur(démarrerDéplacement, 1); placerValeur(nombreÉlémentsEntréeÉlément, 1); } if (estOpérationÉcrire && !(bloc || estSousTableau)) placerValeur(valeurDonnées, 1); } return;
            }
            valeurTas[référenceObjet + 4] = 0; valeurTas[référenceParent + 5] = 0;
            if (valeurTraité < 0 && valeurTraité != -11) { leverException(11, "stream I/O failed"); return; }
            if (possèdeLire) placerValeur(nombreÉlémentsAchevé == 0 && valeurTraité == 256 ? -1 : bloc || estSousTableau ? nombreÉlémentsAchevé : valeurTraité, 1); return;
        }
        valeurÉchec("unsupported Socket/ServerSocket method");
    }
    static int[] référenceÉcran = new int[32], texteÉcranTemporaire = new int[256], ultérieurPlanification = new int[8];
    static int nombreÉlémentsUltérieur;
    static int[] valeurCoréenUltérieur = new int[8];
    static boolean estÉvènementTraitementÉtat;
    static int classeÉcranCoréen(int constanteNom) {
        if (texteMot(constanteNom, "français/interne/fenêtre")) return 24;
        if (texteMot(constanteNom, "français/interne/étiquette")) return 26;
        if (texteMot(constanteNom, "français/interne/bouton")) return 27;
        if (texteMot(constanteNom, "français/interne/ChampTexte")) return 28;
        if (texteMot(constanteNom, "français/interne/NotificationAction")) return 29;
        return 0;
    }
    static boolean propriétaireÉcranCoréen(int constanteNom) {
        return classeÉcranCoréen(constanteNom) != 0 || texteMot(constanteNom, "français/interne/ÉlémentÉcran") || texteMot(constanteNom, "français/interne/FileAttenteÉvènement");
    }
    static int classeÉcran(int constanteNom) {
        int ClasseCoréen = classeÉcranCoréen(constanteNom); if (ClasseCoréen != 0) return ClasseCoréen;
        if (texteMot(constanteNom, "javax/swing/JFrame")) return 24;
        if (texteMot(constanteNom, "javax/swing/JPanel")) return 25;
        if (texteMot(constanteNom, "javax/swing/JLabel")) return 26;
        if (texteMot(constanteNom, "javax/swing/JButton")) return 27;
        if (texteMot(constanteNom, "javax/swing/JTextField")) return 28;
        if (texteMot(constanteNom, "java/awt/event/ActionEvent")) return 29;
        if (texteMot(constanteNom, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean propriétaireÉcran(int constanteNom) {
        return classeÉcran(constanteNom) != 0 || texteMot(constanteNom, "java/awt/Component") || texteMot(constanteNom, "java/awt/Container") || texteMot(constanteNom, "javax/swing/JComponent") || texteMot(constanteNom, "javax/swing/AbstractButton") || texteMot(constanteNom, "javax/swing/text/JTextComponent") || texteMot(constanteNom, "javax/swing/SwingUtilities");
    }
    static boolean objetÉcran(int référenceObjet) { if (!estObjetValide(référenceObjet)) return false; if (valeurTas[référenceObjet] < 24 || valeurTas[référenceObjet] > 28) { valeurÉchec("unsupported Swing receiver"); return false; } return true; }
    static void définirCaractèreÉcran(int référenceObjet, int référenceTexte) {
        if (référenceTexte != 0 && !valeurObjet(référenceTexte, 1)) return;
        int nombreÉlémentsEntréeÉlément = référenceTexte == 0 ? 0 : valeurTas[référenceTexte + 1]; if (nombreÉlémentsEntréeÉlément > 254) { leverException(9, "GUI text limit"); return; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) texteÉcranTemporaire[indiceBoucle] = valeurTas[référenceTexte + 2 + indiceBoucle];
        if (Utilisateur.texteÉcran(valeurTas[référenceObjet + 2], texteÉcranTemporaire, nombreÉlémentsEntréeÉlément) < 0) { leverException(9, "GUI text too long/invalid"); return; }
        valeurTas[référenceObjet + 3] = référenceTexte; référenceTas[référenceObjet + 3] = 1;
    }
    static int lireCaractèreÉcran(int référenceObjet) {
        int valeurIdentité = valeurTas[référenceObjet + 2], nombreÉlémentsEntréeÉlément = Utilisateur.connexionÉcran(8, valeurIdentité, 0, 0, 0, 0), nombreÉlémentsUtilisé = 0;
        if (nombreÉlémentsEntréeÉlément < 0) { valeurÉchec("GUI text read failed"); return 0; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) { int valeurEncodé = Utilisateur.connexionÉcran(9, valeurIdentité, indiceBoucle, 0, 0, 0); if (valeurEncodé >= 65536) { valeurEncodé -= 65536; texteÉcranTemporaire[nombreÉlémentsUtilisé++] = 0xd800 | valeurEncodé >> 10; texteÉcranTemporaire[nombreÉlémentsUtilisé++] = 0xdc00 | valeurEncodé & 1023; } else texteÉcranTemporaire[nombreÉlémentsUtilisé++] = valeurEncodé; }
        int valeurRetourné = allouerStockage(1, nombreÉlémentsUtilisé); if (!erreur) for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsUtilisé; indiceBoucle++) valeurTas[valeurRetourné + 2 + indiceBoucle] = texteÉcranTemporaire[indiceBoucle]; return valeurRetourné;
    }
    /* Crée directement les objets de l’API française et les relie aux fonctions graphiques du noyau, sans objets ni adaptateurs Swing. */
    static void invoquerÉcranCoréen(int propriétaire, int constanteNom, int constanteDescripteur, int codeCommande) {
        if (texteMot(propriétaire, "français/interne/FileAttenteÉvènement")) {
            if (codeCommande == 184 && texteMot(constanteNom, "invoquerUltérieur") && texteMot(constanteDescripteur, "(Lfrançais/interne/TâcheTâcheExécutable;)V")) {
                int ActionTâche = soustraireValeurs(2); if (!estObjetValide(ActionTâche)) return;
                if (nombreÉlémentsUltérieur == 8) { valeurÉchec("Écran Tâche 대기열이 가득 찼습니다"); return; }
                valeurCoréenUltérieur[nombreÉlémentsUltérieur] = 1; ultérieurPlanification[nombreÉlémentsUltérieur++] = ActionTâche; return;
            }
            if (codeCommande == 184 && texteMot(constanteNom, "estDistributionEnCoursÉvènement") && texteMot(constanteDescripteur, "()Z")) { placerValeur(estÉvènementTraitementÉtat ? 1 : 0, 1); return; }
            valeurÉchec("지원하지 않는 français Écran 일정 invoquer"); return;
        }
        if (texteMot(propriétaire, "français/interne/NotificationAction")) {
            int notification = soustraireValeurs(2); if (!valeurObjet(notification, 29) || valeurTas[notification + 3] == 0) return;
            if (texteMot(constanteNom, "sourceÉvènement") && texteMot(constanteDescripteur, "()Lfrançais/interne/ÉlémentÉcran;")) placerValeur(valeurTas[notification + 2], 2);
            else if (texteMot(constanteNom, "texteCommande") && texteMot(constanteDescripteur, "()Ljava/lang/String;")) placerValeur(lireCaractèreÉcran(valeurTas[notification + 2]), 2);
            else if (texteMot(constanteNom, "numéro") && texteMot(constanteDescripteur, "()I")) placerValeur(1001, 1);
            else valeurÉchec("지원하지 않는 français action notification invoquer"); return;
        }
        if (codeCommande == 183 && texteMot(constanteNom, "<init>")) {
            int valeurGenre = classeÉcranCoréen(propriétaire), valeurRécepteur = 0, positionHorizontal = 0, positionVertical = 0, étendueLargeur = 0, valeurHauteur = 0;
            if (valeurGenre == 24 && texteMot(constanteDescripteur, "(Ljava/lang/String;II)V")) {
                valeurHauteur = soustraireValeurs(1); étendueLargeur = soustraireValeurs(1); positionHorizontal = (Utilisateur.largeurÉcran() - étendueLargeur) / 2; positionVertical = (Utilisateur.hauteurÉcran() - valeurHauteur) / 2;
            } else if ((valeurGenre == 26 || valeurGenre == 28) && texteMot(constanteDescripteur, "(Ljava/lang/String;IIII)V") || valeurGenre == 27 && texteMot(constanteDescripteur, "(Ljava/lang/String;IIIILfrançais/interne/RécepteurAction;)V")) {
                if (valeurGenre == 27) valeurRécepteur = soustraireValeurs(2);
                valeurHauteur = soustraireValeurs(1); étendueLargeur = soustraireValeurs(1); positionVertical = soustraireValeurs(1); positionHorizontal = soustraireValeurs(1);
            } else { valeurÉchec("지원하지 않는 français Écran 생성자"); return; }
            int texte = soustraireValeurs(2), valeurÉlément = soustraireValeurs(2); if (!objetÉcran(valeurÉlément)) return;
            if (étendueLargeur < 1 || valeurHauteur < 1 || positionHorizontal < 0 || positionVertical < 0 || étendueLargeur > Utilisateur.largeurÉcran() - positionHorizontal || valeurHauteur > Utilisateur.hauteurÉcran() - positionVertical) { leverException(27, "Écran 영역을 벗어난 크기입니다"); return; }
            int numéro = Utilisateur.connexionÉcran(0, valeurGenre - 23, 0, 0, 0, 0);
            if (numéro < 1 || numéro > 32) { valeurÉchec("Écran valeurÉlément 자리가 가득 찼습니다"); return; }
            valeurTas[valeurÉlément + 2] = numéro; référenceÉcran[numéro - 1] = valeurÉlément;
            valeurTas[valeurÉlément + 5] = positionHorizontal; valeurTas[valeurÉlément + 6] = positionVertical; valeurTas[valeurÉlément + 7] = étendueLargeur; valeurTas[valeurÉlément + 8] = valeurHauteur; valeurTas[valeurÉlément + 10] = 2;
            valeurTas[valeurÉlément + 4] = valeurRécepteur; référenceTas[valeurÉlément + 4] = 1; valeurTas[valeurÉlément + 12] = 1;
            Utilisateur.connexionÉcran(1, numéro, positionHorizontal, positionVertical, étendueLargeur, valeurHauteur);
            if (valeurGenre == 24) Utilisateur.connexionÉcran(7, numéro, 2, 0, 0, 0);
            définirCaractèreÉcran(valeurÉlément, texte); return;
        }
        if (codeCommande != 182) { valeurÉchec("잘못된 français Écran invoquer commande"); return; }
        if (texteMot(constanteNom, "écrireTexte") && texteMot(constanteDescripteur, "(Ljava/lang/String;)V")) {
            int texte = soustraireValeurs(2), valeurÉlément = soustraireValeurs(2); if (objetÉcran(valeurÉlément)) définirCaractèreÉcran(valeurÉlément, texte); return;
        }
        if (texteMot(constanteNom, "lireTexte") && texteMot(constanteDescripteur, "()Ljava/lang/String;")) {
            int valeurÉlément = soustraireValeurs(2); if (objetÉcran(valeurÉlément)) placerValeur(lireCaractèreÉcran(valeurÉlément), 2); return;
        }
        if (texteMot(constanteNom, "définirRécepteurAction") && texteMot(constanteDescripteur, "(Lfrançais/interne/RécepteurAction;)V")) {
            int valeurRécepteur = soustraireValeurs(2), valeurÉlément = soustraireValeurs(2);
            if (objetÉcran(valeurÉlément)) { valeurTas[valeurÉlément + 4] = valeurRécepteur; référenceTas[valeurÉlément + 4] = 1; valeurTas[valeurÉlément + 12] = 1; } return;
        }
        if (texteMot(constanteNom, "ajouterÉlément") && texteMot(constanteDescripteur, "(Lfrançais/interne/ÉlémentÉcran;)V")) {
            int valeurEnfant = soustraireValeurs(2), valeurParent = soustraireValeurs(2); if (!objetÉcran(valeurEnfant) || !objetÉcran(valeurParent)) return;
            if (Utilisateur.connexionÉcran(2, valeurTas[valeurParent + 2], valeurTas[valeurEnfant + 2], 0, 0, 0) < 0) { leverException(27, "잘못된 Écran 부모입니다"); return; }
            valeurTas[valeurEnfant + 11] = valeurParent; référenceTas[valeurEnfant + 11] = 1; return;
        }
        if (texteMot(constanteNom, "définirBornes") && texteMot(constanteDescripteur, "(IIII)V")) {
            int valeurHauteur = soustraireValeurs(1), étendueLargeur = soustraireValeurs(1), positionVertical = soustraireValeurs(1), positionHorizontal = soustraireValeurs(1), valeurÉlément = soustraireValeurs(2); if (!objetÉcran(valeurÉlément)) return;
            if (Utilisateur.connexionÉcran(1, valeurTas[valeurÉlément + 2], positionHorizontal, positionVertical, étendueLargeur, valeurHauteur) < 0) { leverException(27, "Écran 영역을 벗어난 자리입니다"); return; }
            valeurTas[valeurÉlément + 5] = positionHorizontal; valeurTas[valeurÉlément + 6] = positionVertical; valeurTas[valeurÉlément + 7] = étendueLargeur; valeurTas[valeurÉlément + 8] = valeurHauteur; return;
        }
        if ((texteMot(constanteNom, "afficherFenêtre") || texteMot(constanteNom, "fermer")) && texteMot(constanteDescripteur, "()V")) {
            boolean valeurVisibilité = texteMot(constanteNom, "afficherFenêtre"); int valeurÉlément = soustraireValeurs(2); if (!objetÉcran(valeurÉlément)) return;
            if (Utilisateur.connexionÉcran(valeurVisibilité ? 3 : 4, valeurTas[valeurÉlément + 2], valeurVisibilité ? 1 : 0, 0, 0, 0) < 0) { valeurÉchec("화면은 interactif 명령에서 실행해야 합니다"); return; }
            valeurTas[valeurÉlément + 9] = valeurVisibilité ? 1 : 0; return;
        }
        if (texteMot(constanteNom, "estVisible") && texteMot(constanteDescripteur, "()Z")) { int valeurÉlément = soustraireValeurs(2); if (objetÉcran(valeurÉlément)) placerValeur(valeurTas[valeurÉlément + 9], 1); return; }
        valeurÉchec("지원하지 않는 français Écran valeurMéthode");
    }
    static void invoquerÉcran(int propriétaire, int constanteNom, int constanteDescripteur, int codeCommande) {
        if (texteMot(propriétaire, "javax/swing/SwingUtilities")) {
            if (codeCommande == 184 && texteMot(constanteNom, "invokeLater") && texteMot(constanteDescripteur, "(Ljava/lang/Runnable;)V")) { int référenceObjet = soustraireValeurs(2); if (!estObjetValide(référenceObjet)) return; if (nombreÉlémentsUltérieur == 8) { valeurÉchec("invokeLater queue full"); return; } ultérieurPlanification[nombreÉlémentsUltérieur++] = référenceObjet; return; }
            if (codeCommande == 184 && texteMot(constanteNom, "isEventDispatchThread") && texteMot(constanteDescripteur, "()Z")) { placerValeur(estÉvènementTraitementÉtat ? 1 : 0, 1); return; }
            valeurÉchec("unsupported SwingUtilities method"); return;
        }
        if (texteMot(propriétaire, "java/awt/event/ActionEvent")) {
            int référenceObjet = soustraireValeurs(2); if (!valeurObjet(référenceObjet, 29)) return;
            if (texteMot(constanteNom, "getSource") && texteMot(constanteDescripteur, "()Ljava/lang/Object;")) placerValeur(valeurTas[référenceObjet + 2], 2);
            else if (texteMot(constanteNom, "getActionCommand") && texteMot(constanteDescripteur, "()Ljava/lang/String;")) placerValeur(lireCaractèreÉcran(valeurTas[référenceObjet + 2]), 2);
            else if (texteMot(constanteNom, "getID") && texteMot(constanteDescripteur, "()I")) placerValeur(1001, 1);
            else valeurÉchec("unsupported ActionEvent method"); return;
        }
        if (codeCommande == 183 && texteMot(constanteNom, "<init>")) {
            int colonnes = 0, référenceTexte = 0;
            if (texteMot(constanteDescripteur, "(I)V")) colonnes = soustraireValeurs(1);
            else if (texteMot(constanteDescripteur, "(Ljava/lang/String;I)V")) { colonnes = soustraireValeurs(1); référenceTexte = soustraireValeurs(2); }
            else if (texteMot(constanteDescripteur, "(Ljava/lang/String;)V")) référenceTexte = soustraireValeurs(2);
            else if (texteMot(constanteDescripteur, "(Ljava/awt/LayoutManager;)V")) soustraireValeurs(2);
            else if (!texteMot(constanteDescripteur, "()V")) { valeurÉchec("unsupported Swing constructor"); return; }
            int référenceObjet = soustraireValeurs(2); if (!estObjetValide(référenceObjet)) return;
            if (valeurTas[référenceObjet] == 30) { valeurÉchec("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!objetÉcran(référenceObjet) || colonnes < 0) return;
            int valeurIdentité = Utilisateur.connexionÉcran(0, valeurTas[référenceObjet] - 23, 0, 0, 0, 0);
            if (valeurIdentité < 1 || valeurIdentité > 32) { valeurÉchec("GUI widget slots exhausted"); return; }
            valeurTas[référenceObjet + 2] = valeurIdentité; référenceÉcran[valeurIdentité - 1] = référenceObjet; valeurTas[référenceObjet + 5] = valeurTas[référenceObjet] == 24 ? 130 : 16; valeurTas[référenceObjet + 6] = valeurTas[référenceObjet] == 24 ? 110 : 16;
            valeurTas[référenceObjet + 7] = valeurTas[référenceObjet] == 24 ? 380 : 220; valeurTas[référenceObjet + 8] = valeurTas[référenceObjet] == 24 ? 240 : 28; valeurTas[référenceObjet + 10] = 1;
            définirCaractèreÉcran(référenceObjet, référenceTexte); return;
        }
        if (texteMot(constanteNom, "setText") || texteMot(constanteNom, "setTitle")) { int référenceTexte = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet) && texteMot(constanteDescripteur, "(Ljava/lang/String;)V")) définirCaractèreÉcran(référenceObjet, référenceTexte); return; }
        if (texteMot(constanteNom, "getText") || texteMot(constanteNom, "getTitle")) { int référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet) && texteMot(constanteDescripteur, "()Ljava/lang/String;")) placerValeur(lireCaractèreÉcran(référenceObjet), 2); return; }
        if (texteMot(constanteNom, "addActionListener") && texteMot(constanteDescripteur, "(Ljava/awt/event/ActionListener;)V")) { int recevoirRéférence = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet)) { valeurTas[référenceObjet + 4] = recevoirRéférence; référenceTas[référenceObjet + 4] = 1; } return; }
        if (texteMot(constanteNom, "getContentPane") && texteMot(constanteDescripteur, "()Ljava/awt/Container;")) { int référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet)) placerValeur(référenceObjet, 2); return; }
        if (texteMot(constanteNom, "setLayout") && texteMot(constanteDescripteur, "(Ljava/awt/LayoutManager;)V")) { int référenceDisposition = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet) && référenceDisposition != 0) valeurÉchec("only absolute layout (null) is supported"); return; }
        if (texteMot(constanteNom, "add") && (texteMot(constanteDescripteur, "(Ljava/awt/Component;)Ljava/awt/Component;") || texteMot(constanteDescripteur, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean conditionDisposition = texteMot(constanteDescripteur, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (conditionDisposition) soustraireValeurs(2);
            int référenceEnfant = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (!objetÉcran(référenceEnfant) || !objetÉcran(référenceObjet)) return;
            if (Utilisateur.connexionÉcran(2, valeurTas[référenceObjet + 2], valeurTas[référenceEnfant + 2], 0, 0, 0) < 0) { leverException(9, "invalid GUI parent"); return; }
            valeurTas[référenceEnfant + 11] = référenceObjet; référenceTas[référenceEnfant + 11] = 1; if (!conditionDisposition) placerValeur(référenceEnfant, 2); return;
        }
        if (texteMot(constanteNom, "setBounds") && texteMot(constanteDescripteur, "(IIII)V")) {
            int valeurHauteur = soustraireValeurs(1), valeurLargeur = soustraireValeurs(1), coordonnéeCoordonnéeVerticale = soustraireValeurs(1), coordonnéeCoordonnéeHorizontale = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (!objetÉcran(référenceObjet)) return;
            if (Utilisateur.connexionÉcran(1, valeurTas[référenceObjet + 2], coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale, valeurLargeur, valeurHauteur) < 0) { leverException(9, "GUI bounds"); return; }
            valeurTas[référenceObjet + 5] = coordonnéeCoordonnéeHorizontale; valeurTas[référenceObjet + 6] = coordonnéeCoordonnéeVerticale; valeurTas[référenceObjet + 7] = valeurLargeur; valeurTas[référenceObjet + 8] = valeurHauteur; return;
        }
        if (texteMot(constanteNom, "setSize") && texteMot(constanteDescripteur, "(II)V")) {
            int valeurHauteur = soustraireValeurs(1), valeurLargeur = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (!objetÉcran(référenceObjet)) return;
            if (Utilisateur.connexionÉcran(1, valeurTas[référenceObjet + 2], valeurTas[référenceObjet + 5], valeurTas[référenceObjet + 6], valeurLargeur, valeurHauteur) < 0) leverException(9, "GUI size"); else { valeurTas[référenceObjet + 7] = valeurLargeur; valeurTas[référenceObjet + 8] = valeurHauteur; } return;
        }
        if (texteMot(constanteNom, "setLocationRelativeTo") && texteMot(constanteDescripteur, "(Ljava/awt/Component;)V")) { int relatif = soustraireValeurs(2), référenceObjet = soustraireValeurs(2); if (!objetÉcran(référenceObjet)) return; if (relatif != 0) { valeurÉchec("only screen centering supported"); return; } valeurTas[référenceObjet + 5] = (Utilisateur.largeurÉcran() - valeurTas[référenceObjet + 7]) / 2; valeurTas[référenceObjet + 6] = (Utilisateur.hauteurÉcran() - valeurTas[référenceObjet + 8]) / 2; Utilisateur.connexionÉcran(1, valeurTas[référenceObjet + 2], valeurTas[référenceObjet + 5], valeurTas[référenceObjet + 6], valeurTas[référenceObjet + 7], valeurTas[référenceObjet + 8]); return; }
        if (texteMot(constanteNom, "setDefaultCloseOperation") && texteMot(constanteDescripteur, "(I)V")) { int politique = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet)) { if (politique < 0 || politique > 3) leverException(9, "close policy"); else { valeurTas[référenceObjet + 10] = politique; Utilisateur.connexionÉcran(7, valeurTas[référenceObjet + 2], politique, 0, 0, 0); } } return; }
        if (texteMot(constanteNom, "setVisible") && texteMot(constanteDescripteur, "(Z)V")) { int valeurDonnées = soustraireValeurs(1), référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet)) { int valeurTraité = Utilisateur.connexionÉcran(3, valeurTas[référenceObjet + 2], valeurDonnées, 0, 0, 0); if (valeurTraité < 0) valeurÉchec("Swing requires a standalone interactive command"); else valeurTas[référenceObjet + 9] = valeurDonnées; } return; }
        if (texteMot(constanteNom, "dispose") && texteMot(constanteDescripteur, "()V")) { int référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet)) { Utilisateur.connexionÉcran(4, valeurTas[référenceObjet + 2], 0, 0, 0, 0); valeurTas[référenceObjet + 9] = 0; } return; }
        if (texteMot(constanteNom, "repaint") || texteMot(constanteNom, "validate")) { int référenceObjet = soustraireValeurs(2); if (!objetÉcran(référenceObjet) || !texteMot(constanteDescripteur, "()V")) return; Utilisateur.connexionÉcran(1, valeurTas[référenceObjet + 2], valeurTas[référenceObjet + 5], valeurTas[référenceObjet + 6], valeurTas[référenceObjet + 7], valeurTas[référenceObjet + 8]); return; }
        if (texteMot(constanteNom, "isVisible") && texteMot(constanteDescripteur, "()Z")) { int référenceObjet = soustraireValeurs(2); if (objetÉcran(référenceObjet)) placerValeur(valeurTas[référenceObjet + 9], 1); return; }
        valeurÉchec("unsupported Swing method (native subset)");
    }
    static void évènementDistribuerMessage(int adresseCible, int numéroÉvènement, boolean français) {
        if (adresseCible < 1 || valeurTas[adresseCible] < 32) { valeurÉchec("Java event listener required"); return; }
        int indiceFichier = méthodeNom(valeurTas[adresseCible] - 32, numéroÉvènement == 0 ? (français ? "exécuterTâche" : "run") : (français ? "recevoirAction" : "actionPerformed"), numéroÉvènement == 0 ? "()V" : (français ? "(Lfrançais/interne/NotificationAction;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (indiceFichier < 0) { valeurÉchec("event callback missing"); return; }
        filExécutionActuel = 0; nombreÉlémentsFilExécution = 1; indiceCadre = 0; étatValeurFilExécution[0] = 1; pileCadre[0] = 0; verrouCadre[0] = initialiserCadre[0] = 0; changerRequête = false;
        for (int indiceBoucle = 0; indiceBoucle < 128; indiceBoucle++) { valeurLocal[indiceBoucle] = typeLocal[indiceBoucle] = 0; }
        méthodeCadre[0] = indiceFichier; positionCadre[0] = démarrerMéthode[indiceFichier]; valeurLocal[0] = adresseCible; typeLocal[0] = 2;
        if (numéroÉvènement != 0) { valeurLocal[1] = numéroÉvènement; typeLocal[1] = 2; }
        estÉvènementTraitementÉtat = true; exécuterCommande(); estÉvènementTraitementÉtat = false;
    }
    static void évènementsÉcran() {
        while (!erreur) {
            if (nombreÉlémentsUltérieur > 0) { int adresseCible = ultérieurPlanification[0], français = valeurCoréenUltérieur[0]; for (int indiceBoucle = 1; indiceBoucle < nombreÉlémentsUltérieur; indiceBoucle++) { ultérieurPlanification[indiceBoucle - 1] = ultérieurPlanification[indiceBoucle]; valeurCoréenUltérieur[indiceBoucle - 1] = valeurCoréenUltérieur[indiceBoucle]; } ultérieurPlanification[--nombreÉlémentsUltérieur] = 0; valeurCoréenUltérieur[nombreÉlémentsUltérieur] = 0; évènementDistribuerMessage(adresseCible, 0, français != 0); continue; }
            if (Utilisateur.connexionÉcran(6, 0, 0, 0, 0, 0) == 0) return;
            int numéroÉvènement = Utilisateur.connexionÉcran(5, 0, 0, 0, 0, 0); if (numéroÉvènement == 0) continue;
            if (numéroÉvènement < 0) { valeurÉchec("GUI event I/O failed"); return; }
            int valeurIdentité = numéroÉvènement & 65535; if (valeurIdentité < 1 || valeurIdentité > 32) continue; int référenceObjet = référenceÉcran[valeurIdentité - 1]; if (référenceObjet == 0) continue;
            if ((numéroÉvènement & 65536) != 0) {
                if (valeurTas[référenceObjet + 10] != 0) valeurTas[référenceObjet + 9] = 0;
                if (valeurTas[référenceObjet + 10] == 3) for (int indiceBoucle = 0; indiceBoucle < 32; indiceBoucle++) if (référenceÉcran[indiceBoucle] != 0 && valeurTas[référenceÉcran[indiceBoucle]] == 24) Utilisateur.connexionÉcran(4, indiceBoucle + 1, 0, 0, 0, 0);
            } else if (valeurTas[référenceObjet + 4] != 0) {
                int référenceLisezMoi = allouerStockage(29, 2); if (erreur) return; valeurTas[référenceLisezMoi + 2] = référenceObjet; valeurTas[référenceLisezMoi + 3] = valeurTas[référenceObjet + 12]; référenceTas[référenceLisezMoi + 2] = 1; évènementDistribuerMessage(valeurTas[référenceObjet + 4], référenceLisezMoi, valeurTas[référenceObjet + 12] != 0);
            }
        }
    }
    public static int lancer() {
        if (Utilisateur.nombreÉlémentsArguments() == 1 && OutilJava.texteÉgal(Utilisateur.arguments(0), "-version")) {
            Utilisateur.écrire("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (Utilisateur.nombreÉlémentsArguments() < 1) { Utilisateur.écrire("Usage: java CLASS [ARGS]\n"); return 2; }
        définitionClasseEntréeÉlément = chargerDéfinitionClasse(caractèreHôte(Utilisateur.arguments(0))); if (erreur || définitionClasseEntréeÉlément < 0) return 1;
        int valeurPointEntréeÉlément = méthodeNom(définitionClasseEntréeÉlément, "lancer", "()V");
        boolean entréeÉlémentCoréen = valeurPointEntréeÉlément >= 0 && (accèsMéthode[valeurPointEntréeÉlément] & 9) == 9;
        if (!entréeÉlémentCoréen) valeurPointEntréeÉlément = méthodeNom(définitionClasseEntréeÉlément, "main", "([Ljava/lang/String;)V");
        if (valeurPointEntréeÉlément < 0 || (accèsMéthode[valeurPointEntréeÉlément] & 9) != 9) valeurÉchec("public static void lancer() or main(String[] args) required");
        if (erreur) return 1;
        int arguments = allouerStockage(3, Utilisateur.nombreÉlémentsArguments() - 1); élémentTableau[arguments] = -1;
        for (int nombre = 1; nombre < Utilisateur.nombreÉlémentsArguments() && !erreur; nombre++) valeurTas[arguments + 1 + nombre] = caractèreHôte(Utilisateur.arguments(nombre));
        indiceCadre = 0; méthodeCadre[0] = valeurPointEntréeÉlément; positionCadre[0] = démarrerMéthode[valeurPointEntréeÉlément]; valeurLocal[0] = entréeÉlémentCoréen ? 0 : arguments; typeLocal[0] = entréeÉlémentCoréen ? 0 : 2;
        étatValeurFilExécution[0] = 1; objetFilExécution[0] = allouerStockage(13, 2);
        exécuterCommande(); if (!erreur) évènementsÉcran(); return erreur ? 1 : 0;
    }
}

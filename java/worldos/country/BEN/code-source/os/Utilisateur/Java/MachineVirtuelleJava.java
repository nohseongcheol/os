// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** JVM restreinte exécutée en ring 3. Vérifie à l’exécution les limites des fichiers, de la pile, des références et des branchements. */
public final class MachineVirtuelleJava {
    static int[] Fichier = new int[16384], texteNomFichier = new int[64];
    static int[] baliseConstante = new int[512], valeurPremierConstante = new int[512], valeurDeuxièmeConstante = new int[512], référenceChaîne = new int[512];
    static int[] texteNomMéthode = new int[32], typeMéthode = new int[32], accèsMéthode = new int[32];
    static int[] démarrerMéthode = new int[32], finMéthode = new int[32], pileMéthode = new int[32], variablesLocalesMéthode = new int[32];
    static int[] nombreÉlémentsArgumentMéthode = new int[32], typeArgumentMéthode = new int[512], retournerMéthode = new int[32];
    static int[] valeurFrontière = new int[16384];
    static int[] valeurLocal = new int[4096], typeLocal = new int[4096], valeurPileOpérande = new int[4096], typePileOpérande = new int[4096];
    static int[] méthodeCadre = new int[32], positionCadre = new int[32], pileCadre = new int[32];
    static int[] valeurTas = new int[8192];
    static int taille, lirePosition, nombreÉlémentsConstante, nombreÉlémentsMéthode, nomClasse, indiceCadre = -1, positionFinTas = 1, typeRetourner;
    static boolean erreur;

    static void valeurÉchec(String texteMot) {
        if (!erreur) { Utilisateur.écrire("JVM error: "); Utilisateur.écrire(texteMot); Utilisateur.écrireValeurCaractère(10); }
        erreur = true;
    }
    static boolean rogner(int lancer, int longueur) { return lancer >= 0 && longueur >= 0 && lancer <= taille - longueur; }
    static int valeurOctet() {
        if (!rogner(lirePosition, 1)) { valeurÉchec("truncated class file"); return 0; }
        return Fichier[lirePosition++];
    }
    static int valeurCourt() { return valeurOctet() << 8 | valeurOctet(); }
    static int Entier() { return valeurCourt() << 16 | valeurCourt(); }
    static void sauterOctets(int longueur) { if (!rogner(lirePosition, longueur)) valeurÉchec("invalid attribute size"); else lirePosition += longueur; }
    static boolean contrôlerConstante(int nombre, int valeurGenre) {
        if (nombre <= 0 || nombre >= nombreÉlémentsConstante || baliseConstante[nombre] != valeurGenre) { valeurÉchec("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean plageTexte(int lancer, int longueur, String texteMot) {
        if (!rogner(lancer, longueur) || longueur != texteMot.length()) return false;
        for (int nombre = 0; nombre < longueur; nombre++) if (Fichier[lancer + nombre] != texteMot.charAt(nombre)) return false;
        return true;
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
    static void sauterAttribut() {
        int nombreÉlémentsÉlémentListe = valeurCourt();
        for (int nombre = 0; nombre < nombreÉlémentsÉlémentListe && !erreur; nombre++) { contrôlerConstante(valeurCourt(), 1); sauterOctets(Entier()); }
    }
    static int longueurCommande(int valeur) {
        if (valeur == 16 || valeur == 18 || valeur == 21 || valeur == 25 || valeur == 54 || valeur == 58 || valeur == 188) return 2;
        if (valeur == 17 || valeur == 19 || valeur == 132 || valeur >= 153 && valeur <= 167
            || valeur >= 178 && valeur <= 184 || valeur == 187 || valeur == 189 || valeur == 192 || valeur == 198 || valeur == 199) return 3;
        if (valeur >= 0 && valeur <= 8 || valeur >= 26 && valeur <= 29 || valeur >= 42 && valeur <= 46 || valeur == 50
            || valeur >= 59 && valeur <= 62 || valeur >= 75 && valeur <= 79 || valeur == 83 || valeur == 87 || valeur == 89 || valeur == 95
            || valeur == 96 || valeur == 100 || valeur == 104 || valeur == 108 || valeur == 112 || valeur == 116
            || valeur == 120 || valeur == 122 || valeur == 124 || valeur == 126 || valeur == 128 || valeur == 130
            || valeur >= 145 && valeur <= 147 || valeur == 172 || valeur == 176 || valeur == 177 || valeur == 190) return 1;
        return 0;
    }
    static void lireClasse() {
        if (Entier() != 0xcafebabe) valeurÉchec("not a class file");
        int révisionMineur = valeurCourt(), valeurVersion = valeurCourt();
        if (valeurVersion < 45 || valeurVersion > 52 || révisionMineur != 0) valeurÉchec("supported class versions: 45..52, minor 0");
        nombreÉlémentsConstante = valeurCourt();
        if (nombreÉlémentsConstante < 1 || nombreÉlémentsConstante > 512) { valeurÉchec("constant pool limit (511)"); return; }
        for (int nombre = 1; nombre < nombreÉlémentsConstante && !erreur; nombre++) {
            int valeurGenre = valeurOctet(); baliseConstante[nombre] = valeurGenre;
            if (valeurGenre == 1) { valeurDeuxièmeConstante[nombre] = valeurCourt(); valeurPremierConstante[nombre] = lirePosition; sauterOctets(valeurDeuxièmeConstante[nombre]); }
            else if (valeurGenre == 3) valeurPremierConstante[nombre] = Entier();
            else if (valeurGenre == 7 || valeurGenre == 8) valeurPremierConstante[nombre] = valeurCourt();
            else if (valeurGenre == 9 || valeurGenre == 10 || valeurGenre == 12) { valeurPremierConstante[nombre] = valeurCourt(); valeurDeuxièmeConstante[nombre] = valeurCourt(); }
            else valeurÉchec("unsupported constant type");
        }
        int valeurPermission = valeurCourt();
        if ((valeurPermission & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) valeurÉchec("unsupported class flags");
        nomClasse = texteNomClasse(valeurCourt());
        if (!texteMot(texteNomClasse(valeurCourt()), "java/lang/Object")) valeurÉchec("inheritance unsupported");
        if (valeurCourt() != 0) valeurÉchec("interfaces unsupported");
        if (valeurCourt() != 0) valeurÉchec("fields unsupported");
        nombreÉlémentsMéthode = valeurCourt();
        if (nombreÉlémentsMéthode < 1 || nombreÉlémentsMéthode > 32) { valeurÉchec("method count limit (32)"); return; }
        for (int nombre = 0; nombre < nombreÉlémentsMéthode && !erreur; nombre++) {
            accèsMéthode[nombre] = valeurCourt(); texteNomMéthode[nombre] = valeurCourt(); typeMéthode[nombre] = valeurCourt();
            contrôlerConstante(texteNomMéthode[nombre], 1); lireDescripteur(nombre);
            if ((accèsMéthode[nombre] & (0x100 | 0x400 | 0x20)) != 0) valeurÉchec("native, abstract and synchronized methods unsupported");
            if ((accèsMéthode[nombre] & 8) == 0 && !texteMot(texteNomMéthode[nombre], "<init>")) valeurÉchec("instance methods unsupported");
            if (texteMot(texteNomMéthode[nombre], "<clinit>")) valeurÉchec("class initializers unsupported");
            for (int valeurAvantCôté = 0; valeurAvantCôté < nombre; valeurAvantCôté++) if (motConcordant(texteNomMéthode[valeurAvantCôté], texteNomMéthode[nombre]) && motConcordant(typeMéthode[valeurAvantCôté], typeMéthode[nombre])) valeurÉchec("duplicate method");
            int nombreÉlémentsÉlémentListe = valeurCourt();
            for (int valeurAttribut = 0; valeurAttribut < nombreÉlémentsÉlémentListe && !erreur; valeurAttribut++) {
                int nom = valeurCourt(), longueur = Entier(), lancer = lirePosition;
                if (!rogner(lancer, longueur)) { valeurÉchec("truncated method attribute"); break; }
                if (texteMot(nom, "Code")) {
                    if (démarrerMéthode[nombre] != 0) valeurÉchec("duplicate Code attribute");
                    pileMéthode[nombre] = valeurCourt(); variablesLocalesMéthode[nombre] = valeurCourt(); int longueurCode = Entier();
                    if (pileMéthode[nombre] > 128 || variablesLocalesMéthode[nombre] > 128 || variablesLocalesMéthode[nombre] < nombreÉlémentsArgumentMéthode[nombre]
                        || longueurCode < 1 || longueurCode > 8192) valeurÉchec("method memory limits exceeded");
                    démarrerMéthode[nombre] = lirePosition; sauterOctets(longueurCode); finMéthode[nombre] = lirePosition;
                    if (valeurCourt() != 0) valeurÉchec("exception handlers unsupported");
                    sauterAttribut();
                    if (lirePosition != lancer + longueur) valeurÉchec("Code attribute size mismatch");
                } else sauterOctets(longueur);
            }
            if (démarrerMéthode[nombre] == 0) valeurÉchec("missing Code attribute");
            int entréeÉlémentEmplacement = démarrerMéthode[nombre];
            while (entréeÉlémentEmplacement < finMéthode[nombre] && !erreur) {
                int longueur = longueurCommande(Fichier[entréeÉlémentEmplacement]);
                if (longueur == 0 || longueur > finMéthode[nombre] - entréeÉlémentEmplacement) { valeurÉchec("unsupported or truncated bytecode"); break; }
                valeurFrontière[entréeÉlémentEmplacement] = nombre + 1; entréeÉlémentEmplacement += longueur;
            }
            // Refuser les cibles de branchement incorrectes même dans les chemins jamais exécutés.
            entréeÉlémentEmplacement = démarrerMéthode[nombre];
            while (entréeÉlémentEmplacement < finMéthode[nombre] && !erreur) {
                int valeur = Fichier[entréeÉlémentEmplacement];
                if (valeur >= 153 && valeur <= 167 || valeur == 198 || valeur == 199) {
                    int valeurDestination = entréeÉlémentEmplacement + (short)(Fichier[entréeÉlémentEmplacement + 1] << 8 | Fichier[entréeÉlémentEmplacement + 2]);
                    if (valeurDestination < démarrerMéthode[nombre] || valeurDestination >= finMéthode[nombre] || valeurFrontière[valeurDestination] != nombre + 1) valeurÉchec("invalid branch target");
                }
                entréeÉlémentEmplacement += longueurCommande(valeur);
            }
        }
        if (!erreur) sauterAttribut();
        if (lirePosition != taille) valeurÉchec("extra class file data");
    }
    static int allouerStockage(int valeurGenre, int longueur) {
        if (longueur < 0 || longueur > valeurTas.length - positionFinTas - 2) { valeurÉchec("object heap exhausted or negative array size"); return 0; }
        int référence = positionFinTas; positionFinTas += longueur + 2; valeurTas[référence] = valeurGenre; valeurTas[référence + 1] = longueur;
        return référence;
    }
    static boolean valeurObjet(int référence, int valeurGenre) {
        if (référence < 1 || référence >= positionFinTas - 1 || valeurTas[référence] != valeurGenre) { valeurÉchec("null or invalid object reference"); return false; }
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
        if (indiceCadre == 31) { valeurÉchec("call stack limit (32)"); return; }
        int élémentListeSuivant = indiceCadre + 1;
        for (int nombre = 0; nombre < 128; nombre++) typeLocal[élémentListeSuivant * 128 + nombre] = 0;
        for (int nombre = nombreÉlémentsArgumentMéthode[Fonction] - 1; nombre >= 0; nombre--) {
            valeurLocal[élémentListeSuivant * 128 + nombre] = soustraireValeurs(typeArgumentMéthode[Fonction * 16 + nombre]); typeLocal[élémentListeSuivant * 128 + nombre] = typeArgumentMéthode[Fonction * 16 + nombre];
        }
        indiceCadre = élémentListeSuivant; méthodeCadre[indiceCadre] = Fonction; positionCadre[indiceCadre] = démarrerMéthode[Fonction]; pileCadre[indiceCadre] = 0;
    }
    static void résultatRetourner(int valeurType) {
        if (valeurType != retournerMéthode[méthodeCadre[indiceCadre]]) { valeurÉchec("return type mismatch"); return; }
        int valeur = valeurType == 0 ? 0 : soustraireValeurs(valeurType);
        indiceCadre--; if (indiceCadre >= 0 && valeurType != 0) placerValeur(valeur, valeurType);
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
                if (valeur < 1 || valeur > 127) { valeurÉchec("file stream paths currently require ASCII"); return; }
                nomFichierFlux[entréeÉlémentEmplacement] = valeur;
            }
            nomFichierFlux[longueur] = 0;
            int entréeÉlémentDescripteur = Utilisateur.ouvrirDescripteurFichier(nomFichierFlux, Sortie ? (valeurContinuation ? 1089 : 577) : 0);
            if (entréeÉlémentDescripteur < 0) { valeurÉchec("FileNotFoundException: file open failed"); return; }
            valeurTas[valeurFlux + 2] = entréeÉlémentDescripteur; valeurTas[valeurFlux + 3] = 1;
            return;
        }
        if (commande != 182) { valeurÉchec("invalid file stream invocation"); return; }
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
            if (résultat < -1) valeurÉchec("IOException: read failed"); else placerValeur(résultat, 1);
        } else if (Utilisateur.écrireOctetFichierUn(entréeÉlémentDescripteur, valeur) != 1) valeurÉchec("IOException: write failed");
    }
    static void appelMéthode(int numéro, int commande) {
        if (!contrôlerConstante(numéro, 10)) return;
        int valeurPropriétaire = texteNomClasse(valeurPremierConstante[numéro]), nom = nomRéférence(valeurDeuxièmeConstante[numéro]), valeurFormat = typeRéférence(valeurDeuxièmeConstante[numéro]);
        if (erreur) return;
        if (motConcordant(valeurPropriétaire, nomClasse)) {
            if (commande != 184) { valeurÉchec("only static user methods are supported"); return; }
            for (int nombre = 0; nombre < nombreÉlémentsMéthode; nombre++) if (motConcordant(nom, texteNomMéthode[nombre]) && motConcordant(valeurFormat, typeMéthode[nombre])) {
                if ((accèsMéthode[nombre] & 8) == 0) valeurÉchec("method is not static"); else invoquer(nombre);
                return;
            }
            valeurÉchec("NoSuchMethodError"); return;
        }
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
        valeurÉchec("unsupported library method");
    }
    static int emplacementTableau(int référence, int valeurIndiceTableau, int valeurType) {
        if (!valeurObjet(référence, valeurType)) return 0;
        if (valeurIndiceTableau < 0 || valeurIndiceTableau >= valeurTas[référence + 1]) { valeurÉchec("ArrayIndexOutOfBoundsException"); return 0; }
        return référence + 2 + valeurIndiceTableau;
    }
    static void exécuterCommande() {
        int donnéesResteDivision = 500000;
        while (indiceCadre >= 0 && !erreur) {
            if (--donnéesResteDivision == 0) { valeurÉchec("instruction limit (500000)"); break; }
            int lancer = positionCadre[indiceCadre], valeur = lireOctetCodeOpération();
            if (erreur) break;
            if (valeur == 0) continue;
            if (valeur == 1) { placerValeur(0, 2); continue; }
            if (valeur >= 2 && valeur <= 8) { placerValeur(valeur - 3, 1); continue; }
            if (valeur == 16) { placerValeur((byte)lireOctetCodeOpération(), 1); continue; }
            if (valeur == 17) { placerValeur((short)lireCourtCodeOpération(), 1); continue; }
            if (valeur == 18 || valeur == 19) {
                int nombre = valeur == 18 ? lireOctetCodeOpération() : lireCourtCodeOpération();
                if (nombre <= 0 || nombre >= nombreÉlémentsConstante) valeurÉchec("invalid ldc constant");
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
            if (valeur == 46 || valeur == 50) {
                int valeurIndiceTableau = soustraireValeurs(1), référence = soustraireValeurs(2), entréeÉlémentEmplacement = emplacementTableau(référence, valeurIndiceTableau, valeur == 46 ? 2 : 3);
                if (!erreur) placerValeur(valeurTas[entréeÉlémentEmplacement], valeur == 46 ? 1 : 2); continue;
            }
            if (valeur == 79 || valeur == 83) {
                int élémentÉlémentListe = soustraireValeurs(valeur == 79 ? 1 : 2), valeurIndiceTableau = soustraireValeurs(1), référence = soustraireValeurs(2), entréeÉlémentEmplacement = emplacementTableau(référence, valeurIndiceTableau, valeur == 79 ? 2 : 3);
                if (valeur == 83 && élémentÉlémentListe != 0) valeurObjet(élémentÉlémentListe, 1);
                if (!erreur) valeurTas[entréeÉlémentEmplacement] = élémentÉlémentListe; continue;
            }
            if (valeur == 87) { soustraireValeurs(0); continue; }
            if (valeur == 89) { int opérandePremier = soustraireValeurs(0), valeurType = typeRetourner; placerValeur(opérandePremier, valeurType); placerValeur(opérandePremier, valeurType); continue; }
            if (valeur == 95) { int opérandePremier = soustraireValeurs(0), typeOpérandePremier = typeRetourner, opérandeDeuxième = soustraireValeurs(0), typeOpérandeDeuxième = typeRetourner; placerValeur(opérandePremier, typeOpérandePremier); placerValeur(opérandeDeuxième, typeOpérandeDeuxième); continue; }
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
            if (valeur == 178) {
                int nombre = lireCourtCodeOpération(); if (!contrôlerConstante(nombre, 9)) continue;
                if (!texteMot(texteNomClasse(valeurPremierConstante[nombre]), "java/lang/System") || !texteMot(nomRéférence(valeurDeuxièmeConstante[nombre]), "out")
                    || !texteMot(typeRéférence(valeurDeuxièmeConstante[nombre]), "Ljava/io/PrintStream;")) valeurÉchec("unsupported static field");
                else placerValeur(-1, 2); continue;
            }
            if (valeur == 182 || valeur == 183 || valeur == 184) { appelMéthode(lireCourtCodeOpération(), valeur); continue; }
            if (valeur == 187) {
                int nom = texteNomClasse(lireCourtCodeOpération());
                if (texteMot(nom, "java/lang/StringBuilder")) placerValeur(allouerStockage(4, 1), 2);
                else if (texteMot(nom, "java/io/FileInputStream") || texteMot(nom, "java/io/FileOutputStream")) {
                    int référence = allouerStockage(texteMot(nom, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!erreur) { valeurTas[référence + 2] = -1; placerValeur(référence, 2); }
                } else valeurÉchec("unsupported object construction");
                continue;
            }
            if (valeur == 188 || valeur == 189) {
                if (valeur == 188) { if (lireOctetCodeOpération() != 10) valeurÉchec("only int[] newarray is supported"); }
                else if (!texteMot(texteNomClasse(lireCourtCodeOpération()), "java/lang/String")) valeurÉchec("only String[] anewarray is supported");
                int longueur = soustraireValeurs(1); placerValeur(allouerStockage(valeur == 188 ? 2 : 3, longueur), 2); continue;
            }
            if (valeur == 190) {
                int référence = soustraireValeurs(2);
                if (référence < 1 || référence >= positionFinTas - 1 || (valeurTas[référence] != 2 && valeurTas[référence] != 3)) valeurÉchec("null or invalid array");
                else placerValeur(valeurTas[référence + 1], 1); continue;
            }
            if (valeur == 192) {
                int nom = texteNomClasse(lireCourtCodeOpération()), référence = soustraireValeurs(2);
                if (!texteMot(nom, "java/lang/String")) valeurÉchec("unsupported checkcast");
                else if (référence != 0) valeurObjet(référence, 1);
                placerValeur(référence, 2); continue;
            }
            valeurÉchec("unsupported bytecode");
        }
    }
    public static int lancer() {
        if (Utilisateur.nombreÉlémentsArguments() == 1 && OutilJava.texteÉgal(Utilisateur.arguments(0), "-version")) {
            Utilisateur.écrire("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (Utilisateur.nombreÉlémentsArguments() < 1) { Utilisateur.écrire("Usage: java CLASS [ARGS]\n"); return 2; }
        int longueur = OutilJava.nom(texteNomFichier, Utilisateur.arguments(0));
        if (longueur < 1 || longueur > 57) { Utilisateur.écrire("java: invalid class name\n"); return 2; }
        texteNomFichier[longueur] = '.'; texteNomFichier[longueur + 1] = 'c'; texteNomFichier[longueur + 2] = 'l'; texteNomFichier[longueur + 3] = 'a'; texteNomFichier[longueur + 4] = 's'; texteNomFichier[longueur + 5] = 's';
        taille = Utilisateur.lireFichier(texteNomFichier, Fichier);
        if (taille < 0) { Utilisateur.écrire("java: cannot read class: "); OutilJava.écrireNuméro(taille); Utilisateur.écrireValeurCaractère(10); return 1; }
        lireClasse(); if (erreur) return 1;
        int nomCaractère = texteConstante(nomClasse);
        if (!erreur && valeurTas[nomCaractère + 1] != longueur) valeurÉchec("class name does not match file");
        for (int nombre = 0; nombre < longueur && !erreur; nombre++) if (valeurTas[nomCaractère + 2 + nombre] != texteNomFichier[nombre]) valeurÉchec("class name does not match file");
        int valeurPointEntréeÉlément = -1;
        for (int nombre = 0; nombre < nombreÉlémentsMéthode; nombre++) if (texteMot(texteNomMéthode[nombre], "main") && texteMot(typeMéthode[nombre], "([Ljava/lang/String;)V") && (accèsMéthode[nombre] & 9) == 9) valeurPointEntréeÉlément = nombre;
        if (valeurPointEntréeÉlément < 0) valeurÉchec("public static void main(String[] args) required");
        if (erreur) return 1;
        int arguments = allouerStockage(3, Utilisateur.nombreÉlémentsArguments() - 1);
        for (int nombre = 1; nombre < Utilisateur.nombreÉlémentsArguments() && !erreur; nombre++) valeurTas[arguments + 1 + nombre] = caractèreHôte(Utilisateur.arguments(nombre));
        indiceCadre = 0; méthodeCadre[0] = valeurPointEntréeÉlément; positionCadre[0] = démarrerMéthode[valeurPointEntréeÉlément]; valeurLocal[0] = arguments; typeLocal[0] = 2;
        exécuterCommande(); return erreur ? 1 : 0;
    }
}

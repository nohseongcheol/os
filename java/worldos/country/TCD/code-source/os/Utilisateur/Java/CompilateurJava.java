// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Compilateur Java restreint exécuté dans l’invité, produisant des fichiers de classes standard de version 49. */
public final class CompilateurJava {
    static int[] source = new int[16384], Sortie = new int[16384], valeurCode = new int[4096];
    static int[] genreJeton = new int[2048], positionJeton = new int[2048], longueurJeton = new int[2048];
    static int[] valeurConstante = new int[4096], décalageConstante = new int[512];
    static int[] Caractères = new int[512], texteNomFichier = new int[64];
    static int[] codeInséré = new int[16];
    static int tailleSource, nombreÉlémentsJeton, position, tailleCode, tailleConstante, nombreÉlémentsConstante = 1, tailleSortie, longueurCaractère;
    static boolean erreur;
    static int jetonClasse, constanteClasse, constanteParent, constanteCode;
    static int[] nomEntréeÉlémentMéthode = new int[32], retournerMéthode = new int[32], nombreÉlémentsArgumentMéthode = new int[32];
    static int[] nomArgumentMéthode = new int[512], typeArgumentMéthode = new int[512];
    static int[] corpsMéthode = new int[32], finMéthode = new int[32], codeMéthode = new int[32];
    static int[] longueurMéthode = new int[32], variablesLocalesMéthode = new int[32], constanteNomMéthode = new int[32], constanteDescripteurMéthode = new int[32];
    static int[] accèsMéthode = new int[32];
    static int nombreÉlémentsMéthode, méthodeActuel, nombreÉlémentsLocal, valeurProfondeur, profondeurExpression;
    static int[] nomLocal = new int[128], typeLocal = new int[128], profondeurLocal = new int[128];

    static void valeurÉchec(String valeurRaison) {
        if (!erreur) {
            Utilisateur.écrire("javac error: "); Utilisateur.écrire(valeurRaison);
            Utilisateur.écrire(" at line ");
            int ligne = 1, terminaison = position < nombreÉlémentsJeton ? positionJeton[position] : tailleSource;
            for (int nombre = 0; nombre < terminaison; nombre++) if (source[nombre] == 10) ligne++;
            OutilJava.écrireNuméro(ligne); Utilisateur.écrireValeurCaractère(10);
        }
        erreur = true;
    }
    static boolean valeurCaractère(int valeur) { return RèglesCaractèresIdentifiants.caractèrePremier(valeur); }
    static boolean valeurChiffre(int valeur) { return valeur >= '0' && valeur <= '9'; }
    static boolean égalNoms(int opérandePremier, int opérandeDeuxième) {
        if (opérandePremier < 0 || opérandeDeuxième < 0 || opérandePremier >= nombreÉlémentsJeton || opérandeDeuxième >= nombreÉlémentsJeton || longueurJeton[opérandePremier] != longueurJeton[opérandeDeuxième]) return false;
        for (int nombre = 0; nombre < longueurJeton[opérandePremier]; nombre++) if (source[positionJeton[opérandePremier] + nombre] != source[positionJeton[opérandeDeuxième] + nombre]) return false;
        return true;
    }
    static boolean valeurMot(int valeurJeton, String texteMot) {
        if (valeurJeton < 0 || valeurJeton >= nombreÉlémentsJeton || longueurJeton[valeurJeton] != texteMot.length()) return false;
        for (int nombre = 0; nombre < texteMot.length(); nombre++) if (source[positionJeton[valeurJeton] + nombre] != texteMot.charAt(nombre)) return false;
        return true;
    }
    static int valeurGenre() { return position < nombreÉlémentsJeton ? genreJeton[position] : 0; }
    static boolean recevoir(int valeur) { if (valeurGenre() != valeur) return false; position++; return true; }
    static void valeurExigence(int valeur) { if (!recevoir(valeur)) valeurÉchec("unexpected token"); }
    static boolean motPrendre(String texteMot) { if (!valeurMot(position, texteMot)) return false; position++; return true; }
    static void motExiger(String texteMot) { if (!motPrendre(texteMot)) valeurÉchec(texteMot); }
    static int valeurIdentificateur() {
        int résultat = position;
        if (valeurGenre() != 256) valeurÉchec("identifier required"); else position++;
        String motsRéservé = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int lancer = 0;
        for (int nombre = 0; nombre <= motsRéservé.length(); nombre++) {
            if (nombre == motsRéservé.length() || motsRéservé.charAt(nombre) == ' ') {
                boolean texteÉgal = nombre - lancer == longueurJeton[résultat];
                for (int entréeÉlémentEmplacement = lancer; texteÉgal && entréeÉlémentEmplacement < nombre; entréeÉlémentEmplacement++) if (motsRéservé.charAt(entréeÉlémentEmplacement) != source[positionJeton[résultat] + entréeÉlémentEmplacement - lancer]) texteÉgal = false;
                if (texteÉgal) valeurÉchec("reserved word cannot be an identifier");
                lancer = nombre + 1;
            }
        }
        return résultat;
    }
    static void valeurCouper() {
        int nombre = 0;
        while (nombre < tailleSource && !erreur) {
            int valeur = source[nombre], lancer = nombre, valeurGenre = valeur;
            if (valeur == 32 || valeur == 9 || valeur == 10 || valeur == 13) { nombre++; continue; }
            if (valeur == '/' && nombre + 1 < tailleSource && source[nombre + 1] == '/') {
                while (nombre < tailleSource && source[nombre] != 10) nombre++;
                continue;
            }
            if (valeur == '/' && nombre + 1 < tailleSource && source[nombre + 1] == '*') {
                nombre += 2;
                while (nombre + 1 < tailleSource && !(source[nombre] == '*' && source[nombre + 1] == '/')) nombre++;
                if (nombre + 1 >= tailleSource) { valeurÉchec("unterminated comment"); break; }
                nombre += 2; continue;
            }
            if (valeurCaractère(valeur)) { valeurGenre = 256; while (nombre < tailleSource && RèglesCaractèresIdentifiants.caractèreContinuation(source[nombre])) nombre++; }
            else if (valeurChiffre(valeur)) { valeurGenre = 257; while (nombre < tailleSource && valeurChiffre(source[nombre])) nombre++; }
            else if (valeur == '"' || valeur == '\'') {
                valeurGenre = valeur == '"' ? 258 : 259; nombre++;
                while (nombre < tailleSource && source[nombre] != valeur && source[nombre] != 10 && source[nombre] != 13) {
                    if (source[nombre] == '\\') nombre++;
                    nombre++;
                }
                if (nombre >= tailleSource || source[nombre] != valeur) { valeurÉchec("unterminated literal"); break; }
                nombre++;
            } else {
                nombre++;
                if (nombre < tailleSource) {
                    int élémentListeSuivant = source[nombre];
                    if (valeur == '=' && élémentListeSuivant == '=') valeurGenre = 300;
                    if (valeur == '!' && élémentListeSuivant == '=') valeurGenre = 301;
                    if (valeur == '<' && élémentListeSuivant == '=') valeurGenre = 302;
                    if (valeur == '>' && élémentListeSuivant == '=') valeurGenre = 303;
                    if (valeur == '&' && élémentListeSuivant == '&') valeurGenre = 304;
                    if (valeur == '|' && élémentListeSuivant == '|') valeurGenre = 305;
                    if (valeur == '+' && élémentListeSuivant == '+') valeurGenre = 306;
                    if (valeur == '-' && élémentListeSuivant == '-') valeurGenre = 307;
                    if (valeur == '+' && élémentListeSuivant == '=') valeurGenre = 308;
                    if (valeur == '-' && élémentListeSuivant == '=') valeurGenre = 309;
                    if (valeur == '*' && élémentListeSuivant == '=') valeurGenre = 310;
                    if (valeur == '/' && élémentListeSuivant == '=') valeurGenre = 311;
                    if (valeur == '%' && élémentListeSuivant == '=') valeurGenre = 312;
                    if (valeurGenre >= 300) nombre++;
                }
            }
            if (nombreÉlémentsJeton == genreJeton.length - 1) { valeurÉchec("too many tokens (2047 maximum)"); break; }
            genreJeton[nombreÉlémentsJeton] = valeurGenre; positionJeton[nombreÉlémentsJeton] = lancer; longueurJeton[nombreÉlémentsJeton++] = nombre - lancer;
        }
    }
    static void écrireOctetConstante(int valeur) {
        if (tailleConstante == valeurConstante.length) { valeurÉchec("constant pool too large"); return; }
        valeurConstante[tailleConstante++] = valeur & 255;
    }
    static void écrireCourtConstante(int valeur) { écrireOctetConstante(valeur >> 8); écrireOctetConstante(valeur); }
    static int registreConstante(int lancer) {
        for (int nombre = 1; nombre < nombreÉlémentsConstante; nombre++) {
            int valeurAvantCôté = décalageConstante[nombre], longueur = (nombre + 1 < nombreÉlémentsConstante ? décalageConstante[nombre + 1] : lancer) - valeurAvantCôté;
            if (longueur != tailleConstante - lancer) continue;
            boolean texteÉgal = true;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueur; entréeÉlémentEmplacement++) if (valeurConstante[valeurAvantCôté + entréeÉlémentEmplacement] != valeurConstante[lancer + entréeÉlémentEmplacement]) texteÉgal = false;
            if (texteÉgal) { tailleConstante = lancer; return nombre; }
        }
        if (nombreÉlémentsConstante == décalageConstante.length) { valeurÉchec("too many constants"); return 0; }
        décalageConstante[nombreÉlémentsConstante] = lancer;
        return nombreÉlémentsConstante++;
    }
    static void ajouterFinTexte(int valeur) {
        if (longueurCaractère == Caractères.length) { valeurÉchec("text too long"); return; }
        Caractères[longueurCaractère++] = valeur;
    }
    static void ajouterFinMot(String texteMot) { for (int nombre = 0; nombre < texteMot.length(); nombre++) ajouterFinTexte(texteMot.charAt(nombre)); }
    static int constanteCaractère() {
        int lancer = tailleConstante; écrireOctetConstante(1); écrireCourtConstante(0);
        for (int nombre = 0; nombre < longueurCaractère; nombre++) {
            int valeur = Caractères[nombre];
            if (valeur > 0 && valeur < 128) écrireOctetConstante(valeur);
            else if (valeur < 2048) { écrireOctetConstante(192 | valeur >> 6); écrireOctetConstante(128 | valeur & 63); }
            else { écrireOctetConstante(224 | valeur >> 12); écrireOctetConstante(128 | valeur >> 6 & 63); écrireOctetConstante(128 | valeur & 63); }
        }
        if (erreur) return 0;
        int longueur = tailleConstante - lancer - 3;
        valeurConstante[lancer + 1] = longueur >> 8; valeurConstante[lancer + 2] = longueur & 255;
        return registreConstante(lancer);
    }
    static int constanteMot(String texteMot) { longueurCaractère = 0; ajouterFinMot(texteMot); return constanteCaractère(); }
    static int constanteJeton(int valeurJeton) {
        longueurCaractère = 0;
        for (int nombre = 0; nombre < longueurJeton[valeurJeton]; nombre++) ajouterFinTexte(source[positionJeton[valeurJeton] + nombre]);
        return constanteCaractère();
    }
    static int référence(int valeurGenre, int opérandePremier, int opérandeDeuxième) {
        int lancer = tailleConstante; écrireOctetConstante(valeurGenre); écrireCourtConstante(opérandePremier);
        if (valeurGenre == 9 || valeurGenre == 10 || valeurGenre == 12) écrireCourtConstante(opérandeDeuxième);
        return registreConstante(lancer);
    }
    static int référenceExtérieur(int valeurGenre, String valeurPropriétaire, String nom, String valeurDescription) {
        int identificateurPropriétaire = référence(7, constanteMot(valeurPropriétaire), 0);
        int nombreÉlémentsNom = constanteMot(nom), nombreÉlémentsFormat = constanteMot(valeurDescription);
        return référence(valeurGenre, identificateurPropriétaire, référence(12, nombreÉlémentsNom, nombreÉlémentsFormat));
    }
    static void émettreValeur(int valeur) {
        if (tailleCode == valeurCode.length) { valeurÉchec("bytecode too large"); return; }
        valeurCode[tailleCode++] = valeur & 255;
    }
    static void commande(int valeur, int arguments) { émettreValeur(valeur); émettreValeur(arguments >> 8); émettreValeur(arguments); }
    static void constanteNumérique(int valeur) {
        if (valeur >= -1 && valeur <= 5) { émettreValeur(valeur + 3); return; }
        int lancer = tailleConstante; écrireOctetConstante(3); écrireCourtConstante(valeur >>> 16); écrireCourtConstante(valeur);
        commande(19, registreConstante(lancer));
    }
    static int branche(int commande) { int résultat = tailleCode; commande(commande, 0); return résultat; }
    static void valeurLier(int branche, int objetCible) {
        if (erreur) return;
        int valeurDistance = objetCible - branche;
        if (valeurDistance < -32768 || valeurDistance > 32767 || branche < 0 || branche + 2 >= tailleCode) { valeurÉchec("invalid branch"); return; }
        valeurCode[branche + 1] = valeurDistance >> 8 & 255; valeurCode[branche + 2] = valeurDistance & 255;
    }
    static void valeurComparaison(int commande) {
        int valeurVrai = branche(commande); émettreValeur(3); int terminaison = branche(167);
        valeurLier(valeurVrai, tailleCode); émettreValeur(4); valeurLier(terminaison, tailleCode);
    }
    static int valeurFormat() {
        if (motPrendre("void")) return 0;
        if (motPrendre("int")) return 1;
        if (motPrendre("boolean")) return 2;
        if (motPrendre("char")) return 5;
        if (motPrendre("FileInputStream")) return 6;
        if (motPrendre("FileOutputStream")) return 7;
        if (motPrendre("String")) { if (recevoir('[')) { valeurExigence(']'); return 4; } return 3; }
        valeurÉchec("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void ajouterFormat(int valeurType) {
        if (valeurType == 0) ajouterFinTexte('V');
        if (valeurType == 1) ajouterFinTexte('I');
        if (valeurType == 2) ajouterFinTexte('Z');
        if (valeurType == 3) ajouterFinMot("Ljava/lang/String;");
        if (valeurType == 4) ajouterFinMot("[Ljava/lang/String;");
        if (valeurType == 5) ajouterFinTexte('C');
        if (valeurType == 6) ajouterFinMot("Ljava/io/FileInputStream;");
        if (valeurType == 7) ajouterFinMot("Ljava/io/FileOutputStream;");
    }
    // Le compilateur restreint accepte les déclarations throws. Les corps de gestion d’exception nécessitent javac sur l’hôte.
    static void lireNomException() {
        boolean LotCoréen = motPrendre("français");
        if (LotCoréen) { valeurExigence('.'); motExiger("interne"); valeurExigence('.'); }
        if (!LotCoréen && (motPrendre("Exception") || motPrendre("IOException"))) return;
        if (motPrendre("exception") || motPrendre("ExceptionExécution") || motPrendre("ExceptionSortieEntrée") || motPrendre("ExceptionDélaiExpirationAttendre") || motPrendre("ExceptionRechercherAdresse") || motPrendre("ExceptionFichierManquant") || motPrendre("ExceptionCommunication") || motPrendre("ExceptionArgumentInvalide") || motPrendre("ÉchecFormatNuméro") || motPrendre("ExceptionBornes") || motPrendre("ExceptionBornesTableau") || motPrendre("ExceptionBornesChaîne") || motPrendre("ExceptionRéférenceRéférenceNulle") || motPrendre("ÉchecArithmétique") || motPrendre("ExceptionÉtatValeur") || motPrendre("ExceptionConversionTypeType") || motPrendre("ÉchecTailleTableauNégatif") || motPrendre("ÉchecStockerTableau") || motPrendre("ExceptionÉtatValeurFilExécution") || motPrendre("ExceptionInterrompuAttendre")) return;
        valeurÉchec("unsupported throws type");
    }
    static void lireDéclaration() {
        while (motPrendre("import")) {
            if (valeurMot(position, "français")) lireNomException();
            else {
                motExiger("java"); valeurExigence('.'); motExiger("io"); valeurExigence('.');
                if (!(motPrendre("FileInputStream") || motPrendre("FileOutputStream") || motPrendre("IOException"))) valeurÉchec("unsupported import");
            }
            valeurExigence(';');
        }
        motPrendre("public"); motPrendre("final"); motExiger("class"); jetonClasse = valeurIdentificateur();
        constanteClasse = référence(7, constanteJeton(jetonClasse), 0);
        constanteParent = référence(7, constanteMot("java/lang/Object"), 0); constanteCode = constanteMot("Code"); valeurExigence('{');
        while (!erreur && valeurGenre() != '}') {
            if (nombreÉlémentsMéthode == 32) { valeurÉchec("too many methods"); break; }
            int entréeÉlémentAccès = motPrendre("public") ? 1 : motPrendre("private") ? 2 : 0; motExiger("static");
            int Fonction = nombreÉlémentsMéthode++;
            accèsMéthode[Fonction] = entréeÉlémentAccès | 8;
            retournerMéthode[Fonction] = valeurFormat(); nomEntréeÉlémentMéthode[Fonction] = valeurIdentificateur(); valeurExigence('(');
            for (int valeurAvantCôté = 0; valeurAvantCôté < Fonction; valeurAvantCôté++) if (égalNoms(nomEntréeÉlémentMéthode[valeurAvantCôté], nomEntréeÉlémentMéthode[Fonction])) valeurÉchec("duplicate method (overloading unsupported)");
            while (!erreur && valeurGenre() != ')') {
                int nombre = nombreÉlémentsArgumentMéthode[Fonction];
                if (nombre == 16) { valeurÉchec("too many parameters"); break; }
                int valeurType = valeurFormat(); if (valeurType == 0) valeurÉchec("void parameter");
                typeArgumentMéthode[Fonction * 16 + nombre] = valeurType; nomArgumentMéthode[Fonction * 16 + nombre] = valeurIdentificateur();
                nombreÉlémentsArgumentMéthode[Fonction]++;
                if (!recevoir(',')) break;
            }
            valeurExigence(')');
            if (motPrendre("throws")) {
                do { lireNomException(); } while (!erreur && recevoir(','));
            }
            corpsMéthode[Fonction] = position; valeurExigence('{');
            int valeurImbrication = 1;
            while (position < nombreÉlémentsJeton && valeurImbrication > 0) {
                if (valeurGenre() == '{') valeurImbrication++;
                if (valeurGenre() == '}') valeurImbrication--;
                position++;
            }
            if (valeurImbrication != 0) valeurÉchec("unclosed method body");
            finMéthode[Fonction] = position;
            constanteNomMéthode[Fonction] = constanteJeton(nomEntréeÉlémentMéthode[Fonction]);
            longueurCaractère = 0; ajouterFinTexte('(');
            for (int nombre = 0; nombre < nombreÉlémentsArgumentMéthode[Fonction]; nombre++) ajouterFormat(typeArgumentMéthode[Fonction * 16 + nombre]);
            ajouterFinTexte(')'); ajouterFormat(retournerMéthode[Fonction]); constanteDescripteurMéthode[Fonction] = constanteCaractère();
        }
        valeurExigence('}'); if (position != nombreÉlémentsJeton) valeurÉchec("extra input after class");
    }
    static int trouverLocal(int nom) {
        for (int nombre = nombreÉlémentsLocal - 1; nombre >= 0; nombre--) if (profondeurLocal[nombre] >= 0 && égalNoms(nomLocal[nombre], nom)) return nombre;
        valeurÉchec("unknown variable"); return 0;
    }
    static int ajouterLocal(int nom, int valeurType) {
        for (int nombre = 0; nombre < nombreÉlémentsLocal; nombre++) if (profondeurLocal[nombre] >= 0 && égalNoms(nomLocal[nombre], nom)) valeurÉchec("duplicate local variable");
        if (nombreÉlémentsLocal == 128) { valeurÉchec("too many locals"); return 0; }
        nomLocal[nombreÉlémentsLocal] = nom; typeLocal[nombreÉlémentsLocal] = valeurType; profondeurLocal[nombreÉlémentsLocal] = valeurProfondeur;
        return nombreÉlémentsLocal++;
    }
    static boolean typeEntier(int valeurType) { return valeurType == 1 || valeurType == 5; }
    static void lireLocal(int nombre) { émettreValeur(typeLocal[nombre] <= 2 || typeLocal[nombre] == 5 ? 21 : 25); émettreValeur(nombre); }
    static void écrireLocal(int nombre) { émettreValeur(typeLocal[nombre] <= 2 || typeLocal[nombre] == 5 ? 54 : 58); émettreValeur(nombre); }
    static void vérifierType(int donnéesEffectif, int attente) { if (donnéesEffectif != attente && !(donnéesEffectif == 5 && attente == 1)) valeurÉchec("type mismatch"); }
    static void lireValeurCaractère(int valeurJeton) {
        longueurCaractère = 0; int lancer = positionJeton[valeurJeton] + 1, terminaison = positionJeton[valeurJeton] + longueurJeton[valeurJeton] - 1;
        while (lancer < terminaison && !erreur) {
            int valeur = source[lancer++];
            if (valeur == '\\') {
                if (lancer == terminaison) { valeurÉchec("invalid escape"); break; }
                valeur = source[lancer++];
                if (valeur == 'n') valeur = 10;
                else if (valeur == 'r') valeur = 13;
                else if (valeur == 't') valeur = 9;
                else if (valeur == 'b') valeur = 8;
                else if (valeur == 'f') valeur = 12;
                else if (valeur != '\\' && valeur != '"' && valeur != '\'') valeurÉchec("unsupported escape");
            }
            ajouterFinTexte(valeur);
        }
    }
    static int analyserEntier(int valeurJeton, boolean valeurNégatif) {
        if (longueurJeton[valeurJeton] > 1 && source[positionJeton[valeurJeton]] == '0') valeurÉchec("octal literals unsupported");
        int valeur = 0;
        for (int nombre = 0; nombre < longueurJeton[valeurJeton]; nombre++) {
            int élémentListeChiffre = source[positionJeton[valeurJeton] + nombre] - '0';
            if (valeur < -214748364 || valeur == -214748364 && élémentListeChiffre > (valeurNégatif ? 8 : 7)) valeurÉchec("integer literal out of range");
            valeur = valeur * 10 - élémentListeChiffre;
        }
        return valeurNégatif ? valeur : -valeur;
    }
    static int expressionPrimaire() {
        if (motPrendre("new")) {
            int valeurType = valeurFormat();
            if (valeurType != 6 && valeurType != 7) { valeurÉchec("only file streams supported by new in source"); return 0; }
            String valeurPropriétaire = valeurType == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            commande(187, référence(7, constanteMot(valeurPropriétaire), 0)); émettreValeur(89);
            valeurExigence('('); vérifierType(valeurExpression(), 3); boolean valeurContinuation = false;
            if (recevoir(',')) { if (valeurType != 7) valeurÉchec("input stream constructor arguments"); vérifierType(valeurExpression(), 2); valeurContinuation = true; }
            valeurExigence(')');
            commande(183, référenceExtérieur(10, valeurPropriétaire, "<init>", valeurContinuation ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return valeurType;
        }
        if (recevoir('(')) { int valeurType = valeurExpression(); valeurExigence(')'); return valeurType; }
        if (valeurGenre() == 257) { constanteNumérique(analyserEntier(position++, false)); return 1; }
        if (valeurGenre() == 258) { lireValeurCaractère(position++); commande(19, référence(8, constanteCaractère(), 0)); return 3; }
        if (valeurGenre() == 259) { lireValeurCaractère(position++); if (longueurCaractère != 1) valeurÉchec("character literal length"); constanteNumérique(Caractères[0]); return 5; }
        if (motPrendre("true")) { émettreValeur(4); return 2; }
        if (motPrendre("false")) { émettreValeur(3); return 2; }
        if (motPrendre("français")) {
            valeurExigence('.'); motExiger("interne"); valeurExigence('.');
            String valeurPropriétaire = "", valeurMéthode = "", valeurDescription = ""; int opérandePremier = 0, opérandeDeuxième = 0, opérandeTroisième = 0, opérandeQuatrième = 0, opérandeCinquième = 0, résultat = 0;
            if (motPrendre("Sortie")) {
                valeurPropriétaire = "français/interne/Sortie"; valeurExigence('.');
                if (motPrendre("écrireLigne")) { valeurMéthode = "écrireLigne"; valeurDescription = "(Ljava/lang/String;)V"; opérandePremier = 3; }
                else if (motPrendre("écrire")) { valeurMéthode = "écrire"; valeurDescription = "(Ljava/lang/String;)V"; opérandePremier = 3; }
                else if (motPrendre("écrireNuméro")) { valeurMéthode = "écrireNuméro"; valeurDescription = "(I)V"; opérandePremier = 1; }
                else valeurÉchec("unknown Korean output method");
            } else if (motPrendre("Caractères")) {
                valeurPropriétaire = "français/interne/Caractères"; valeurExigence('.'); opérandePremier = 3;
                if (motPrendre("longueur")) { valeurMéthode = "longueur"; valeurDescription = "(Ljava/lang/String;)I"; résultat = 1; }
                else if (motPrendre("nombreÉlémentsPointCode")) { valeurMéthode = "nombreÉlémentsPointCode"; valeurDescription = "(Ljava/lang/String;)I"; résultat = 1; }
                else if (motPrendre("analyserEntier")) { valeurMéthode = "analyserEntier"; valeurDescription = "(Ljava/lang/String;)I"; résultat = 1; }
                else if (motPrendre("écrireValeurEntier")) { valeurMéthode = "écrireValeurEntier"; valeurDescription = "(I)Ljava/lang/String;"; opérandePremier = 1; résultat = 3; }
                else if (motPrendre("texteÉgal")) { valeurMéthode = "texteÉgal"; valeurDescription = "(Ljava/lang/String;Ljava/lang/String;)Z"; opérandeDeuxième = 3; résultat = 2; }
                else if (motPrendre("texteColler")) { valeurMéthode = "texteColler"; valeurDescription = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; opérandeDeuxième = 3; résultat = 3; }
                else if (motPrendre("valeurCouper")) { valeurMéthode = "valeurCouper"; valeurDescription = "(Ljava/lang/String;II)Ljava/lang/String;"; opérandeDeuxième = 1; opérandeTroisième = 1; résultat = 3; }
                else valeurÉchec("unknown Korean text method");
            } else if (motPrendre("Fichier")) {
                valeurPropriétaire = "français/interne/Fichier"; valeurExigence('.'); opérandePremier = 3;
                if (motPrendre("lire")) { valeurMéthode = "lire"; valeurDescription = "(Ljava/lang/String;)Ljava/lang/String;"; résultat = 3; }
                else if (motPrendre("écrire")) { valeurMéthode = "écrire"; valeurDescription = "(Ljava/lang/String;Ljava/lang/String;)V"; opérandeDeuxième = 3; }
                else valeurÉchec("unknown Korean file method");
            } else if (motPrendre("Écran")) {
                valeurPropriétaire = "français/interne/Écran"; valeurExigence('.');
                if (motPrendre("valeurLargeur")) { valeurMéthode = "valeurLargeur"; valeurDescription = "()I"; résultat = 1; }
                else if (motPrendre("valeurHauteur")) { valeurMéthode = "valeurHauteur"; valeurDescription = "()I"; résultat = 1; }
                else if (motPrendre("rectangle")) { valeurMéthode = "rectangle"; valeurDescription = "(IIIII)V"; opérandePremier = 1; opérandeDeuxième = 1; opérandeTroisième = 1; opérandeQuatrième = 1; opérandeCinquième = 1; }
                else if (motPrendre("effacerEntréeÉlément")) { valeurMéthode = "effacerEntréeÉlément"; valeurDescription = "(I)V"; opérandePremier = 1; }
                else if (motPrendre("attendreFin")) { valeurMéthode = "attendreFin"; valeurDescription = "()V"; }
                else valeurÉchec("unknown Korean framebuffer method");
            } else valeurÉchec("unsupported Korean library class");
            valeurExigence('('); if (opérandePremier != 0) vérifierType(valeurExpression(), opérandePremier);
            if (opérandeDeuxième != 0) { valeurExigence(','); vérifierType(valeurExpression(), opérandeDeuxième); }
            if (opérandeTroisième != 0) { valeurExigence(','); vérifierType(valeurExpression(), opérandeTroisième); }
            if (opérandeQuatrième != 0) { valeurExigence(','); vérifierType(valeurExpression(), opérandeQuatrième); }
            if (opérandeCinquième != 0) { valeurExigence(','); vérifierType(valeurExpression(), opérandeCinquième); }
            valeurExigence(')'); commande(184, référenceExtérieur(10, valeurPropriétaire, valeurMéthode, valeurDescription)); return résultat;
        }
        if (motPrendre("Integer")) {
            valeurExigence('.'); motExiger("parseInt"); valeurExigence('('); vérifierType(valeurExpression(), 3); valeurExigence(')');
            commande(184, référenceExtérieur(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int nom = valeurIdentificateur();
        if (recevoir('(')) {
            int Fonction = -1;
            for (int nombre = 0; nombre < nombreÉlémentsMéthode; nombre++) if (égalNoms(nom, nomEntréeÉlémentMéthode[nombre])) Fonction = nombre;
            if (Fonction < 0) { valeurÉchec("unknown static method"); return 0; }
            int nombre = 0;
            while (!erreur && valeurGenre() != ')') {
                if (nombre >= nombreÉlémentsArgumentMéthode[Fonction]) { valeurÉchec("too many arguments"); break; }
                vérifierType(valeurExpression(), typeArgumentMéthode[Fonction * 16 + nombre++]); if (!recevoir(',')) break;
            }
            valeurExigence(')'); if (nombre != nombreÉlémentsArgumentMéthode[Fonction]) valeurÉchec("argument count mismatch");
            commande(184, référence(10, constanteClasse, référence(12, constanteNomMéthode[Fonction], constanteDescripteurMéthode[Fonction])));
            return retournerMéthode[Fonction];
        }
        int portéeLocal = trouverLocal(nom), valeurType = typeLocal[portéeLocal]; lireLocal(portéeLocal);
        while (!erreur) {
            if (recevoir('[')) { vérifierType(valeurType, 4); vérifierType(valeurExpression(), 1); valeurExigence(']'); émettreValeur(50); valeurType = 3; }
            else if (recevoir('.')) {
                if (valeurType == 6 || valeurType == 7) {
                    String valeurPropriétaire = valeurType == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (motPrendre("close")) { valeurExigence('('); valeurExigence(')'); commande(182, référenceExtérieur(10, valeurPropriétaire, "close", "()V")); valeurType = 0; }
                    else if (valeurType == 6 && motPrendre("read")) { valeurExigence('('); valeurExigence(')'); commande(182, référenceExtérieur(10, valeurPropriétaire, "read", "()I")); valeurType = 1; }
                    else if (valeurType == 7 && motPrendre("write")) { valeurExigence('('); vérifierType(valeurExpression(), 1); valeurExigence(')'); commande(182, référenceExtérieur(10, valeurPropriétaire, "write", "(I)V")); valeurType = 0; }
                    else { valeurÉchec("unsupported file stream method"); }
                    continue;
                }
                motExiger("length");
                if (valeurType == 4) { émettreValeur(190); valeurType = 1; }
                else { vérifierType(valeurType, 3); valeurExigence('('); valeurExigence(')'); commande(182, référenceExtérieur(10, "java/lang/String", "length", "()I")); valeurType = 1; }
            } else break;
        }
        return valeurType;
    }
    static int valeurUnaire() {
        if (++profondeurExpression > 64) { valeurÉchec("expression nesting too deep"); profondeurExpression--; return 0; }
        int valeurType;
        if (recevoir('!')) { vérifierType(valeurUnaire(), 2); valeurComparaison(153); valeurType = 2; }
        else if (recevoir('-')) {
            if (valeurGenre() == 257) constanteNumérique(analyserEntier(position++, true));
            else { vérifierType(valeurUnaire(), 1); émettreValeur(116); }
            valeurType = 1;
        } else if (recevoir('+')) { vérifierType(valeurUnaire(), 1); valeurType = 1; }
        else valeurType = expressionPrimaire();
        profondeurExpression--; return valeurType;
    }
    static int expressionMultiplication() {
        int valeurType = valeurUnaire();
        while (!erreur && (valeurGenre() == '*' || valeurGenre() == '/' || valeurGenre() == '%')) {
            int valeurEncodage = valeurGenre(); position++; vérifierType(valeurType, 1); vérifierType(valeurUnaire(), 1);
            émettreValeur(valeurEncodage == '*' ? 104 : valeurEncodage == '/' ? 108 : 112); valeurType = 1;
        }
        return valeurType;
    }
    static int expressionAddition() {
        int valeurType = expressionMultiplication();
        while (!erreur && (valeurGenre() == '+' || valeurGenre() == '-')) {
            int valeurEncodage = valeurGenre(); position++; int valeurFrontière = tailleCode, typeValeurRetourArrièreCôté = expressionMultiplication();
            if (valeurEncodage == '+' && (valeurType == 3 || typeValeurRetourArrièreCôté == 3)) { valeursCombiner(valeurFrontière, valeurType, typeValeurRetourArrièreCôté); valeurType = 3; }
            else { vérifierType(valeurType, 1); vérifierType(typeValeurRetourArrièreCôté, 1); émettreValeur(valeurEncodage == '+' ? 96 : 100); valeurType = 1; }
        }
        return valeurType;
    }
    static int référenceJoint(int valeurType) {
        if (valeurType != 1 && valeurType != 2 && valeurType != 3 && valeurType != 5) valeurÉchec("unsupported concatenation type");
        return référenceExtérieur(10, "java/lang/StringBuilder", "append", valeurType == 1 ? "(I)Ljava/lang/StringBuilder;"
            : valeurType == 2 ? "(Z)Ljava/lang/StringBuilder;" : valeurType == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void valeursCombiner(int valeurFrontière, int typeValeurAvantCôté, int typeValeurRetourArrièreCôté) {
        // Insérer le code produit avant celui de l’opérande droit pour que la valeur gauche déjà calculée soit ajoutée d’abord par append.
        // Les distances des branchements relatifs dans l’expression droite sont conservées, car toute la région est déplacée ensemble.
        int terminaison = tailleCode;
        commande(187, référence(7, constanteMot("java/lang/StringBuilder"), 0)); émettreValeur(89);
        commande(183, référenceExtérieur(10, "java/lang/StringBuilder", "<init>", "()V")); émettreValeur(95); commande(182, référenceJoint(typeValeurAvantCôté));
        if (erreur) return;
        int longueur = tailleCode - terminaison;
        for (int nombre = 0; nombre < longueur; nombre++) codeInséré[nombre] = valeurCode[terminaison + nombre];
        for (int nombre = terminaison - 1; nombre >= valeurFrontière; nombre--) valeurCode[nombre + longueur] = valeurCode[nombre];
        for (int nombre = 0; nombre < longueur; nombre++) valeurCode[valeurFrontière + nombre] = codeInséré[nombre];
        commande(182, référenceJoint(typeValeurRetourArrièreCôté)); commande(182, référenceExtérieur(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int expressionComparaison() {
        int valeurType = expressionAddition();
        while (!erreur && (valeurGenre() == '<' || valeurGenre() == '>' || valeurGenre() == 302 || valeurGenre() == 303)) {
            int valeurEncodage = valeurGenre(); position++; vérifierType(valeurType, 1); vérifierType(expressionAddition(), 1);
            valeurComparaison(valeurEncodage == '<' ? 161 : valeurEncodage == '>' ? 163 : valeurEncodage == 302 ? 164 : 162); valeurType = 2;
        }
        return valeurType;
    }
    static int expressionÉgalité() {
        int valeurType = expressionComparaison();
        while (!erreur && (valeurGenre() == 300 || valeurGenre() == 301)) {
            int valeurEncodage = valeurGenre(); position++; int typeValeurRetourArrièreCôté = expressionComparaison();
            if (valeurType == 0 || typeValeurRetourArrièreCôté == 0) valeurÉchec("void expression");
            if (!(typeEntier(valeurType) && typeEntier(typeValeurRetourArrièreCôté))) vérifierType(typeValeurRetourArrièreCôté, valeurType);
            valeurComparaison((valeurType <= 2 || valeurType == 5 ? 159 : 165) + (valeurEncodage == 301 ? 1 : 0)); valeurType = 2;
        }
        return valeurType;
    }
    static int etLogique() {
        int valeurType = expressionÉgalité();
        while (!erreur && recevoir(304)) {
            vérifierType(valeurType, 2); int opérandePremier = branche(153); vérifierType(expressionÉgalité(), 2); int opérandeDeuxième = branche(153);
            émettreValeur(4); int terminaison = branche(167); valeurLier(opérandePremier, tailleCode); valeurLier(opérandeDeuxième, tailleCode); émettreValeur(3); valeurLier(terminaison, tailleCode); valeurType = 2;
        }
        return valeurType;
    }
    static int valeurExpression() {
        int valeurType = etLogique();
        while (!erreur && recevoir(305)) {
            vérifierType(valeurType, 2); int opérandePremier = branche(154); vérifierType(etLogique(), 2); int opérandeDeuxième = branche(154);
            émettreValeur(3); int terminaison = branche(167); valeurLier(opérandePremier, tailleCode); valeurLier(opérandeDeuxième, tailleCode); émettreValeur(4); valeurLier(terminaison, tailleCode); valeurType = 2;
        }
        return valeurType;
    }
    static void valeurAffectation(boolean autoriserDéclaration) {
        if (valeurMot(position, "int") || valeurMot(position, "boolean") || valeurMot(position, "String") || valeurMot(position, "char")
            || valeurMot(position, "FileInputStream") || valeurMot(position, "FileOutputStream")) {
            if (!autoriserDéclaration) valeurÉchec("declaration not allowed here");
            int valeurType = valeurFormat(), nom = valeurIdentificateur(); valeurExigence('='); vérifierType(valeurExpression(), valeurType);
            écrireLocal(ajouterLocal(nom, valeurType)); return;
        }
        int nom = valeurIdentificateur(), portéeLocal = trouverLocal(nom);
        if (recevoir('=')) { vérifierType(valeurExpression(), typeLocal[portéeLocal]); écrireLocal(portéeLocal); }
        else if (valeurGenre() >= 308 && valeurGenre() <= 312) {
            int valeurEncodage = valeurGenre(); position++; lireLocal(portéeLocal); int valeurFrontière = tailleCode, typeValeurRetourArrièreCôté = valeurExpression();
            if (valeurEncodage == 308 && typeLocal[portéeLocal] == 3) valeursCombiner(valeurFrontière, 3, typeValeurRetourArrièreCôté);
            else {
                vérifierType(typeLocal[portéeLocal], 1); vérifierType(typeValeurRetourArrièreCôté, 1);
                émettreValeur(valeurEncodage == 308 ? 96 : valeurEncodage == 309 ? 100 : valeurEncodage == 310 ? 104 : valeurEncodage == 311 ? 108 : 112);
                if (typeLocal[portéeLocal] == 5) émettreValeur(146);
            }
            écrireLocal(portéeLocal);
        }
        else if (valeurGenre() == 306 || valeurGenre() == 307) {
            vérifierType(typeLocal[portéeLocal], 1); émettreValeur(132); émettreValeur(portéeLocal); émettreValeur(valeurGenre() == 306 ? 1 : 255); position++;
            if (typeLocal[portéeLocal] == 5) { lireLocal(portéeLocal); émettreValeur(146); écrireLocal(portéeLocal); }
        } else valeurÉchec("assignment or postfix increment required");
    }
    static void sortieÉcran() {
        motExiger("System"); valeurExigence('.'); motExiger("out"); valeurExigence('.');
        boolean nouvelleLigne = motPrendre("println"); if (!nouvelleLigne) motExiger("print"); valeurExigence('(');
        commande(178, référenceExtérieur(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean argumentVide = valeurGenre() == ')';
        int valeurType = argumentVide ? 0 : valeurExpression(); valeurExigence(')'); valeurExigence(';');
        String valeurDescription = valeurType == 0 ? "()V" : valeurType == 1 ? "(I)V" : valeurType == 2 ? "(Z)V" : valeurType == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (valeurType == 4 || valeurType >= 6 || valeurType == 0 && (!nouvelleLigne || !argumentVide)) valeurÉchec("unsupported print argument");
        commande(182, référenceExtérieur(10, "java/io/PrintStream", nouvelleLigne ? "println" : "print", valeurDescription));
    }
    static boolean valeurInstruction() {
        if (erreur) return false;
        if (valeurProfondeur > 32) { valeurÉchec("statement nesting too deep"); return false; }
        if (recevoir('{')) {
            valeurProfondeur++; boolean résultatRetourner = false;
            while (!erreur && valeurGenre() != '}') { if (résultatRetourner) valeurÉchec("unreachable statement"); résultatRetourner = valeurInstruction(); }
            valeurExigence('}'); for (int nombre = 0; nombre < nombreÉlémentsLocal; nombre++) if (profondeurLocal[nombre] == valeurProfondeur) profondeurLocal[nombre] = -1;
            valeurProfondeur--; return résultatRetourner;
        }
        if (recevoir(';')) return false;
        if (motPrendre("return")) {
            int valeurType = valeurGenre() == ';' ? 0 : valeurExpression(); vérifierType(valeurType, retournerMéthode[méthodeActuel]); valeurExigence(';');
            émettreValeur(valeurType == 0 ? 177 : valeurType <= 2 || valeurType == 5 ? 172 : 176); return true;
        }
        if (motPrendre("if")) {
            valeurExigence('('); vérifierType(valeurExpression(), 2); valeurExigence(')'); int valeurFaux = branche(153);
            valeurProfondeur++; boolean opérandePremier = instructionContrôle(); valeurProfondeur--;
            if (motPrendre("else")) { int terminaison = branche(167); valeurLier(valeurFaux, tailleCode); valeurProfondeur++; boolean opérandeDeuxième = instructionContrôle(); valeurProfondeur--; valeurLier(terminaison, tailleCode); return opérandePremier && opérandeDeuxième; }
            valeurLier(valeurFaux, tailleCode); return false;
        }
        if (motPrendre("while")) {
            int lancer = tailleCode; valeurExigence('('); vérifierType(valeurExpression(), 2); valeurExigence(')'); int terminaison = branche(153);
            valeurProfondeur++; instructionContrôle(); valeurProfondeur--; valeurLier(branche(167), lancer); valeurLier(terminaison, tailleCode); return false;
        }
        if (motPrendre("for")) {
            valeurProfondeur++; valeurExigence('('); if (valeurGenre() != ';') valeurAffectation(true); valeurExigence(';');
            int condition = tailleCode; if (valeurGenre() == ';') émettreValeur(4); else vérifierType(valeurExpression(), 2); valeurExigence(';');
            int terminaison = branche(153), texteCorps = branche(167), actualiser = tailleCode;
            if (valeurGenre() != ')') valeurAffectation(false); valeurExigence(')'); valeurLier(branche(167), condition); valeurLier(texteCorps, tailleCode);
            instructionContrôle(); valeurLier(branche(167), actualiser); valeurLier(terminaison, tailleCode);
            for (int nombre = 0; nombre < nombreÉlémentsLocal; nombre++) if (profondeurLocal[nombre] == valeurProfondeur) profondeurLocal[nombre] = -1;
            valeurProfondeur--; return false;
        }
        if (valeurMot(position, "System")) { sortieÉcran(); return false; }
        if (valeurGenre() == 256 && position + 1 < nombreÉlémentsJeton && (genreJeton[position + 1] == '(' || genreJeton[position + 1] == '.')) {
            int valeurType = valeurExpression(); if (valeurType != 0) émettreValeur(87); valeurExigence(';'); return false;
        }
        valeurAffectation(true); valeurExigence(';'); return false;
    }
    static boolean instructionContrôle() {
        if (valeurMot(position, "int") || valeurMot(position, "boolean") || valeurMot(position, "char") || valeurMot(position, "String")
            || valeurMot(position, "FileInputStream") || valeurMot(position, "FileOutputStream")) valeurÉchec("local declaration requires braces");
        return valeurInstruction();
    }
    static void émettreOctetClasse(int valeur) { if (tailleSortie == Sortie.length) valeurÉchec("class file too large"); else Sortie[tailleSortie++] = valeur & 255; }
    static void émettreCourtClasse(int valeur) { émettreOctetClasse(valeur >> 8); émettreOctetClasse(valeur); }
    static void émettreEntierClasse(int valeur) { émettreCourtClasse(valeur >>> 16); émettreCourtClasse(valeur); }
    static void écrireClasse() {
        émettreEntierClasse(0xcafebabe); émettreCourtClasse(0); émettreCourtClasse(49); émettreCourtClasse(nombreÉlémentsConstante);
        for (int nombre = 0; nombre < tailleConstante; nombre++) émettreOctetClasse(valeurConstante[nombre]);
        émettreCourtClasse(0x21); émettreCourtClasse(constanteClasse); émettreCourtClasse(constanteParent); émettreCourtClasse(0); émettreCourtClasse(0); émettreCourtClasse(nombreÉlémentsMéthode);
        for (int nombre = 0; nombre < nombreÉlémentsMéthode; nombre++) {
            émettreCourtClasse(accèsMéthode[nombre]); émettreCourtClasse(constanteNomMéthode[nombre]); émettreCourtClasse(constanteDescripteurMéthode[nombre]); émettreCourtClasse(1); émettreCourtClasse(constanteCode);
            émettreEntierClasse(12 + longueurMéthode[nombre]); émettreCourtClasse(128); émettreCourtClasse(variablesLocalesMéthode[nombre]); émettreEntierClasse(longueurMéthode[nombre]);
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueurMéthode[nombre]; entréeÉlémentEmplacement++) émettreOctetClasse(valeurCode[codeMéthode[nombre] + entréeÉlémentEmplacement]);
            émettreCourtClasse(0); émettreCourtClasse(0);
        }
        émettreCourtClasse(0);
    }
    public static int lancer() {
        if (Utilisateur.nombreÉlémentsArguments() == 1 && OutilJava.texteÉgal(Utilisateur.arguments(0), "-version")) {
            Utilisateur.écrire("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (Utilisateur.nombreÉlémentsArguments() != 1) { Utilisateur.écrire("Usage: javac FILE.java\n"); return 2; }
        int tailleNom = OutilJava.nom(texteNomFichier, Utilisateur.arguments(0));
        if (tailleNom < 6 || tailleNom > 62 || texteNomFichier[tailleNom - 5] != '.' || texteNomFichier[tailleNom - 4] != 'j'
            || texteNomFichier[tailleNom - 3] != 'a' || texteNomFichier[tailleNom - 2] != 'v' || texteNomFichier[tailleNom - 1] != 'a') {
            Utilisateur.écrire("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        tailleSource = Utilisateur.lireFichier(texteNomFichier, source);
        if (tailleSource < 0) { Utilisateur.écrire("javac: cannot read source: "); OutilJava.écrireNuméro(tailleSource); Utilisateur.écrireValeurCaractère(10); return 1; }
        tailleSource = OutilJava.décoderSource(source, tailleSource);
        if (tailleSource < 0) { Utilisateur.écrire("javac error: invalid UTF-8 source\n"); return 1; }
        valeurCouper(); if (!erreur) lireDéclaration();
        if (!erreur) {
            if (longueurJeton[jetonClasse] != tailleNom - 5) valeurÉchec("class name must match file name");
            for (int nombre = 0; nombre < tailleNom - 5; nombre++) if (source[positionJeton[jetonClasse] + nombre] != texteNomFichier[nombre]) valeurÉchec("class name must match file name");
        }
        for (méthodeActuel = 0; méthodeActuel < nombreÉlémentsMéthode && !erreur; méthodeActuel++) {
            position = corpsMéthode[méthodeActuel]; codeMéthode[méthodeActuel] = tailleCode; nombreÉlémentsLocal = 0; valeurProfondeur = 0;
            for (int nombre = 0; nombre < nombreÉlémentsArgumentMéthode[méthodeActuel]; nombre++) ajouterLocal(nomArgumentMéthode[méthodeActuel * 16 + nombre], typeArgumentMéthode[méthodeActuel * 16 + nombre]);
            boolean résultatRetourner = valeurInstruction();
            if (!résultatRetourner && retournerMéthode[méthodeActuel] != 0) valeurÉchec("missing return");
            // Le point de jonction après un branchement doit être une véritable instruction, conformément au vérificateur de version 49.
            if (retournerMéthode[méthodeActuel] == 0) émettreValeur(177);
            else { boolean Entier = retournerMéthode[méthodeActuel] <= 2 || retournerMéthode[méthodeActuel] == 5; émettreValeur(Entier ? 3 : 1); émettreValeur(Entier ? 172 : 176); }
            if (position != finMéthode[méthodeActuel]) valeurÉchec("invalid method body");
            variablesLocalesMéthode[méthodeActuel] = nombreÉlémentsLocal; longueurMéthode[méthodeActuel] = tailleCode - codeMéthode[méthodeActuel];
        }
        if (erreur) return 1;
        écrireClasse(); if (erreur) return 1;
        texteNomFichier[tailleNom - 4] = 'c'; texteNomFichier[tailleNom - 3] = 'l'; texteNomFichier[tailleNom - 2] = 'a';
        texteNomFichier[tailleNom - 1] = 's'; texteNomFichier[tailleNom] = 's'; texteNomFichier[tailleNom + 1] = 0;
        int résultat = Utilisateur.écrireFichier(texteNomFichier, Sortie, tailleSortie);
        if (résultat < 0) { Utilisateur.écrire("javac: cannot save class: "); OutilJava.écrireNuméro(résultat); Utilisateur.écrireValeurCaractère(10); return 1; }
        Utilisateur.écrire("Compiled: "); for (int nombre = 0; texteNomFichier[nombre] != 0; nombre++) Utilisateur.écrireValeurCaractère(texteNomFichier[nombre]);
        Utilisateur.écrire(" (JVM class version 49)\n"); return 0;
    }
}

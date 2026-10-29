// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Gère le découpage, la composition par bandes et le fond sous le pointeur. Le code de la carte accède à la mémoire d’affichage réelle. */
public final class ComposeurTamponImage {
    static int valeurLargeur, valeurHauteur, estCompositionEnCours, valeurFrontièreGauche, frontièreSupérieur, valeurFrontièreDroit, valeurFrontièreInférieur;
    static int coordonnéeHorizontalePointeur, coordonnéeVerticalePointeur, formePointeur;
    static int basCompteur, hautCompteur;
    static int[] pixelsComposé = new int[32 * 1920];
    static int[] arrièrePlanPointeur = new int[21 * 21];
    static int[] bornesRogné = new int[4];
    public static void préparer(int étendueLargeur, int longueur) {
        valeurLargeur = étendueLargeur; valeurHauteur = longueur; estCompositionEnCours = 0; formePointeur = 0;
        basCompteur = 0; hautCompteur = 0;
    }
    public static int obtenirLargeur() { return valeurLargeur; }
    public static int obtenirHauteur() { return valeurHauteur; }
    public static int obtenirBasCompteur() { return basCompteur; }
    public static int obtenirHautCompteur() { return hautCompteur; }
    public static int valeurRogner(int indiceOrdinal) { return bornesRogné[indiceOrdinal]; }
    static int ajouterLongueurPositif(int démarrerValeur, int longueur) {
        if (démarrerValeur > 2147483647 - longueur) return 2147483647;
        return démarrerValeur + longueur;
    }
    public static int rogner(int positionHorizontal, int positionVertical, int étendueLargeur, int longueur) {
        if (valeurLargeur == 0 || étendueLargeur <= 0 || longueur <= 0) return 0;
        int droit = ajouterLongueurPositif(positionHorizontal, étendueLargeur), côtéInférieur = ajouterLongueurPositif(positionVertical, longueur);
        int côtéGauche = estCompositionEnCours != 0 ? valeurFrontièreGauche : 0, côtéSupérieur = estCompositionEnCours != 0 ? frontièreSupérieur : 0;
        int positionHorizontalMaximal = estCompositionEnCours != 0 ? valeurFrontièreDroit : valeurLargeur, positionVerticalMaximal = estCompositionEnCours != 0 ? valeurFrontièreInférieur : valeurHauteur;
        if (positionHorizontal < côtéGauche) positionHorizontal = côtéGauche;
        if (positionVertical < côtéSupérieur) positionVertical = côtéSupérieur;
        if (droit > positionHorizontalMaximal) droit = positionHorizontalMaximal;
        if (côtéInférieur > positionVerticalMaximal) côtéInférieur = positionVerticalMaximal;
        if (droit <= positionHorizontal || côtéInférieur <= positionVertical) return 0;
        bornesRogné[0] = positionHorizontal; bornesRogné[1] = positionVertical;
        bornesRogné[2] = droit - positionHorizontal; bornesRogné[3] = côtéInférieur - positionVertical;
        return 1;
    }
    public static int lancer(int positionHorizontal, int positionVertical, int étendueLargeur, int longueur) {
        if (estCompositionEnCours != 0 || longueur > 32 || rogner(positionHorizontal, positionVertical, étendueLargeur, longueur) == 0) return 0;
        valeurFrontièreGauche = bornesRogné[0]; frontièreSupérieur = bornesRogné[1];
        valeurFrontièreDroit = valeurFrontièreGauche + bornesRogné[2]; valeurFrontièreInférieur = frontièreSupérieur + bornesRogné[3];
        estCompositionEnCours = 1; return 1;
    }
    static boolean bitPointeur(int positionHorizontal, int positionVertical, int valeurForme) {
        if (valeurForme == 1) return positionHorizontal >= 0 && positionHorizontal <= positionVertical / 2 && positionVertical < 16;
        if (valeurForme == 3) positionHorizontal = 20 - positionHorizontal;
        int valeurDifférence = positionHorizontal - positionVertical; if (valeurDifférence < 0) valeurDifférence = -valeurDifférence;
        return (valeurDifférence <= 1 && positionHorizontal >= 3 && positionHorizontal <= 17) ||
            (positionHorizontal >= 2 && positionHorizontal <= 8 && positionVertical >= 2 && positionVertical <= 8 && (positionHorizontal <= 3 || positionVertical <= 3)) ||
            (positionHorizontal >= 12 && positionHorizontal <= 18 && positionVertical >= 12 && positionVertical <= 18 && (positionHorizontal >= 17 || positionVertical >= 17));
    }
    static int pixelPointeur(int positionHorizontal, int positionVertical) {
        if (bitPointeur(positionHorizontal, positionVertical, formePointeur)) return 2;
        for (int ligne = -1; ligne <= 1; ligne++) for (int entréeÉlémentEmplacement = -1; entréeÉlémentEmplacement <= 1; entréeÉlémentEmplacement++)
            if (bitPointeur(positionHorizontal + entréeÉlémentEmplacement, positionVertical + ligne, formePointeur)) return 1;
        return 0;
    }
    static void pixelPrésenter(int positionHorizontal, int positionVertical, int valeurCouleur) {
        int entréeÉlémentEmplacement = positionHorizontal - coordonnéeHorizontalePointeur, ligne = positionVertical - coordonnéeVerticalePointeur;
        if (formePointeur != 0 && entréeÉlémentEmplacement >= 0 && ligne >= 0 && entréeÉlémentEmplacement < 21 && ligne < 21) {
            arrièrePlanPointeur[ligne * 21 + entréeÉlémentEmplacement] = valeurCouleur;
            int valeurPoint = pixelPointeur(entréeÉlémentEmplacement, ligne); if (valeurPoint != 0) valeurCouleur = valeurPoint == 2 ? 0xffffff : 0x101010;
        }
        if (CarteMatérielle.lirePixelPrésenter(positionHorizontal, positionVertical) != valeurCouleur) {
            CarteMatérielle.écrirePixelPrésenter(positionHorizontal, positionVertical, valeurCouleur);
            basCompteur++; if (basCompteur == 0) hautCompteur++;
        }
    }
    public static void terminer() {
        if (estCompositionEnCours == 0) return;
        for (int ligne = frontièreSupérieur; ligne < valeurFrontièreInférieur; ligne++) for (int entréeÉlémentEmplacement = valeurFrontièreGauche; entréeÉlémentEmplacement < valeurFrontièreDroit; entréeÉlémentEmplacement++)
            pixelPrésenter(entréeÉlémentEmplacement, ligne, pixelsComposé[(ligne - frontièreSupérieur) * 1920 + entréeÉlémentEmplacement]);
        estCompositionEnCours = 0;
    }
    public static int pixel(int positionHorizontal, int positionVertical, int valeurCouleur) {
        if (positionHorizontal < 0 || positionVertical < 0 || positionHorizontal >= valeurLargeur || positionVertical >= valeurHauteur) return 0;
        if (estCompositionEnCours != 0) {
            if (positionHorizontal >= valeurFrontièreGauche && positionHorizontal < valeurFrontièreDroit && positionVertical >= frontièreSupérieur && positionVertical < valeurFrontièreInférieur)
                pixelsComposé[(positionVertical - frontièreSupérieur) * 1920 + positionHorizontal] = valeurCouleur;
        } else pixelPrésenter(positionHorizontal, positionVertical, valeurCouleur);
        return 0;
    }
    public static void remplirRectangle(int positionHorizontal, int positionVertical, int étendueLargeur, int longueur, int valeurCouleur) {
        if (rogner(positionHorizontal, positionVertical, étendueLargeur, longueur) == 0) return;
        positionHorizontal = bornesRogné[0]; positionVertical = bornesRogné[1]; étendueLargeur = bornesRogné[2]; longueur = bornesRogné[3];
        for (int ligne = positionVertical; ligne < positionVertical + longueur; ligne++) for (int entréeÉlémentEmplacement = positionHorizontal; entréeÉlémentEmplacement < positionHorizontal + étendueLargeur; entréeÉlémentEmplacement++) {
            if (estCompositionEnCours != 0) pixelsComposé[(ligne - frontièreSupérieur) * 1920 + entréeÉlémentEmplacement] = valeurCouleur;
            else pixelPrésenter(entréeÉlémentEmplacement, ligne, valeurCouleur);
        }
    }
    public static void pointeur(int positionHorizontal, int positionVertical, int valeurForme) {
        if (valeurLargeur == 0) return;
        int positionHorizontalNouveau = positionHorizontal - (valeurForme >= 2 ? 10 : 0), positionVerticalNouveau = positionVertical - (valeurForme >= 2 ? 10 : 0);
        if (formePointeur == valeurForme && coordonnéeHorizontalePointeur == positionHorizontalNouveau && coordonnéeVerticalePointeur == positionVerticalNouveau) return;
        if (formePointeur != 0) for (int ligne = 0; ligne < 21; ligne++) for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 21; entréeÉlémentEmplacement++) {
            int opérandePremier = coordonnéeHorizontalePointeur + entréeÉlémentEmplacement, valeurTrois = coordonnéeVerticalePointeur + ligne;
            if (opérandePremier >= 0 && valeurTrois >= 0 && opérandePremier < valeurLargeur && valeurTrois < valeurHauteur) CarteMatérielle.écrirePixelPrésenter(opérandePremier, valeurTrois, arrièrePlanPointeur[ligne * 21 + entréeÉlémentEmplacement]);
        }
        formePointeur = valeurForme; coordonnéeHorizontalePointeur = positionHorizontalNouveau; coordonnéeVerticalePointeur = positionVerticalNouveau;
        if (valeurForme != 0) for (int ligne = 0; ligne < 21; ligne++) for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 21; entréeÉlémentEmplacement++) {
            int opérandePremier = coordonnéeHorizontalePointeur + entréeÉlémentEmplacement, valeurTrois = coordonnéeVerticalePointeur + ligne;
            if (opérandePremier >= 0 && valeurTrois >= 0 && opérandePremier < valeurLargeur && valeurTrois < valeurHauteur) {
                arrièrePlanPointeur[ligne * 21 + entréeÉlémentEmplacement] = CarteMatérielle.lirePixelPrésenter(opérandePremier, valeurTrois);
                int valeurPoint = pixelPointeur(entréeÉlémentEmplacement, ligne); if (valeurPoint != 0) CarteMatérielle.écrirePixelPrésenter(opérandePremier, valeurTrois, valeurPoint == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}

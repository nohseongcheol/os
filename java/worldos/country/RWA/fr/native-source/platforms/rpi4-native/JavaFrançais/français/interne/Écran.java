// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Tampon d’image RGB32 du noyau autonome, aux dimensions choisies au démarrage. */
public final class Écran {
    private Écran() {}
    public static int valeurLargeur() { int valeur = valeurNoyau.largeurÉcran(); if (valeur < 0) throw new ExceptionÉtatValeur("Aucun tampon d’image"); return valeur; }
    public static int valeurHauteur() { int valeur = valeurNoyau.hauteurÉcran(); if (valeur < 0) throw new ExceptionÉtatValeur("Aucun tampon d’image"); return valeur; }
    public static void rectangle(int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur, int valeurCouleur) {
        if (positionHorizontal < 0 || positionVertical < 0 || étendueLargeur < 0 || valeurHauteur < 0 || positionHorizontal > valeurLargeur() || positionVertical > valeurHauteur() || étendueLargeur > valeurLargeur() - positionHorizontal || valeurHauteur > valeurHauteur() - positionVertical) throw new ExceptionArgumentInvalide("Limites de l’écran");
        if (valeurNoyau.rectangle(positionHorizontal, positionVertical, étendueLargeur, valeurHauteur, valeurCouleur) < 0) throw new ExceptionÉtatValeur("Aucun tampon d’image");
    }
    public static void effacerEntréeÉlément(int valeurCouleur) { rectangle(0, 0, valeurLargeur(), valeurHauteur(), valeurCouleur); }
    public static void attendreFin() { if (valeurNoyau.attendreImagePour() < 0) throw new ExceptionÉtatValeur("Une saisie interactive est nécessaire"); }
}

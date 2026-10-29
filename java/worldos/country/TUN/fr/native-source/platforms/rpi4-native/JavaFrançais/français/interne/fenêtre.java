// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Fenêtre reliée directement à la JVM du projet et au gestionnaire de fenêtres du noyau. */
public final class fenêtre extends ÉlémentÉcran {
    public fenêtre(String titreFenêtre, int étendueLargeur, int valeurHauteur) {
        throw new ExceptionÉtatValeur("La JVM propre au système doit permettre de créer des fenêtres avec l’API française.");
    }
    public native void ajouterÉlément(ÉlémentÉcran valeurÉlément);
    public native void afficherFenêtre();
    public native void fermer();
    public native boolean estVisible();
}

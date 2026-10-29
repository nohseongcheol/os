// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Contrat commun des objets d’affichage de la JVM du projet ; ne conserve pas d’objets Swing standard. */
public abstract class ÉlémentÉcran {
    public native String lireTexte();
    public native void écrireTexte(String texte);
    public native void définirBornes(int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur);
}

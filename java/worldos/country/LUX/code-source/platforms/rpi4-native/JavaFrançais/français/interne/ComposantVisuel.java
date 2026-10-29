// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Méthodes pratiques pour créer les composants graphiques de l’API française. */
public final class ComposantVisuel {
    private ComposantVisuel() {}
    public static void invoquerUltérieur(TâcheTâcheExécutable ActionTâche) { FileAttenteÉvènement.invoquerUltérieur(ActionTâche); }
    public static étiquette valeurBalise(String texte, int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur) {
        return new étiquette(texte, positionHorizontal, positionVertical, étendueLargeur, valeurHauteur);
    }
    public static bouton bouton(String texte, int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur, RécepteurAction valeurRécepteur) {
        return new bouton(texte, positionHorizontal, positionVertical, étendueLargeur, valeurHauteur, valeurRécepteur);
    }
    public static ChampTexte ChampTexte(String texte, int positionHorizontal, int positionVertical, int étendueLargeur, int valeurHauteur) {
        return new ChampTexte(texte, positionHorizontal, positionVertical, étendueLargeur, valeurHauteur);
    }
}

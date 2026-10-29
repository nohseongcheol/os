// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Un fil est un flux d’exécution. La JVM du projet alterne les fils selon le nombre d’instructions exécutées. */
public final class Tâche {
    private Tâche() {}
    public static tâcheFond lancer(TâcheTâcheExécutable ActionTâche) { tâcheFond valeurFilExécution = new tâcheFond(ActionTâche); valeurFilExécution.démarrerTâche(); return valeurFilExécution; }
    public static void attendreFin(tâcheFond valeurFilExécution) throws ExceptionInterrompuAttendre { valeurFilExécution.attendreFin(); }
    public static boolean estVivant(tâcheFond valeurFilExécution) { return valeurFilExécution.estVivant(); }
    public static void céderTâche() { tâcheFond.céderTâche(); }
}

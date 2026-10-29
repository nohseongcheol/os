// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Flux d’exécution géré par l’ordonnanceur de la JVM du projet, sans encapsuler un Thread standard. */
public final class tâcheFond {
    public tâcheFond(TâcheTâcheExécutable ActionTâche) {
        throw new ExceptionÉtatValeur("La JVM propre au système doit permettre de créer des fils d’exécution avec l’API française.");
    }
    public native void démarrerTâche() throws ExceptionÉtatValeurFilExécution;
    public native void attendreFin() throws ExceptionInterrompuAttendre;
    public native boolean estVivant();
    public static native void céderTâche();
}

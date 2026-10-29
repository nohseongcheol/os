// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class Tâche {
    private Tâche() {}
    public static Thread lancer(String nom, Runnable action) {
        Thread valeurFilExécution = new Thread(action, nom);
        valeurFilExécution.start();
        return valeurFilExécution;
    }
    public static void attendreFin(Thread valeurFilExécution) throws InterruptedException { valeurFilExécution.join(); }
    public static void brièvementReste(long millisecondes) throws InterruptedException { Thread.sleep(millisecondes); }
    /** L’appelant doit libérer les ressources avec shutdown(). */
    public static ExecutorService valeurAtelier(int nombreÉlémentsFilExécution) { return Executors.newFixedThreadPool(nombreÉlémentsFilExécution); }
}

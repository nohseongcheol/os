// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.Java;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class Tarea {
    private Tarea() {}
    public static Thread ponerEnMarcha(String nombre, Runnable acción) {
        Thread valorHiloEjecución = new Thread(acción, nombre);
        valorHiloEjecución.start();
        return valorHiloEjecución;
    }
    public static void esperarFin(Thread valorHiloEjecución) throws InterruptedException { valorHiloEjecución.join(); }
    public static void brevementeRestanteParte(long milisegundos) throws InterruptedException { Thread.sleep(milisegundos); }
    /** El llamante debe liberar los recursos mediante shutdown(). */
    public static ExecutorService valorBancoTrabajo(int númeroElementosHiloEjecución) { return Executors.newFixedThreadPool(númeroElementosHiloEjecución); }
}

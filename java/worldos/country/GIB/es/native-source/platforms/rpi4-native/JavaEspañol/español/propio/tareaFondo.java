// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Flujo de ejecución gestionado por el planificador de la JVM propia, sin envolver un Thread estándar. */
public final class tareaFondo {
    public tareaFondo(TareaTareaEjecutable AcciónTarea) {
        throw new ExcepciónEstadoValor("La JVM propia debe permitir crear hilos mediante la API en español.");
    }
    public native void iniciarTarea() throws ExcepciónEstadoValorHiloEjecución;
    public native void esperarFin() throws ExcepciónInterrumpidoEsperar;
    public native boolean esVivo();
    public static native void cederTarea();
}

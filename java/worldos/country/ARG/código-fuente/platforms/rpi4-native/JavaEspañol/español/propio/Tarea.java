// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Un hilo es un flujo de ejecución. La JVM propia alterna los hilos según el número de instrucciones ejecutadas. */
public final class Tarea {
    private Tarea() {}
    public static tareaFondo ponerEnMarcha(TareaTareaEjecutable AcciónTarea) { tareaFondo valorHiloEjecución = new tareaFondo(AcciónTarea); valorHiloEjecución.iniciarTarea(); return valorHiloEjecución; }
    public static void esperarFin(tareaFondo valorHiloEjecución) throws ExcepciónInterrumpidoEsperar { valorHiloEjecución.esperarFin(); }
    public static boolean esVivo(tareaFondo valorHiloEjecución) { return valorHiloEjecución.esVivo(); }
    public static void cederTarea() { tareaFondo.cederTarea(); }
}

// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Entrega un trabajo a la cola de eventos de la pantalla propia. */
public final class ColaEvento {
    private ColaEvento() {}
    public static native void invocarPosterior(TareaTareaEjecutable AcciónTarea);
    public static native boolean esDespachoEnCursoEvento();
}

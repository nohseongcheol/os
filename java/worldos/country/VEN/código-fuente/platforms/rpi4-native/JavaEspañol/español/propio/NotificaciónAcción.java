// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Notificación de acción generada por el gestor de eventos de la JVM propia. */
public final class NotificaciónAcción {
    private NotificaciónAcción() {}
    public native String textoComando();
    public native ElementoPantalla fuenteEvento();
    public native int número();
}

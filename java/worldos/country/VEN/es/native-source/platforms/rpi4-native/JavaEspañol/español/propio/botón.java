// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Botón que envía notificaciones de acción en la pantalla propia. */
public final class botón extends ElementoPantalla {
    public botón(String texto, int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura, ReceptorAcción valorReceptor) {
        throw new ExcepciónEstadoValor("La JVM propia debe permitir crear botones mediante la API en español.");
    }
    public native void establecerReceptorAcción(ReceptorAcción valorReceptor);
}

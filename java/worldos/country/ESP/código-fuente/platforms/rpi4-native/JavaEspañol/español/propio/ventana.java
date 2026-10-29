// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Ventana conectada directamente con la JVM propia y el gestor de ventanas del núcleo. */
public final class ventana extends ElementoPantalla {
    public ventana(String títuloVentana, int extensiónRangoAnchura, int valorAltura) {
        throw new ExcepciónEstadoValor("La JVM propia debe permitir crear ventanas mediante la API en español.");
    }
    public native void añadirElemento(ElementoPantalla valorElemento);
    public native void mostrarVentana();
    public native void cerrar();
    public native boolean esVisible();
}

// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Contrato común de los objetos de pantalla de la JVM propia; no conserva objetos Swing estándar. */
public abstract class ElementoPantalla {
    public native String leerTexto();
    public native void escribirTexto(String texto);
    public native void establecerLímites(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura);
}

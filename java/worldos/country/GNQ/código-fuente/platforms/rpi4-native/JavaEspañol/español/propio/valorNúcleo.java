// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** ABI fija enlazada por la JVM propia; no es JNI ni un cargador de métodos native arbitrarios. */
public final class valorNúcleo {
    private valorNúcleo() {}
    public static native int milisegundos();
    public static native int esperarImagenPara();
    public static native int anchuraPantalla();
    public static native int alturaPantalla();
    public static native int rectángulo(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura, int valorColor);
}

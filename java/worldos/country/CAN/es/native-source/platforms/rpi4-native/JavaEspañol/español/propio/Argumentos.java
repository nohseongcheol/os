// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Argumentos de línea de órdenes que la JVM propia entrega al método de entrada; excluyen el nombre de clase. */
public final class Argumentos {
    private Argumentos() {}
    public static native int númeroElementosElementoLista();
    public static native String texto(int índiceOrdinal) throws ExcepciónLímites;
}

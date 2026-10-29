// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Búfer de imagen RGB32 del núcleo autónomo, con el tamaño elegido durante el arranque. */
public final class Pantalla {
    private Pantalla() {}
    public static int valorAnchura() { int valor = valorNúcleo.anchuraPantalla(); if (valor < 0) throw new ExcepciónEstadoValor("No hay búfer de imagen"); return valor; }
    public static int valorAltura() { int valor = valorNúcleo.alturaPantalla(); if (valor < 0) throw new ExcepciónEstadoValor("No hay búfer de imagen"); return valor; }
    public static void rectángulo(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura, int valorColor) {
        if (posiciónHorizontal < 0 || posiciónVertical < 0 || extensiónRangoAnchura < 0 || valorAltura < 0 || posiciónHorizontal > valorAnchura() || posiciónVertical > valorAltura() || extensiónRangoAnchura > valorAnchura() - posiciónHorizontal || valorAltura > valorAltura() - posiciónVertical) throw new ExcepciónArgumentoInválido("Límites de pantalla");
        if (valorNúcleo.rectángulo(posiciónHorizontal, posiciónVertical, extensiónRangoAnchura, valorAltura, valorColor) < 0) throw new ExcepciónEstadoValor("No hay búfer de imagen");
    }
    public static void borrarEntradaElemento(int valorColor) { rectángulo(0, 0, valorAnchura(), valorAltura(), valorColor); }
    public static void esperarFin() { if (valorNúcleo.esperarImagenPara() < 0) throw new ExcepciónEstadoValor("Se necesita entrada interactiva"); }
}

// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;
/** Salida estándar del núcleo autónomo. Los pares sustitutos UTF-16 se envían como UTF-8 por UART. */
public final class Salida {
    private Salida() {}
    public static void escribir(String texto) { System.out.print(texto); }
    public static void escribirLínea(String texto) { System.out.println(texto); }
    public static void escribirNúmero(int númeroValor) { System.out.println(númeroValor); }
}

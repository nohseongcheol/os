// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** FalloTamañoArregloNegativo: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class FalloTamañoArregloNegativo extends java.lang.NegativeArraySizeException {
    public FalloTamañoArregloNegativo() { super(); }
    public FalloTamañoArregloNegativo(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

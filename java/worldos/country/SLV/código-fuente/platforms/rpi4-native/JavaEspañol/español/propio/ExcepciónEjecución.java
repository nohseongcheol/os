// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónEjecución: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónEjecución extends java.lang.RuntimeException {
    public ExcepciónEjecución() { super(); }
    public ExcepciónEjecución(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

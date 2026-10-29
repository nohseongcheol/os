// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónEstadoValorHiloEjecución: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónEstadoValorHiloEjecución extends java.lang.IllegalThreadStateException {
    public ExcepciónEstadoValorHiloEjecución() { super(); }
    public ExcepciónEstadoValorHiloEjecución(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

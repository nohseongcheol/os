// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónEstadoValor: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónEstadoValor extends java.lang.IllegalStateException {
    public ExcepciónEstadoValor() { super(); }
    public ExcepciónEstadoValor(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

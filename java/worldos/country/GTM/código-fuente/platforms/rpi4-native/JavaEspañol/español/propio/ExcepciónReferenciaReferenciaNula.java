// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónReferenciaReferenciaNula: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónReferenciaReferenciaNula extends java.lang.NullPointerException {
    public ExcepciónReferenciaReferenciaNula() { super(); }
    public ExcepciónReferenciaReferenciaNula(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

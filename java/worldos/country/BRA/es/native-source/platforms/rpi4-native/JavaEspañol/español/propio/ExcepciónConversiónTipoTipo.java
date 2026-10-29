// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónConversiónTipoTipo: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónConversiónTipoTipo extends java.lang.ClassCastException {
    public ExcepciónConversiónTipoTipo() { super(); }
    public ExcepciónConversiónTipoTipo(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónLímitesCadena: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónLímitesCadena extends ExcepciónLímites {
    public ExcepciónLímitesCadena() { super(); }
    public ExcepciónLímitesCadena(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónLímites: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónLímites extends java.lang.IndexOutOfBoundsException {
    public ExcepciónLímites() { super(); }
    public ExcepciónLímites(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

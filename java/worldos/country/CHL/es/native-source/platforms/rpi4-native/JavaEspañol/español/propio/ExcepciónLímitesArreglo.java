// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónLímitesArreglo: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónLímitesArreglo extends ExcepciónLímites {
    public ExcepciónLímitesArreglo() { super(); }
    public ExcepciónLímitesArreglo(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

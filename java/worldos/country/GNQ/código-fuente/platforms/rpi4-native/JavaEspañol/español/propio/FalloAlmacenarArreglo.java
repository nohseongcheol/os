// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** FalloAlmacenarArreglo: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class FalloAlmacenarArreglo extends java.lang.ArrayStoreException {
    public FalloAlmacenarArreglo() { super(); }
    public FalloAlmacenarArreglo(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

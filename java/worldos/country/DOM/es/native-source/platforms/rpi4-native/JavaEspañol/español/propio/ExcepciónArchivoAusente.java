// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónArchivoAusente: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónArchivoAusente extends ExcepciónSalidaEntrada {
    public ExcepciónArchivoAusente() { super(); }
    public ExcepciónArchivoAusente(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

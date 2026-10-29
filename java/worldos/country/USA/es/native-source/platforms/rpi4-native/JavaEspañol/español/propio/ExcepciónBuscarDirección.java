// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónBuscarDirección: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónBuscarDirección extends ExcepciónSalidaEntrada {
    public ExcepciónBuscarDirección() { super(); }
    public ExcepciónBuscarDirección(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

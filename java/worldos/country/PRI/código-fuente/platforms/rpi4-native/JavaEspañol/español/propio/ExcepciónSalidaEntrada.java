// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónSalidaEntrada: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónSalidaEntrada extends java.io.IOException {
    public ExcepciónSalidaEntrada() { super(); }
    public ExcepciónSalidaEntrada(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

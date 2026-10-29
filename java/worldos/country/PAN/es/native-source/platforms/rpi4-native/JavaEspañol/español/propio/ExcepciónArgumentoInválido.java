// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** ExcepciónArgumentoInválido: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class ExcepciónArgumentoInválido extends java.lang.IllegalArgumentException {
    public ExcepciónArgumentoInválido() { super(); }
    public ExcepciónArgumentoInválido(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

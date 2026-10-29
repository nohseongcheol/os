// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** FalloFormatoNúmero: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class FalloFormatoNúmero extends ExcepciónArgumentoInválido {
    public FalloFormatoNúmero() { super(); }
    public FalloFormatoNúmero(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

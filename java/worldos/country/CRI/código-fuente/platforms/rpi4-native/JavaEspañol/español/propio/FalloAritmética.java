// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** FalloAritmética: excepción que se puede declarar, lanzar y capturar mediante la API en español. */
public class FalloAritmética extends java.lang.ArithmeticException {
    public FalloAritmética() { super(); }
    public FalloAritmética(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

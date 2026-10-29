// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.propio;

/** Indica la interrupción de una operación que esperaba un hilo, no la terminación de la propia tarea. */
public class ExcepciónInterrumpidoEsperar extends java.lang.InterruptedException {
    public ExcepciónInterrumpidoEsperar() { super(); }
    public ExcepciónInterrumpidoEsperar(String descripción) { super(descripción); }
    public String descripción() { return getMessage(); }
}

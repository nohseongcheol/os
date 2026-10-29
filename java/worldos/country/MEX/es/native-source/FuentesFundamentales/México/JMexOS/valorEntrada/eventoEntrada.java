// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package México.JMexOS.valorEntrada;

public final class eventoEntrada {
    public enum valorClaseTipo {
        abajoTecla,
        arribaTecla,
        movimientoRatón,
        pulsadoBotónRatón,
        liberadoBotónRatón
    }

    private final valorClaseTipo claseTipoEvento;
    private final int valorPrimero;
    private final int valorSegundo;

    public eventoEntrada(valorClaseTipo claseTipoEvento, int valorPrimero, int valorSegundo) {
        this.claseTipoEvento = claseTipoEvento;
        this.valorPrimero = valorPrimero;
        this.valorSegundo = valorSegundo;
    }

    public valorClaseTipo claseTipoEvento() {
        return claseTipoEvento;
    }

    public int valorPrimero() {
        return valorPrimero;
    }

    public int valorSegundo() {
        return valorSegundo;
    }
}


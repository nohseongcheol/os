// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Marruecos.JMarOS.Dispositivo;

/** Gestiona los pulsos del PIT y los momentos de desalojo. */
public final class Reloj {
    private final int segundoPorPulsos;
    private long númeroElementosPulso;

    public Reloj(int segundoPorPulsos) {
        if (segundoPorPulsos <= 0) {
            throw new IllegalArgumentException("초당 valorPulso 수가 올바르지 않습니다.");
        }
        this.segundoPorPulsos = segundoPorPulsos;
    }

    public long valorPulso() {
        return ++númeroElementosPulso;
    }

    public long númeroElementosPulso() {
        return númeroElementosPulso;
    }

    public long milisegundosTranscurrido() {
        return númeroElementosPulso * 1000L / segundoPorPulsos;
    }
}


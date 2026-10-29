// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guiné_Bissau.JGnbOS.entrada_VALOR;

public final class entrada_Evento {
    public enum Tipo_VALOR {
        Chave_inoperante,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Tipo_VALOR tipo_de_evento;
    private final int 첫째값;
    private final int SEGUNDO_VALOR;

    public entrada_Evento(Tipo_VALOR tipo_de_evento, int 첫째값, int SEGUNDO_VALOR) {
        this.tipo_de_evento = tipo_de_evento;
        this.첫째값 = 첫째값;
        this.SEGUNDO_VALOR = SEGUNDO_VALOR;
    }

    public Tipo_VALOR tipo_de_evento() {
        return tipo_de_evento;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEGUNDO_VALOR() {
        return SEGUNDO_VALOR;
    }
}


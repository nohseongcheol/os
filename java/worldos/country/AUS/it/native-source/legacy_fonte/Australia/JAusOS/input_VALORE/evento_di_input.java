// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Australia.JAusOS.input_VALORE;

public final class evento_di_input {
    public enum Kind_VALORE {
        키누름,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Kind_VALORE tipo_di_evento;
    private final int 첫째값;
    private final int SECONDO_VALORE;

    public evento_di_input(Kind_VALORE tipo_di_evento, int 첫째값, int SECONDO_VALORE) {
        this.tipo_di_evento = tipo_di_evento;
        this.첫째값 = 첫째값;
        this.SECONDO_VALORE = SECONDO_VALORE;
    }

    public Kind_VALORE tipo_di_evento() {
        return tipo_di_evento;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SECONDO_VALORE() {
        return SECONDO_VALORE;
    }
}


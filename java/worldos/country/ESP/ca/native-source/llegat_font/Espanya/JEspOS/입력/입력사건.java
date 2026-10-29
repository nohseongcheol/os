// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.입력;

public final class 입력사건 {
    public enum 종류 {
        키누름,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 사건종류;
    private final int 첫째값;
    private final int SEGON_VALOR;

    public 입력사건(종류 사건종류, int 첫째값, int SEGON_VALOR) {
        this.사건종류 = 사건종류;
        this.첫째값 = 첫째값;
        this.SEGON_VALOR = SEGON_VALOR;
    }

    public 종류 사건종류() {
        return 사건종류;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEGON_VALOR() {
        return SEGON_VALOR;
    }
}


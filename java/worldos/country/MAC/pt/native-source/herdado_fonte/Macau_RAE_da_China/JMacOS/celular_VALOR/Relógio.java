// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Macau_RAE_da_China.JMacOS.celular_VALOR;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Relógio {
    private final int 초당틱;
    private long contagem_em_escala;

    public Relógio(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tique_VALOR 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tique_VALOR() {
        return ++contagem_em_escala;
    }

    public long contagem_em_escala() {
        return contagem_em_escala;
    }

    public long 지난밀리초() {
        return contagem_em_escala * 1000L / 초당틱;
    }
}


// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Соединенные_Штаты.JUsaOS.входные_данные_ЗНАЧЕН;

public final class входные_данные_Событие {
    public enum Вид_ЗНАЧЕН {
        Ключ_отключен,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Вид_ЗНАЧЕН тип_события;
    private final int 첫째값;
    private final int СЕКУНДЫ_ЗНАЧЕН;

    public входные_данные_Событие(Вид_ЗНАЧЕН тип_события, int 첫째값, int СЕКУНДЫ_ЗНАЧЕН) {
        this.тип_события = тип_события;
        this.첫째값 = 첫째값;
        this.СЕКУНДЫ_ЗНАЧЕН = СЕКУНДЫ_ЗНАЧЕН;
    }

    public Вид_ЗНАЧЕН тип_события() {
        return тип_события;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int СЕКУНДЫ_ЗНАЧЕН() {
        return СЕКУНДЫ_ЗНАЧЕН;
    }
}


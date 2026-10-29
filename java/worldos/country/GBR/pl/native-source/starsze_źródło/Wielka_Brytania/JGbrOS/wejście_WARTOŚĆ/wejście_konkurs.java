// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wielka_Brytania.JGbrOS.wejście_WARTOŚĆ;

public final class wejście_konkurs {
    public enum Rodzaj_WARTOŚĆ {
        Klucz_niedziałający,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Rodzaj_WARTOŚĆ rodzaj_zdarzenia;
    private final int 첫째값;
    private final int SEKUNDA_WARTOŚĆ;

    public wejście_konkurs(Rodzaj_WARTOŚĆ rodzaj_zdarzenia, int 첫째값, int SEKUNDA_WARTOŚĆ) {
        this.rodzaj_zdarzenia = rodzaj_zdarzenia;
        this.첫째값 = 첫째값;
        this.SEKUNDA_WARTOŚĆ = SEKUNDA_WARTOŚĆ;
    }

    public Rodzaj_WARTOŚĆ rodzaj_zdarzenia() {
        return rodzaj_zdarzenia;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEKUNDA_WARTOŚĆ() {
        return SEKUNDA_WARTOŚĆ;
    }
}


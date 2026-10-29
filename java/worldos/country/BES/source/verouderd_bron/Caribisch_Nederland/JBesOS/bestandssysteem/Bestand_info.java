// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Caribisch_Nederland.JBesOS.bestandssysteem;

public final class Bestand_info {
    private final int Grootte;
    private final int vorm_soort;

    public Bestand_info(int Grootte, int vorm_soort) {
        this.Grootte = Grootte;
        this.vorm_soort = vorm_soort;
    }

    public int Grootte() {
        return Grootte;
    }

    public int vorm_soort() {
        return vorm_soort;
    }
}


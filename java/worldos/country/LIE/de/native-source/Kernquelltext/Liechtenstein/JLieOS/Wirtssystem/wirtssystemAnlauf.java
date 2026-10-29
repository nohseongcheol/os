// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Liechtenstein.JLieOS.Wirtssystem;

import Liechtenstein.JLieOS.Betriebskern.Betriebskern;

public final class wirtssystemAnlauf {
    private wirtssystemAnlauf() {
    }

    public static void main(String[] parameterArgument) {
        Betriebskern betriebskernWert = new Betriebskern(new WirtssystemHardware());
        betriebskernWert.ausführenVorgang();
        betriebskernWert.schrittAusführen();
    }
}


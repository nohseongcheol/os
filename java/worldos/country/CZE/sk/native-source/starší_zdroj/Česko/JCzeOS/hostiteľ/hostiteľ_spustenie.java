// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.hostiteľ;

import Česko.JCzeOS.jadro.jadro;

public final class hostiteľ_spustenie {
    private hostiteľ_spustenie() {
    }

    public static void main(String[] parameter_argument) {
        jadro jadro_VALUE = new jadro(new hostiteľ_hardvér());
        jadro_VALUE.Spustiť_2();
        jadro_VALUE.Vykonať_krok();
    }
}


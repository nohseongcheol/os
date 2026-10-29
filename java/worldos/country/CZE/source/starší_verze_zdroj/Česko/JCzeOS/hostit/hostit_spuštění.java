// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.hostit;

import Česko.JCzeOS.jádro.jádro;

public final class hostit_spuštění {
    private hostit_spuštění() {
    }

    public static void main(String[] parametr_argument) {
        jádro jádro_HODNOTA = new jádro(new hostit_hardware());
        jádro_HODNOTA.Spustit_2();
        jádro_HODNOTA.Provést_krok();
    }
}


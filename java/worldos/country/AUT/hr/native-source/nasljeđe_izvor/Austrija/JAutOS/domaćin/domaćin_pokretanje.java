// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Austrija.JAutOS.domaćin;

import Austrija.JAutOS.jezgra_sustava.jezgra_sustava;

public final class domaćin_pokretanje {
    private domaćin_pokretanje() {
    }

    public static void main(String[] parametar_argument) {
        jezgra_sustava jezgra_sustava_VALUE = new jezgra_sustava(new 호스트하드웨어());
        jezgra_sustava_VALUE.Pokreni();
        jezgra_sustava_VALUE.Izvrši_korak();
    }
}


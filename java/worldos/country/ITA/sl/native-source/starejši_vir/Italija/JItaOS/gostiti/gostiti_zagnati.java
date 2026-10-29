// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.gostiti;

import Italija.JItaOS.jedro.jedro;

public final class gostiti_zagnati {
    private gostiti_zagnati() {
    }

    public static void main(String[] parameter_argument) {
        jedro jedro_VALUE = new jedro(new gostiti_strojna_oprema());
        jedro_VALUE.Zaženi();
        jedro_VALUE.Izvedi_korak();
    }
}


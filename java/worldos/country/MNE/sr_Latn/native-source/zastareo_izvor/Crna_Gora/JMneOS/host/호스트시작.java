// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Crna_Gora.JMneOS.host;

import Crna_Gora.JMneOS.jezgro.jezgro;

public final class 호스트시작 {
    private 호스트시작() {
    }

    public static void main(String[] parametar_argument) {
        jezgro jezgro_VALUE = new jezgro(new 호스트하드웨어());
        jezgro_VALUE.koristiti();
        jezgro_VALUE.Izvrši_korak();
    }
}


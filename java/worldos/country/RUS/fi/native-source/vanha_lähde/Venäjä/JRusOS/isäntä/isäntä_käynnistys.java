// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.isäntä;

import Venäjä.JRusOS.ydin.ydin;

public final class isäntä_käynnistys {
    private isäntä_käynnistys() {
    }

    public static void main(String[] parametri_argumentti) {
        ydin ydin_ARVO = new ydin(new isäntä_laitteisto());
        ydin_ARVO.Suorita_2();
        ydin_ARVO.Suorita_vaihe();
    }
}


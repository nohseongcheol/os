// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.organizuoti;

import Jungtinė_Karalystė.JGbrOS.branduolys.branduolys;

public final class organizuoti_perkrovimas {
    private organizuoti_perkrovimas() {
    }

    public static void main(String[] parametras_argumentas) {
        branduolys branduolys_VALUE = new branduolys(new organizuoti_aparatūra());
        branduolys_VALUE.Paleisti();
        branduolys_VALUE.Vykdyti_veiksmas();
    }
}


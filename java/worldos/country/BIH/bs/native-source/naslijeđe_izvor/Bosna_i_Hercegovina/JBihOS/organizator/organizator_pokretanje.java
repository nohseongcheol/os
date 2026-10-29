// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.organizator;

import Bosna_i_Hercegovina.JBihOS.jezgro.jezgro;

public final class organizator_pokretanje {
    private organizator_pokretanje() {
    }

    public static void main(String[] parametar_argument) {
        jezgro jezgro_VALUE = new jezgro(new organizator_hardver());
        jezgro_VALUE.Pokreni();
        jezgro_VALUE.한단계실행();
    }
}


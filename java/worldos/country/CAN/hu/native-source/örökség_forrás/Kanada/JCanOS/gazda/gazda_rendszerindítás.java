// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.gazda;

import Kanada.JCanOS.kernel.kernel;

public final class gazda_rendszerindítás {
    private gazda_rendszerindítás() {
    }

    public static void main(String[] paraméter_argumentum) {
        kernel kernel_ÉRTÉK = new kernel(new gazda_hardver());
        kernel_ÉRTÉK.Futtatás();
        kernel_ÉRTÉK.végrehajt_lépés();
    }
}


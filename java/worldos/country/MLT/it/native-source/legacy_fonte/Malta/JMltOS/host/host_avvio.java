// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.host;

import Malta.JMltOS.Nucleo.Nucleo;

public final class host_avvio {
    private host_avvio() {
    }

    public static void main(String[] parametro_argomento) {
        Nucleo kernel_VALORE = new Nucleo(new host_hardware());
        kernel_VALORE.avvia();
        kernel_VALORE.Esegui_passaggio();
    }
}


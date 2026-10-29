// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankrijk.JFraOS.host;

import Frankrijk.JFraOS.Kern.Kern;

public final class host_bootstrap {
    private host_bootstrap() {
    }

    public static void main(String[] parameter_argument) {
        Kern kernel_WAARDE = new Kern(new host_hardware());
        kernel_WAARDE.starten();
        kernel_WAARDE.Uitvoeren_stap();
    }
}


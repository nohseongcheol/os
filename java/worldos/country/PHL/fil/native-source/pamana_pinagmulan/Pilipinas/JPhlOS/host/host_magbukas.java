// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Pilipinas.JPhlOS.host;

import Pilipinas.JPhlOS.kernel.kernel;

public final class host_magbukas {
    private host_magbukas() {
    }

    public static void main(String[] parameter_argumento) {
        kernel kernel_VALUE = new kernel(new 호스트하드웨어());
        kernel_VALUE.run();
        kernel_VALUE.한단계실행();
    }
}


// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Host;

import Lëtzebuerg.JLuxOS.Kernel.Kernel;

public final class Host_Start {
    private Host_Start() {
    }

    public static void main(String[] 인자) {
        Kernel Kernel_VALUE = new Kernel(new 호스트하드웨어());
        Kernel_VALUE.Laf();
        Kernel_VALUE.한단계실행();
    }
}


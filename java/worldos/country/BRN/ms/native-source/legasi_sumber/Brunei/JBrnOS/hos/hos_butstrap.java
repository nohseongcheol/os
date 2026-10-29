// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brunei.JBrnOS.hos;

import Brunei.JBrnOS.kernel.kernel;

public final class hos_butstrap {
    private hos_butstrap() {
    }

    public static void main(String[] parameter_argumen) {
        kernel kernel_VALUE = new kernel(new 호스트하드웨어());
        kernel_VALUE.Jalan();
        kernel_VALUE.laksanakan_langkah();
    }
}


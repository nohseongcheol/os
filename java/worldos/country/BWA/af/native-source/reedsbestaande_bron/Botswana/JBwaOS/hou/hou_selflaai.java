// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.hou;

import Botswana.JBwaOS.kern.kern;

public final class hou_selflaai {
    private hou_selflaai() {
    }

    public static void main(String[] 인자) {
        kern kern_VALUE = new kern(new hou_hardeware());
        kern_VALUE.Loop();
        kern_VALUE.한단계실행();
    }
}


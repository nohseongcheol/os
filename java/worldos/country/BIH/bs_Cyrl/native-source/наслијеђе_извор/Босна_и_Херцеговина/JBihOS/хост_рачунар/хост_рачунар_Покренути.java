// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.хост_рачунар;

import Босна_и_Херцеговина.JBihOS.језгро.језгро;

public final class хост_рачунар_Покренути {
    private хост_рачунар_Покренути() {
    }

    public static void main(String[] 인자) {
        језгро језгро_вриједност = new језгро(new 호스트하드웨어());
        језгро_вриједност.시작();
        језгро_вриједност.한단계실행();
    }
}


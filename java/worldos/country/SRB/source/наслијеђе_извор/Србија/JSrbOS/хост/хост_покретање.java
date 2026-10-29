// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.хост;

import Србија.JSrbOS.језгро.језгро;

public final class хост_покретање {
    private хост_покретање() {
    }

    public static void main(String[] параметар_аргумент) {
        језгро језгро_вриједност = new језгро(new 호스트하드웨어());
        језгро_вриједност.Покрени();
        језгро_вриједност.Изврши_корак();
    }
}

